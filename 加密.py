import struct
import random

def encode_obfuscated(value):
    # 随机拆分 value 为两个 double
    num1 = random.uniform(0, value)
    num2 = value - num1

    # 转换为 bytes（小端序）
    bytes_part1 = struct.pack('<d', num1)
    bytes_part2 = struct.pack('<d', num2)

    # 合并成 16 字节
    obfuscated_bytes = bytes_part1 + bytes_part2

    # 转换为 0-255 的整数列表（方便查看）
    obfuscated_data = list(obfuscated_bytes)
    return obfuscated_data

def xxx(num):
    print(f"{num}加密:\n{encode_obfuscated(num)}")

c=[1,20,50,100,200,500,1000,5000,10000]
for i in c:
    xxx(i)

# 测试：加密 10000
encoded_data = encode_obfuscated(1000.0)#想生成数字就改这里
print("加密后的数据:", encoded_data)  # 类似 [4, 119, 38, ...]



from 解密 import decode_obfuscated

# 解密验证
decoded_value = decode_obfuscated(encoded_data)
print("解密验证:", decoded_value)  # 输出 ≈10000.0