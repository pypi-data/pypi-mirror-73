# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# MoldUDP bytearray/packet decoder according to the specification from Nasdaq
# http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf
#
from struct import unpack_from
from struct import calcsize

from moldudp.codec.const import END_OF_SESSION
from moldudp.codec.const import HEART_BEAT
from moldudp.codec.const import PAYLOAD_OFFSET
from moldudp.codec.const import SESSION_OFFSET
from moldudp.codec.const import MESSAGE_SIZE_FIELD_LEN
from moldudp.codec.msgsub import MsgSubscriber


class MoldUDPDecoder:

    # subscriber is the application message processor
    def __init__(self, subscriber: MsgSubscriber, debug=False):
        self._offset = SESSION_OFFSET
        self._subscriber = subscriber
        self._debug = debug

    def _process_msghdr(self, session, seq, msgcount):
        self._session = session
        self._seq = seq
        self._msgcount = msgcount
        if (self._debug == True):
            print("RECEIVED HDR SESSION: {}".format(self._session))
            print("RECEIVED HDR SEQ:     {}".format(self._seq))
            print("RECEIVED MSG COUNT:   {}".format(self._msgcount))

    def _process_msgblks(self):
        i = self._msgcount
        while (i > 0):
            # message block consists of 2-bytes message length and follows by message data with previously specified length
            blk_sz = unpack_from('>H', self._buffer, self._offset)[0]
            self._offset += MESSAGE_SIZE_FIELD_LEN
            fmt = '>{}s'.format(blk_sz)
            msg = unpack_from(fmt, self._buffer, self._offset)[0]
            if (self._subscriber):
                self._subscriber.on_msgblk(msg)
            self._offset += calcsize(fmt)
            i -= 1

    def buffer(self, buffer):
        self._buffer = bytearray(buffer)
        (session, seq, msgcount) = unpack_from('>10sQh', self._buffer)
        self._process_msghdr(session, seq, msgcount)
        self._offset = PAYLOAD_OFFSET

    def decode(self):
        if (self._subscriber == None):
            return

        if (self.is_hb() == True):
            self._subscriber.on_hb()
        elif (self.is_eos() == True):
            self._subscriber.on_eos()
        else:
            self._process_msgblks()

    def session(self):
        return self._session

    def seq(self):
        return self._seq

    def count(self):
        return self._msgcount

    def is_hb(self):
        return self._msgcount == HEART_BEAT

    def is_eos(self):
        return self._msgcount == END_OF_SESSION
