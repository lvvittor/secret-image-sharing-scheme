a = 231
print(a.to_bytes(1, byteorder="big"))

b = 0b1
print(b.to_bytes(1, byteorder="big"))

clear = 0b11111100

a &= clear
print(a.to_bytes(1, byteorder="big"))

result = a | b
print(result.to_bytes(1, byteorder="big"))