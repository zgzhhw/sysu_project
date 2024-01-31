from xmlrpc.client import ServerProxy

# 连接 RPC 服务器
rpc_server = ServerProxy('http://localhost:8000', allow_none=True)

try:
    # 测试文件创建
    print(rpc_server.create_file("test_file.txt"))

    # 测试文件读取
    print(rpc_server.read_file("test_file.txt"))

    # 测试文件写入
    print(rpc_server.write_file("test_file.txt", "This is some data."))

    # 测试文件读取
    print(rpc_server.read_file("test_file.txt"))

    # 测试文件删除
    print(rpc_server.delete_file("test_file.txt"))

    # 测试删除后的文件读取
    print(rpc_server.read_file("test_file.txt"))

except Exception as e:
    print(f"Error: {e}")
