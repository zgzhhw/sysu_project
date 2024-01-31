import os
import time
import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from time import sleep
import msvcrt

class DistributedServer:
    def __init__(self, server_id):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.server_files_directory = os.path.join(script_directory, f'server_{server_id}_files')
        
        # 创建当前服务器的文件夹
        os.makedirs(self.server_files_directory, exist_ok=True)

        self.global_lock = threading.Lock()  # 全局锁
        self.lock_in_use = False  # 辅助变量，用于指示锁的状态

        # 创建所有辅助服务器的文件夹
        self.auxiliary_servers = [os.path.join(script_directory, f'server_{i}_files') for i in range(1, 3) if i != server_id]
        for aux_server in self.auxiliary_servers:
            os.makedirs(aux_server, exist_ok=True)

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
                return file.read().decode()
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
                os.remove(file_path)

                # 删除辅助服务器上的文件
                for auxiliary_server in self.auxiliary_servers:
                    threading.Thread(target=self.delete_file_auxiliary, args=(file_name, auxiliary_server)).start()

                # 删除对应的锁文件
                self.release_lock(lock_file)
                lock_file_path = os.path.join(self.server_files_directory, f'{file_name}.lock')
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)

                return f"文件 {file_name} 删除成功"
            return f'文件 {file_name} 不存在'
        except:
            self.release_lock(lock_file)

    
    def delete_file_auxiliary(self, file_name, auxiliary_server):
        # 构建辅助服务器上文件的路径
        auxiliary_file_path = os.path.join(auxiliary_server, file_name)

        # 检查文件是否存在，存在则删除
        if os.path.exists(auxiliary_file_path):
            os.remove(auxiliary_file_path)

    def write_file(self, file_name, data):
        lock_file = self.acquire_lock(file_name)
        if not lock_file:
            return "无法获取文件锁，写操作失败"
        try:
            file_path = os.path.join(self.server_files_directory, file_name)

            if os.path.exists(file_path):
                # 更新server_files目录下的文件
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



def run_test(client_id, file_system):
    file_name = 'test'
    
    # 模拟并发写操作
    data_to_write = f"Data written by Client {client_id}"
    file_system.write_file(file_name, data_to_write)
    print(f"Client {client_id} wrote to file: {data_to_write}")

    # 模拟并发读操作
    read_data = file_system.read_file(file_name)
    print(f"Client {client_id} read from file: {read_data}")


# 创建分布式文件系统对象
file_system = DistributedServer(1)

# 启动RPC服务器
rpc_server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
rpc_server.register_instance(file_system)

# 启动服务器线程
server_thread = threading.Thread(target=rpc_server.serve_forever)
server_thread.start()

# 创建多个客户端线程并运行测试
num_clients = 10  # 可以根据需要调整客户端数量
client_threads = []

for i in range(num_clients):
    client_thread = threading.Thread(target=run_test, args=(i + 1, file_system))
    client_threads.append(client_thread)

for client_thread in client_threads:
    client_thread.start()

# 等待所有线程结束
for client_thread in client_threads:
    client_thread.join()

# 关闭RPC服务器
rpc_server.shutdown()
rpc_server.server_close()
