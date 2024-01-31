import os
import json
import base64
from xmlrpc.client import ServerProxy
from collections import OrderedDict

# 连接RPC服务器
rpc_server = ServerProxy(f'http://localhost:8000', allow_none=True)

# 缓存目录

script_directory = os.path.dirname(os.path.abspath(__file__))
LOCAL_DIR = os.path.join(script_directory, f'client_files')
CACHE_DIR = os.path.join(script_directory, f'client_cache')

# 确保缓存目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOCAL_DIR, exist_ok=True)

class LRUCache:
    def __init__(self, capacity=5):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get_cache_order(self):
        # 返回当前缓存中的文件顺序
        return list(self.cache.keys())

    def get(self, key):
        if key in self.cache:
            # 将该项移到字典的末尾，表示最近使用
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            return None

    def put(self, key, value):
        if len(self.cache) >= self.capacity:
            # 移除字典的第一项，即最久未使用的项
            self.cache.popitem(last=False)

        # 将新项加入字典末尾
        self.cache[key] = value
        self.cache.move_to_end(key)

    def pop(self, key):
        return self.cache.pop(key, None)

def read_file_with_cache(file_name, cache):
    # 检查缓存中是否存在该文件信息
    file_info = cache.get(file_name)
    
    if file_info and isinstance(file_info, dict):
        # 获取文件的最后修改时间
        cached_mtime = file_info.get('mtime', 0)
        # 获取服务器上文件的最后修改时间
        server_mtime = rpc_server.get_mtime(file_name)

        if cached_mtime == server_mtime:
            print(f"从缓存中读取文件 {file_name} 的信息")
            return file_info
        else:
            print(f"文件 {file_name} 已经被修改，更新缓存")

    # 调用远程RPC方法
    print(f"远程调用读取文件 {file_name} 的信息")
    file_info = rpc_server.read_file(file_name)
    # 获取文件的最后修改时间并存入缓存
    mtime = file_info.get('mtime', 0)
    file_info['mtime'] = mtime
    cache.put(file_name, file_info)
    
    return file_info


import shutil


def delete_file_with_cache(name, cache):
    # 从缓存中移除文件或文件夹信息
    cache.pop(name)

    client_path = os.path.join(LOCAL_DIR, name)

    try:
        if os.path.exists(client_path):
            if os.path.isfile(client_path):
                # 如果是文件，直接删除
                os.remove(client_path)
                print(f"文件 {name} 的本地副本删除成功")
            elif os.path.isdir(client_path):
                # 如果是文件夹，使用 shutil.rmtree 递归删除
                shutil.rmtree(client_path)
                print(f"文件夹 {name} 的本地副本删除成功")
        else:
            print(f"本地副本 {name} 不存在")

        # 调用远程RPC方法
        response = rpc_server.delete_file(name)
        return response
    except Exception as e:
        print(f"删除文件或文件夹 {name} 的本地副本失败：{e}")
        return f"删除文件或文件夹 {name} 的本地副本失败：{e}"



def upload_file(file_path,folder):
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return

    file_name = os.path.basename(file_path)
    client_file_path = os.path.join(LOCAL_DIR, file_name)

    # 将指定路径的文件复制到本地文件夹
    with open(file_path, 'rb') as source_file:
        with open(client_file_path, 'wb') as destination_file:
            destination_file.write(source_file.read())

    # 读取本地文件并将其转换为base64编码的字符串
    with open(client_file_path, 'rb') as file:
        file_data = base64.b64encode(file.read()).decode()

    # 调用远程RPC方法上传文件
    response = rpc_server.upload_file(file_name, file_data, folder)
    print(response)

def download_file(file_name):
    try:
        # 调用远程RPC方法下载文件
        file_info = rpc_server.download_file(file_name)

        if 'file_data' in file_info and 'file_name' in file_info:
            file_data = base64.b64decode(file_info['file_data'])
            client_file_path = os.path.join(LOCAL_DIR, file_info['file_name'])
            print(file_info['file_data'],file_info['file_name'])
            # 将文件数据写入客户端文件夹
            with open(client_file_path, 'wb') as file:
                file.write(file_data)

            print(f"文件 {file_name} 下载成功到 {client_file_path}")
        else:
            print(f"下载文件 {file_name} 失败：{file_info}")

    except Exception as e:
        print(f"Error during file download: {e}")

def create_folder_on_server(folder_name):
    try:
        # 调用远程RPC方法创建文件夹
        response = rpc_server.create_folder_sync(folder_name)
        print(response)
    except Exception as e:
        print(f"Error: {e}")

try:
    username = input("请输入用户名: ")
    password = input("请输入密码: ")

    # 调用远程RPC方法进行身份验证
    user_permissions = rpc_server.authenticate_user(username, password)

    if not user_permissions:
        print("身份验证失败")
        exit()

    # 初始化LRU缓存
    lru_cache = LRUCache()

    while True:
        # command = input("有命令集合如下：\ncreate_file \ncreate_folder \nlist \ndelete \nread \nwrite \nupload \ndownload \nexit \n请输入命令:")
        command = input("请输入命令(输入help显示命令集合):")

        if command == "exit":
            break

        if command not in user_permissions and '*' not in user_permissions:
            print("无权执行此操作")
            continue

        elif command in ['create_file', 'delete', 'read', 'write','download']:
            file_name = input("请输入文件名: ")

            if command == "write":
                data = input("请输入要写入的数据: ")
                # 异步更新服务器
                response = rpc_server.write_file(file_name, data)
                print(response)

            if command == "read":
                # 使用缓存的读取方法
                file_info = read_file_with_cache(file_name, lru_cache)
                print(file_info['content'])
                print(f"当前缓存文件顺序: {lru_cache.get_cache_order()}")

            elif command == "delete":
                # 使用带有缓存删除的方法
                response = delete_file_with_cache(file_name, lru_cache)
                print(response)

            elif command == "create_file":
                # 调用远程RPC方法
                response = rpc_server.create_file(file_name)
                print(response)

            elif command == 'download':
                download_file(file_name)


        elif command in ['upload']:
            
            if command == "upload":
                file_path = input("请输入文件路径: ")
                folder_path = input("请输入以服务器为根的文件夹路径(如果没有则enter)：")
                # 上传指定路径的文件到服务器
                upload_file(file_path,folder_path)

        elif command in ['create_folder']:
            folder_name = input("请输入文件夹名: ")
            full_folder_path = os.path.join(LOCAL_DIR, folder_name)
            os.makedirs(full_folder_path, exist_ok=True)
            create_folder_on_server(folder_name)

        elif command in ['list']:
            result = rpc_server.list_files()
            for r in result:
                print(r)

        elif command in ['help']:
            result =' create_file        --创建文件\n create_folder      --创建文件夹\n read               --读文件\n write              --写文件\n delete             --删除文件\n upload             --上传文件\n download           --下载文件\n list               --显示服务器根目录下文件组织\n exit               --退出'
            print(result)

except Exception as e:
    print(f"Error: {e}")
