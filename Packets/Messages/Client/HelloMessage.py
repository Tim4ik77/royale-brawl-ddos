from Helpers.Writer import Writer

class Hello(object):
    
    def GetPacketData(self,major, seed):
        writer = Writer()
        writer.WriteInt32(0)
        writer.WriteInt32(major)
        writer.WriteInt32(0)
        writer.WriteInt32(seed)#magic number (просто сид, для криптографии)
        return writer.GetBuffer()
        
    def GetHeaderPacket(self, major, seed):
        packet = Hello.GetPacketData(self, major, seed)
        writer = Writer()
        writer.WriteInt16(10100)
        writer.WriteInt24(len(packet))
        writer.WriteInt16(0)
        writer.WriteBytes(packet)
        return writer.GetBuffer()