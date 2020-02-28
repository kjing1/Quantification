# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% C类型数据读取 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# def GetMdArecHead(stream):
#     mda = {}
#     mda['suFlag'] = stream.Read16()
#     mda['suSize'] = stream.Read16()
#     mda['ucMkCode'] = stream.Read8()
#     mda['scode'] = stream.ReadString(31)
#     mda['uDate'] = stream.Read32()
#     mda['ucType'] = stream.Read8()
#     mda['ucRes'] = stream.Read8()
#     mda['suRecSize'] = stream.Read16()
#     mda['uCrc32'] = stream.Read32()
#     return mda

def String2Bytes(s): return s.encode(encoding='utf-8')


class Stream(object):
    """docstring for Stream"""

    def __init__(self, char_array):
        super(Stream, self).__init__()
        self.data_ = char_array
        self.offset_ = 0

    def Read8(self):
        ret = self.data_[self.offset_]
        self.offset_ += 1
        return ret

    def Read16(self):
        offset = self.offset_
        ret = self.data_[offset] | self.data_[offset + 1] << 8
        self.offset_ += 2
        return ret

    def Read32(self):
        offset = self.offset_
        ret = self.data_[offset] | self.data_[offset + 1] << 8 | self.data_[offset + 2] << 16 | self.data_[
            offset + 3] << 24
        self.offset_ += 4
        return ret

    def Read64(self):
        offset = self.offset_
        ret = self.data_[offset] | self.data_[offset + 1] << 8 \
              | self.data_[offset + 2] << 16 | self.data_[offset + 3] << 24 \
              | self.data_[offset + 4] << 32 | self.data_[offset + 4] << 40 \
              | self.data_[offset + 6] << 48 | self.data_[offset + 7] << 56
        self.offset_ += 8
        return ret

    def ReadChar(self):
        offset = self.offset_
        self.offset_ += 1
        return self.data_[offset:(offset + 1)].decode('gbk')

    def ReadString(self, size):
        offset = self.offset_
        self.offset_ += size
        return self.data_[offset:(offset + size)].decode('gbk')

    def Seek(self, size):
        self.offset_ += size

    def SeekBack(self, size):
        self.offset_ -= size

