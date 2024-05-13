class Writer:
    def __init__(self):
        self.client = None
        self.buffer = b''

    def WriteUInt8(self, data):
        self.buffer += data.to_bytes(1, 'big', signed=False)

    def WriteInt8(self, data):
        self.buffer += data.to_bytes(1, 'big', signed=True)

    def WriteUInt16(self, data):
        self.buffer += data.to_bytes(2, 'big', signed=False)

    def WriteInt16(self, data):
        self.buffer += data.to_bytes(2, 'big', signed=True)

    def WriteUInt24(self, data):
        self.buffer += data.to_bytes(3, 'big', signed=False)

    def WriteInt24(self, data):
        self.buffer += data.to_bytes(3, 'big', signed=True)

    def WriteUInt32(self, data):
        self.buffer += data.to_bytes(4, 'big', signed=False)

    def WriteInt32(self, data):
        self.buffer += data.to_bytes(4, 'big', signed=True)

    def ClearBuffer(self):
        self.buffer = b''
    
    def WriteBytes(self, data):
        self.buffer += data

    def GetBuffer(self):
        return self.buffer

    def WriteHexa(self, data):
        if data:
            if data.startswith('0x'):
                data = data[2:]
            self.buffer += bytes.fromhex(''.join(data.split()).replace('-', ''))

    def WriteVInt(self, data):
        rotate = True
        final = b''
        if data == 0:
            self.WriteInt8(0)
        else:
            data = (data << 1) ^ (data >> 31)
            while data:
                b = data & 0x7f
                if data >= 0x80:
                    b |= 0x80
                if rotate:
                    rotate = False
                    lsb = b & 0x1
                    msb = (b & 0x80) >> 7
                    b >>= 1
                    b = b & ~0xC0
                    b = b | (msb << 7) | (lsb << 6)

                final += b.to_bytes(1, 'big')
                data >>= 7
        self.buffer += final

    def WriteString(self, string):
        if string is None:
            self.WriteInt32(-1)
        else:
            encoded = string.encode('utf-8')
            self.WriteInt32(len(encoded))
            self.buffer += encoded

    def WriteStringReference(self, string):
        encoded = string.encode('utf-8')
        self.WriteInt16(0)
        self.WriteVInt(len(encoded))
        self.buffer += encoded

    def WriteDataReference(self, x, y):
        self.WriteVInt(x)
        self.WriteVInt(y)
        
    def WriteLong(self, x, y):
        self.WriteInt32(x)
        self.WriteInt32(y)
        
    def WriteArrayVInt(self, l):
        self.WriteVInt(len(l))
        for item in l:
            self.WriteVInt(item)
            
    def WriteBoolean(self, t):
        if t:
            self.WriteUInt8(1)
        else:
            self.WriteUInt8(0)
            
    def WriteLogicLong(self, x, y):
        self.WriteVInt(x)
        self.WriteVInt(y)