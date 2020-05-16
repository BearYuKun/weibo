import random
from hashlib import sha256

# md5处理的较短
# md5的哈希不够安全  整体长度处理较短 容易产生碰撞  攻击  彩虹表 产生哈希碰撞
# shasum 多一些   都是一种算法   openssl

def gen_password(user_password):
    '''产生一个安全的密码'''
    bin_password = user_password.encode('utf8')  # 将密码转成 bytes 类型
    hash_value = sha256(bin_password).hexdigest()  # 计算用户密码的哈希值
    # %x 自动转化16进制
    salt = '%x' % random.randint(0x10000000, 0xffffffff)  # 产生随机盐
    # 0x去ipython查看
    # import hashilib
    # hashilib.sha256(b'123456789098765432').hexdigest()
    # len()
    # 0x10000000, 0xffffffff
    # ‘%x’ % random.randint(0x10000000, 0xffffffff)
    # '%s' % random.randint(0x10000000, 0xffffffff)
    safe_password = salt + hash_value
    return safe_password


def check_password(user_password, safe_password):
    '''检查用户密码是否正确'''
    bin_password = user_password.encode('utf8')  # 将密码转成 bytes 类型
    hash_value = sha256(bin_password).hexdigest()  # 计算用户密码的哈希值
    # 只需要检测8位之后的
    return hash_value == safe_password[8:]
