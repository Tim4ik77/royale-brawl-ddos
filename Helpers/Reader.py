from io import BufferedReader, BytesIO

class Reader(BufferedReader):
    
    def __init__(self, initial_bytes):
        super().__init__(BytesIO(initial_bytes))

    def ReadInt8(self):
        return int.from_bytes(self.read(1), 'big', signed=True)
    
    def ReadUInt8(self):
        return int.from_bytes(self.read(1), 'big', signed=False)
    
    def ReadInt16(self):
        return int.from_bytes(self.read(2), 'big', signed=True)
    
    def ReadUInt16(self):
        return int.from_bytes(self.read(2), 'big', signed=False)
    
    def ReadInt24(self):
        return int.from_bytes(self.read(3), 'big', signed=True)
    
    def ReadUInt24(self):
        return int.from_bytes(self.read(3), 'big', signed=False)
    
    def ReadInt32(self):
        return int.from_bytes(self.read(4), 'big', signed=True)
    
    def ReadUInt32(self):
        return int.from_bytes(self.read(4), 'big', signed=False)

    def ReadVInt(self):
        n = self._read_varint(True)
        return (n >> 1) ^ (-(n & 1))

    def _read_varint(self, rotate: bool = True):
        Result = 0
        shift = 0
        while True:
            byte = self.ReadInt8()
            if rotate and shift == 0:
                seventh = (byte & 0x40) >> 6  # save 7th bit
                msb = (byte & 0x80) >> 7  # save msb
                n = byte << 1  # rotate to the left
                n = n & ~0x181  # clear 8th and 1st bit and 9th if any
                byte = n | (msb << 7) | seventh  # insert msb and 6th back in
            Result |= (byte & 0x7f) << shift
            shift += 7
            if not (byte & 0x80):
                break
        return Result

    def ReadString(self):
        length = self.ReadInt32()
        if length == - 1:
            return ''
        else:
            try:
                decoded = self.read(length)
            except MemoryError:
                raise IndexError('String out of range.')
            else:
                return decoded.decode('utf-8')
            
    def ReadLong(self):
        x = self.ReadInt32()
        y = self.ReadInt32()
        return x, y
    
    def ReadBoolean(self):
        a = self.ReadUInt8()
        if a == 1:
            return True
        else:
            return False
        
    def ReadDataReference(self):
        x = self.ReadVInt()
        if x != 0:
            y = self.ReadVInt()
        else:
            y = -1
        return x, y

    def ReadLogicLong(self):
        x = self.ReadVInt()
        y = self.ReadVInt()
        return x, y