# Redis数据库的地址和端口
HOST = 'localhost'
PORT = 6379

# 如果Redis有密码，则添加这句密码，否则设置为None
PASSWORD = None

# 代理池数量界限
POOL_LOWER_THRESHOLD = 50
POOL_UPPER_THRESHOLD = 200

# 检查周期
VALID_CHECK_CYCLE = 300
POOL_LEN_CHECK_CYCLE = 20

# 测试API，用百度来测试
TEST_API='https://www.baidu.com'