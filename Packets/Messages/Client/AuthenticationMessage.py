from Helpers.Writer import Writer
import Helpers.Cryptography as crypto

def see_like_bytes(b):
    print([hex(x).split('x')[-1] for x in list(b)])

class Authentificate(object):
    
    def GetPacketData(self, key, nonce):
        writer = Writer()
        writer.WriteBytes(key)
        writer.WriteBytes(nonce)
        writer.WriteLong(0, 0) # Account ID
        writer.WriteString(None) # Token
        return writer.GetBuffer()
        
    def GetHeaderPacket(self, client_pk, client_sk, server_pk, nonce, key):
        packet = Authentificate.GetPacketData(self, key, nonce)
        encrypted_packet = crypto.encrypt(packet, nonce, server_pk, client_sk)
        writer = Writer()
        writer.WriteInt16(10101)
        writer.WriteInt24(len(client_pk)+len(encrypted_packet))
        writer.WriteInt16(0)
        writer.WriteBytes(client_pk)
        writer.WriteBytes(encrypted_packet)
        return writer.GetBuffer()