import struct


def decode_obfuscated(obfuscated):
    # 将整数列表转换为字节数组
    byte_data = bytes(obfuscated)

    # 提取前8字节（第一个double）和后8字节（第二个double）
    first_double_bytes = byte_data[:8]
    second_double_bytes = byte_data[8:16]

    # 解析成 double
    first_double = struct.unpack('<d', first_double_bytes)[0]  # 小端序
    second_double = struct.unpack('<d', second_double_bytes)[0]

    # 相加得到原始值
    original_value = first_double + second_double
    return original_value

if __name__=='__main__':
    # 你的加密数据（16个整数，0-255）
    obfuscated_data = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    # 检查长度（必须16字节）
    if len(obfuscated_data) != 16:
        print("数据长度必须是16字节！")
    else:
        original_value = decode_obfuscated(obfuscated_data)
        print(f"解密后的值: {original_value}")
