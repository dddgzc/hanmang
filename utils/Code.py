import os
import base64

# 加密
def enCryption(openid):
    bytes_code = openid.encode("utf-8") # 想将字符串转换为base64 要将字符串先转化为2进制
    code = base64.b64encode(bytes_code) # 加密
    code = str(code,"utf-8")
    return code

# 解密
def deCryption(code):
    openid = base64.b64decode(code).decode("utf-8")
    return openid