from xmlrpc.client import ServerProxy
import base64

# 连接RPC服务器
rpc_server = ServerProxy('http://localhost:8000', allow_none=True)


file_name = 'test_file.txt'
file_data = base64.b64encode(b'This is a test file.').decode()
folder = 'test_folder'

# 测试创建文件夹
folder_path = 'test_folder'
create_folder_response = rpc_server.create_folder_sync(folder_path)
print(create_folder_response)

# 测试上传文件
upload_response = rpc_server.upload_file(file_name, file_data, folder)
print(upload_response)

# 测试下载文件
download_response = rpc_server.download_file('test_folder/test_file.txt')
print(f"{download_response['file_name']}下载成功")

# 测试读文件
read_file_name = 'test_folder/test_file.txt'
read_response = rpc_server.read_file(read_file_name)
print(f"文件内容为:{read_response['content']}")

# 测试写文件
write_file_name = 'test_folder/test_file.txt'
write_file_data = 'It has been changed!'

write_response = rpc_server.write_file(write_file_name, write_file_data)
print(write_response)

# 测试读文件
read_file_name = 'test_folder/test_file.txt'
read_response = rpc_server.read_file(read_file_name)
print(f"文件内容为:{read_response['content']}")

# 测试删除文件夹
delete_folder_response = rpc_server.delete_file(folder_path)
print(delete_folder_response)



