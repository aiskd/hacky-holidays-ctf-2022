import re

flag = [0 for i in range(33)]

text = """
    ((((((sVar1 == 0x21)  // password contains 33 characters &&
    (*param_1 == (byte)(param_1[6] * '\x02' - 0x1d))) &&
    (param_1[1] == (byte)(param_1[0x13] + 5))) &&
    (((param_1[2] == (byte)(((char)param_1[8] >> 1) + 0x13U) &&
    (param_1[3] == (byte)(param_1[0xf] + 0x35))) &&
    ((param_1[4] == (byte)(param_1[3] + 0xbc) &&
    ((param_1[5] == (byte)(param_1[0x11] + 0x28) &&
    (param_1[6] == (char)param_1[0x16] >> 1)))))))) && 
    (param_1[7] == (param_1[0xb] ^ param_1[0x15]))) &&
    (((((((param_1[8] == (param_1[5] ^ 7) &&
    (param_1[9] == (byte)(param_1[0xe] - 0x21))) &&
    (param_1[10] == (byte)(param_1[0x1e] + 7))) &&
    ((param_1[0xb] == (byte)(param_1[0x10] * '\x02') &&
    (param_1[0xc] == (byte)(param_1[0x1d] + param_1[9]))))) &&
    (param_1[0xd] == 0x31)) &&
    ((((param_1[0xe] == (byte)(param_1[0x1d] * '\x02' + 3) &&
    (param_1[0xf] == (*param_1 ^ 5))) &&
    (((param_1[0x10] == (byte)(((char)param_1[0x12] >> 1) * '\x02') &&
    (((param_1[0x11] == (param_1[0x14] ^ 0x40)
    && (param_1[0x12] == (param_1[0x17] ^ 10))) &&
    (param_1[0x13] == (byte)(param_1[7] - 2))))) &&
    (((param_1[0x14] == (param_1[10] ^ param_1[0x1c]) &&
    (param_1[0x15] == (char)param_1[0x19] >> 1)) &&
    (param_1[0x16] == (byte)((param_1[0x1f] | 0x61) - 2))))))) &&
    ((param_1[0x17] == 0x39 &&
    (param_1[0x18] == (byte)(param_1[0x12] * '\x02'))))))) &&
    (((param_1[0x19] == (byte)(param_1[0x10] + param_1[0x1a]) &&
    (((param_1[0x1a] == (byte)((char)param_1[0xb] / '\x02' + 7U) &&
    (param_1[0x1b] == (byte)((param_1[4] + 0x7b) * '\x02'))) &&
    (param_1[0x1c] == (byte)(param_1[1] - 0x13))))) &&
    (((param_1[0x1d] == (byte)(param_1[0x20] + 0xb3) &&
    (param_1[0x1e] == (byte)(param_1[0x1f] - param_1[0x10]))) &&
    ((param_1[0x1f] == (byte)(param_1[0xd] * '\x02' + 1) &&
    (param_1[0x20] == (byte)(param_1[4] + param_1[0xf])))))))))))
    """
print(text)

# 1. Replace binary hex with decimal values
hex_re = r"0x[\d|\w]{1,3}"
matches = set(re.findall(hex_re, text))
print(matches)
for m in matches:
    # convert the string into byte object
    print(m[1:])
    b = bytes(m[1:], 'utf-8')

    print(b)
    # convert byte object to decimal value
    int_val = int.from_bytes(b, "little")
    print(f"int: {int_val}")
    text = re.sub(m, int_val, text)

print(text)

