# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# MoldUDP bytearray/packet decoder according to the specification from Nasdaq
# http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf
#
from struct import unpack_from
from struct import calcsize

from moldudp.msg.msgsub import MsgSubscriber
from moldudp.codec.const import END_OF_SESSION
from moldudp.codec.const import HEART_BEAT
from moldudp.codec.const import PAYLOAD_OFFSET
from moldudp.codec.const import SESSION_OFFSET
from moldudp.codec.const import MESSAGE_SIZE_FIELD_LEN


class MoldUDPDecoder:

    # subscriber is the application message processor
    def __init__(self, subscriber: MsgSubscriber, debug=False):
        self.__offset = SESSION_OFFSET
        self.__subscriber = subscriber
        self.__debug = debug

    def __process_msghdr(self, session, seq, msgcount):
        self.__session = session
        self.__seq = seq
        self.__msgcount = msgcount
        if (self.__debug == True):
            print("RECEIVED HDR SESSION: {}".format(self.__session))
            print("RECEIVED HDR SEQ:     {}".format(self.__seq))
            print("RECEIVED MSG COUNT:   {}".format(self.__msgcount))

    def __process_msgblks(self):
        i = self.__msgcount
        while (i > 0):
            # message block consists of 2-bytes message length and follows by message data with previously specified length
            blk_sz = unpack_from('>H', self.__buffer, self.__offset)[0]
            self.__offset += MESSAGE_SIZE_FIELD_LEN
            fmt = '>{}s'.format(blk_sz)
            msg = unpack_from(fmt, self.__buffer, self.__offset)[0]
            if (self.__subscriber):
                self.__subscriber.on_msgblk(msg)
            self.__offset += calcsize(fmt)
            i -= 1

    def buffer(self, buffer):
        self.__buffer = bytearray(buffer)
        (session, seq, msgcount) = unpack_from('>10sQh', self.__buffer)
        self.__process_msghdr(session, seq, msgcount)
        self.__offset = PAYLOAD_OFFSET

    def decode(self):
        if (self.__subscriber == None):
            return

        if (self.is_hb() == True):
            self.__subscriber.on_hb()
        elif (self.is_eos() == True):
            self.__subscriber.on_eos()
        else:
            self.__process_msgblks()

    def session(self):
        return self.__session

    def seq(self):
        return self.__seq

    def count(self):
        return self.__msgcount

    def is_hb(self):
        return self.__msgcount == HEART_BEAT

    def is_eos(self):
        return self.__msgcount == END_OF_SESSION
