import os
import threading
import msvcrt
import base64
import shutil
import random
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from paxos import PaxosServer

class DistributedServer:
    def __init__(self, server_id):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.server_files_directory = os.path.join(script_directory, f'server_{server_id}_files')
        
        # 创建当前服务器的文件夹
        os.makedirs(self.server_files_directory, exist_ok=True)

        self.global_lock = threading.Lock()  # 全局锁
        self.lock_in_use = False  # 辅助变量，用于指示锁的状态

        # 创建所有辅助服务器的文件夹
        self.auxiliary_servers = [os.path.join(script_directory, f'server_{i}_files') for i in range(1, 4) if i != server_id]
        for aux_server in self.auxiliary_servers:
            os.makedirs(aux_server, exist_ok=True)

        self.users = {
            'user1': {'password': 'password1', 'permissions': ['read', 'write', 'delete','list', 'create_file']},
            'admin': {'password': 'admin', 'permissions': ['*']}
            # 可以根据需要添加更多用户和权限
        }

        self.paxos_server = PaxosServer(server_id)

    def authenticate_user(self, username, password):
        # 简单身份验证，检查用户名和密码是否匹配
        user_data = self.users.get(username)
        if user_data and user_data['password'] == password:
            return user_data['permissions']
        else:
            return None

    # 在需要权限控制的方法中调用此方法
    def check_permissions(self, username, required_permission):
        user_permissions = self.users[username]['permissions']
        if required_permission in user_permissions:
            return True
        else:
            return False

    def acquire_lock(self, file_name):
        lock_file_path = os.path.join(self.server_files_directory, f'{file_name}.lock')
        lock_file = open(lock_file_path, 'w')

        try:
            # 尝试获取文件锁，如果锁已被占用，则等待
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
        except Exception as e:
            print(f"获取文件锁时发生错误 ({file_name}): {e}")
            return False

        return lock_file

    def release_lock(self, lock_file):
        try:
            # 释放文件锁
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception as e:
            print(f"释放文件锁时发生错误: {e}")
        finally:
            lock_file.close()

    def read_file(self, file_name):

        file_path = os.path.join(self.server_files_directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                content = file.read().decode()
                mtime = os.path.getmtime(file_path)
                return {'content': content, 'mtime': mtime}
        else:
            return f"文件 {file_name} 不存在"

    def copy_file(self, file_name, source_path, destination_directory):
        destination_path = os.path.join(destination_directory, file_name)

        if os.path.exists(source_path):
            with open(source_path, 'rb') as source_file:
                data = source_file.read()
                with open(destination_path, 'wb') as destination_file:
                    destination_file.write(data)


    def delete_file(self, file_name):

        lock_file = self.acquire_lock(file_name)
        if not lock_file:
            return "无法获取文件锁，删除操作失败"
        try:
            file_path = os.path.join(self.server_files_directory, file_name)
            
            if os.path.exists(file_path):
                proposal_id = self.paxos_server.generate_id()  # 替换为生成唯一提案 ID 的机制
                value = f"DELETE {file_name}"  # 替换为你要提议的删除文件的值
                self.paxos_server.run_paxos(proposal_id, value)

                # 等待 Paxos 达成共识
                while not self.paxos_server.paxos_instance.accepted_proposal:
                    time.sleep(0.1)

            # 确保 Paxos 达成共识并执行相应的删除操作
                if self.paxos_server.paxos_instance.accepted_value == value:
                    if os.path.isfile(file_path):
                        # 如果是文件，直接删除
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        # 如果是文件夹，使用 shutil.rmtree 递归删除
                        shutil.rmtree(file_path)

                    # 删除辅助服务器上的文件或文件夹
                    for auxiliary_server in self.auxiliary_servers:
                        threading.Thread(target=self.delete_file_auxiliary, args=(file_name, auxiliary_server)).start()

                    # 删除对应的锁文件
                    self.release_lock(lock_file)
                    lock_file_path = os.path.join(self.server_files_directory, f'{file_name}.lock')
                    if os.path.exists(lock_file_path):
                        os.remove(lock_file_path)

                    return f"文件或文件夹 {file_name} 删除成功"
            return f'文件或文件夹 {file_name} 不存在'
        except Exception as e:
            self.release_lock(lock_file)
            return f"删除文件或文件夹 {file_name} 失败：{e}"

    def delete_file_auxiliary(self, file_name, auxiliary_server):
        # 构建辅助服务器上文件的路径
        auxiliary_file_path = os.path.join(auxiliary_server, file_name)

        # 检查文件或文件夹是否存在，存在则删除
        if os.path.exists(auxiliary_file_path):
            if os.path.isfile(auxiliary_file_path):
                os.remove(auxiliary_file_path)
            elif os.path.isdir(auxiliary_file_path):
                shutil.rmtree(auxiliary_file_path)


    def write_file(self, file_name, data):

        lock_file = self.acquire_lock(file_name)
        if not lock_file:
            return "无法获取文件锁，写操作失败"
        try:
            file_path = os.path.join(self.server_files_directory, file_name)

            if os.path.exists(file_path):
                # 更新server_files目录下的文件
                proposal_id = self.paxos_server.generate_id()  # 替换为生成唯一提案 ID 的机制
                value = f"WRITE {file_name}"  # 替换为你要提议的操作文件的值
                self.paxos_server.run_paxos(proposal_id, value)

                # 等待 Paxos 达成共识
                while not self.paxos_server.paxos_instance.accepted_proposal:
                    time.sleep(0.1)

            # 确保 Paxos 达成共识并执行相应的操作
                if self.paxos_server.paxos_instance.accepted_value == value:
                    with open(file_path, 'wb') as file:
                        file.write(data.encode())

                    self.release_lock(lock_file)
                    # 在辅助服务器上写入文件
                    for auxiliary_server in self.auxiliary_servers:
                        threading.Thread(target=self.copy_file, args=(file_name, file_path, auxiliary_server)).start()

                    return f"文件 {file_name} 写入成功"
            else:
                return f"文件 {file_name} 不存在"
        except:
            self.release_lock(lock_file)

    def create_file(self, file_name):

        file_path = os.path.join(self.server_files_directory, file_name)
        proposal_id = self.paxos_server.generate_id()  # 替换为生成唯一提案 ID 的机制
        value = f"CREATE {file_name}"  # 替换为你要提议的操作文件的值
        self.paxos_server.run_paxos(proposal_id, value)

        # 等待 Paxos 达成共识
        while not self.paxos_server.paxos_instance.accepted_proposal:
            time.sleep(0.1)

    # 确保 Paxos 达成共识并执行相应的操作
        if self.paxos_server.paxos_instance.accepted_value == value:
            if not os.path.exists(file_path):
                # 在server_files目录中创建文件，使用字节模拟文件内容
                with open(file_path, 'wb') as file:
                    file.write(b'')

                # 在所有辅助服务器上异步复制文件
                for auxiliary_server in self.auxiliary_servers:
                    threading.Thread(target=self.copy_file, args=(file_name, file_path, auxiliary_server)).start()

                return f"文件 {file_name} 创建成功"
            else:
                return f"文件 {file_name} 已存在"

    def upload_file(self, file_name, file_data, folder):

        lock_file = self.acquire_lock(file_name)
        if not lock_file:
            return "无法获取文件锁，上传操作失败"
        try:
            # 将二进制数据写入服务器文件夹

            proposal_id = self.paxos_server.generate_id()  # 替换为生成唯一提案 ID 的机制
            value = f"UPLOAD {file_name}"  # 替换为你要提议的操作文件的值
            self.paxos_server.run_paxos(proposal_id, value)

            # 等待 Paxos 达成共识
            while not self.paxos_server.paxos_instance.accepted_proposal:
                time.sleep(0.1)

        # 确保 Paxos 达成共识并执行相应的操作
            if self.paxos_server.paxos_instance.accepted_value == value:
                file_name = os.path.join(folder, file_name)
                server_file_path = os.path.join(self.server_files_directory, file_name)
                with open(server_file_path, 'wb') as file:
                    file.write(base64.b64decode(file_data))

                # 将文件同步到所有辅助服务器
                for auxiliary_server in self.auxiliary_servers:
                    threading.Thread(target=self.copy_file, args=(file_name, server_file_path, auxiliary_server)).start()

                return f"文件 {file_name} 上传成功"
        finally:
            self.release_lock(lock_file)

    def download_file(self, file_name):

        proposal_id = self.paxos_server.generate_id()  # 替换为生成唯一提案 ID 的机制
        value = f"DOWNLOAD {file_name}"  # 替换为你要提议的操作文件的值
        self.paxos_server.run_paxos(proposal_id, value)

        # 等待 Paxos 达成共识
        while not self.paxos_server.paxos_instance.accepted_proposal:
            time.sleep(0.1)

         # 确保 Paxos 达成共识并执行相应的操作
        if self.paxos_server.paxos_instance.accepted_value == value:
            file_path = os.path.join(self.server_files_directory, file_name)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_data = base64.b64encode(file.read()).decode()
                    return {'file_data': file_data, 'file_name': file_name}
            else:
                return f"文件 {file_name} 不存在"

        

    def create_folder_sync(self, folder_path):

        lock = threading.Lock()
        with lock:
            try:
                # 在当前服务器上创建文件夹
                proposal_id = self.paxos_server.generate_id()  # 替换为生成唯一提案 ID 的机制
                value = f"CREATE_FOLDER {folder_path}"  # 替换为你要提议的操作文件的值
                self.paxos_server.run_paxos(proposal_id, value)

                # 等待 Paxos 达成共识
                while not self.paxos_server.paxos_instance.accepted_proposal:
                    time.sleep(0.1)

            # 确保 Paxos 达成共识并执行相应的操作
                if self.paxos_server.paxos_instance.accepted_value == value:
                    full_folder_path = os.path.join(self.server_files_directory, folder_path)
                    os.makedirs(full_folder_path, exist_ok=True)

                    # 在所有辅助服务器上异步创建文件夹
                    for auxiliary_server in self.auxiliary_servers:
                        threading.Thread(target=self.create_folder_auxiliary, args=(folder_path, auxiliary_server)).start()

                    return f"文件夹 {folder_path} 在所有服务器上创建成功"
            except Exception as e:
                return f"创建文件夹 {folder_path} 失败：{e}"

    # 辅助服务器上的文件夹创建方法
    def create_folder_auxiliary(self, folder_path, auxiliary_server):
        lock = threading.Lock()
        with lock:
            try:
                full_folder_path = os.path.join(auxiliary_server, folder_path)
                os.makedirs(full_folder_path, exist_ok=True)
            except Exception as e:
                print(f"在辅助服务器上创建文件夹 {folder_path} 失败：{e}")


    def list_files(self, folder_path=".", indent=""):
        full_folder_path = os.path.join(self.server_files_directory, folder_path)

        def list_files_recursive(current_path, current_indent):
            result = []

            items = sorted(os.listdir(current_path))

            for i, item in enumerate(items):
                item_path = os.path.join(current_path, item)
                is_last = i == len(items) - 1

                result.append(current_indent + ("└── " if is_last else "├── ") + item)

                if os.path.isdir(item_path):
                    child_indent = current_indent + ("    " if is_last else "│   ")
                    result.extend(list_files_recursive(item_path, child_indent))

            return result

        return list_files_recursive(full_folder_path, indent)



    def get_file_content(self, file_name):
        self.acquire_lock()
        try:
            file_path = os.path.join(self.server_files_directory, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    return file.read().decode()
            else:
                return f"文件 {file_name} 不存在"
        finally:
            self.release_lock()

    def get_mtime(self, file_name):
        file_path = os.path.join(self.server_files_directory, file_name)
        if os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
            return mtime
        else:
            return 0



# 创建分布式文件系统对象
server_id = 1  # 当前服务器ID
distributed_server = DistributedServer(server_id)

# 创建RPC服务器
rpc_server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
rpc_server.register_instance(distributed_server)

print("RPC服务器已启动，等待客户端连接...")

# 启动服务器
rpc_server.serve_forever()
