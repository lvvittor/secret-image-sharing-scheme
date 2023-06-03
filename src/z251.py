class Z251:
    """
        a = Z251(200)
        b = Z251(30)

        print(a + b)  # Output: 24
        print(a - b)  # Output: 170
        print(a * b)  # Output: 60
        print(a ** 2) # Output: 40
        print(a / b)  # Output: 173
        print(a == b) # Output: False
        print(a != b) # Output: True
    """

    # Inverse table for the finite field of integers modulo 251
    INVERSE_TABLE = {
        0: 0,
        1: 1,
        2: 126,
        3: 84,
        4: 63,
        5: 201,
        6: 42,
        7: 36,
        8: 157,
        9: 28,
        10: 226,
        11: 137,
        12: 21,
        13: 58,
        14: 18,
        15: 67,
        16: 204,
        17: 192,
        18: 14,
        19: 185,
        20: 113,
        21: 12,
        22: 194,
        23: 131,
        24: 136,
        25: 241,
        26: 29,
        27: 93,
        28: 9,
        29: 26,
        30: 159,
        31: 81,
        32: 102,
        33: 213,
        34: 96,
        35: 208,
        36: 7,
        37: 95,
        38: 218,
        39: 103,
        40: 182,
        41: 49,
        42: 6,
        43: 216,
        44: 97,
        45: 106,
        46: 191,
        47: 235,
        48: 68,
        49: 41,
        50: 246,
        51: 64,
        52: 140,
        53: 90,
        54: 172,
        55: 178,
        56: 130,
        57: 229,
        58: 13,
        59: 234,
        60: 205,
        61: 107,
        62: 166,
        63: 4,
        64: 51,
        65: 112,
        66: 232,
        67: 15,
        68: 48,
        69: 211,
        70: 104,
        71: 99,
        72: 129,
        73: 196,
        74: 173,
        75: 164,
        76: 109,
        77: 163,
        78: 177,
        79: 197,
        80: 91,
        81: 31,
        82: 150,
        83: 124,
        84: 3,
        85: 189,
        86: 108,
        87: 176,
        88: 174,
        89: 110,
        90: 53,
        91: 80,
        92: 221,
        93: 27,
        94: 243,
        95: 37,
        96: 34,
        97: 44,
        98: 146,
        99: 71,
        100: 123,
        101: 169,
        102: 32,
        103: 39,
        104: 70,
        105: 153,
        106: 45,
        107: 61,
        108: 86,
        109: 76,
        110: 89,
        111: 199,
        112: 65,
        113: 20,
        114: 240,
        115: 227,
        116: 132,
        117: 118,
        118: 117,
        119: 135,
        120: 228,
        121: 195,
        122: 179,
        123: 100,
        124: 83,
        125: 249,
        126: 2,
        127: 168,
        128: 151,
        129: 72,
        130: 56,
        131: 23,
        132: 116,
        133: 134,
        134: 133,
        135: 119,
        136: 24,
        137: 11,
        138: 231,
        139: 186,
        140: 52,
        141: 162,
        142: 175,
        143: 165,
        144: 190,
        145: 206,
        146: 98,
        147: 181,
        148: 212,
        149: 219,
        150: 82,
        151: 128,
        152: 180,
        153: 105,
        154: 207,
        155: 217,
        156: 214,
        157: 8,
        158: 224,
        159: 30,
        160: 171,
        161: 198,
        162: 141,
        163: 77,
        164: 75,
        165: 143,
        166: 62,
        167: 248,
        168: 127,
        169: 101,
        170: 220,
        171: 160,
        172: 54,
        173: 74,
        174: 88,
        175: 142,
        176: 87,
        177: 78,
        178: 55,
        179: 122,
        180: 152,
        181: 147,
        182: 40,
        183: 203,
        184: 236,
        185: 19,
        186: 139,
        187: 200,
        188: 247,
        189: 85,
        190: 144,
        191: 46,
        192: 17,
        193: 238,
        194: 22,
        195: 121,
        196: 73,
        197: 79,
        198: 161,
        199: 111,
        200: 187,
        201: 5,
        202: 210,
        203: 183,
        204: 16,
        205: 60,
        206: 145,
        207: 154,
        208: 35,
        209: 245,
        210: 202,
        211: 69,
        212: 148,
        213: 33,
        214: 156,
        215: 244,
        216: 43,
        217: 155,
        218: 38,
        219: 149,
        220: 170,
        221: 92,
        222: 225,
        223: 242,
        224: 158,
        225: 222,
        226: 10,
        227: 115,
        228: 120,
        229: 57,
        230: 239,
        231: 138,
        232: 66,
        233: 237,
        234: 59,
        235: 47,
        236: 184,
        237: 233,
        238: 193,
        239: 230,
        240: 114,
        241: 25,
        242: 223,
        243: 94,
        244: 215,
        245: 209,
        246: 50,
        247: 188,
        248: 167,
        249: 125,
        250: 250,
    }

    def __init__(self, value):
        print(f"value: {value}")
        print(f"type(value): {type(value)}")
        self.value = value % 251

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, Z251):
            return Z251((self.value + other.value) % 251)
        raise ValueError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, Z251):
            return Z251((self.value - other.value) % 251)
        raise ValueError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, Z251):
            return Z251((self.value * other.value) % 251)
        raise ValueError("Unsupported operand type for *")
    
    def __pow__(self, exponent):
        if isinstance(exponent, int):
            return Z251(pow(self.value, exponent, 251))
        raise ValueError("Unsupported operand type for pow()")

    def __truediv__(self, other):
        if isinstance(other, Z251):
            if other.value == 0:
                raise ValueError("Division by zero is not allowed")
            else:
                inverse = Z251.INVERSE_TABLE[other.value]
                return Z251((self.value * inverse) % 251)
        raise ValueError("Unsupported operand type for /")

    def __eq__(self, other):
        if isinstance(other, Z251):
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self.__eq__(other)