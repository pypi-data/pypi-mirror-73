# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# MoldUDP bytearray/packet encoder according to the specification from Nasdaq
# http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf
#
from struct import pack_into

from moldudp.msg.msgpub import MsgPublisher
from moldudp.codec.const import HEADER_SIZE
from moldudp.codec.const import MESSAGE_SIZE_FIELD_LEN
from moldudp.codec.const import MOLDPKT_SIZE
from moldudp.codec.const import PAYLOAD_OFFSET
from moldudp.codec.const import PAYLOAD_SIZE
from moldudp.codec.const import SESSION_OFFSET


class MoldUDPEncoder:

    # publisher is the message sender to the wire
    def __init__(self, publisher: MsgPublisher, debug=False):
        self.__offset = SESSION_OFFSET
        self.__publisher = publisher
        self.__debug = debug
        self.__msgblks = []
        self.__header = bytearray(HEADER_SIZE)
        self.__buffer = bytearray(PAYLOAD_SIZE)
        self.__packet = bytearray(MOLDPKT_SIZE)
        self.__left = PAYLOAD_SIZE
        self.__seq = 0
        self.__msgcount = 0

    def __encode(self):
        if (self.__publisher == None):
            return

        published = False
        # clear payload buffers
        self.__header[:] = b'\x00' * HEADER_SIZE
        self.__buffer[:] = b'\x00' * PAYLOAD_SIZE

        if (self.__debug == True):
            print("SEND HDR SESSION: {}".format(self.__session))
            print("SEND HDR SEQ:     {}".format(self.__seq))

        # encode payload until it can't fit
        self.__offset = 0
        remaining = PAYLOAD_SIZE
        while (len(self.__msgblks) > 0):
            # pop the message block from the beginning of queue
            msg = self.__msgblks.pop(0)
            sz = len(msg)
            if ((self.__offset + MESSAGE_SIZE_FIELD_LEN + sz) < remaining):
                pack_into('>H', self.__buffer, self.__offset, sz)
                self.__offset += MESSAGE_SIZE_FIELD_LEN
                fmt = ">{}s".format(sz)
                pack_into(fmt, self.__buffer, self.__offset, msg)
                self.__offset += sz
                self.__msgcount += 1
                published = False
            else:
                # can't fit into the buffer going out so
                # put the message block back to the front of queue
                self.__msgblks.insert(0, msg)
                # payload is filled, now send
                self.__send()
                published = True
                break
        # Flushing the last packet even it didn't fill up the buffer
        if ((published == False) and (self.__offset < remaining)):
            # now send
            self.__send()
            published = True
        self.__left = PAYLOAD_SIZE

    def __send(self):
        # update header with latest count
        pack_into('>10sQh', self.__header, 0,
                  self.__session, self.__seq, self.__msgcount)
        if (self.__debug == True):
            print("SEND MSG COUNT:   {}".format(self.__msgcount))
            print("SEND HDR: {}".format(self.__header))
        # combine header and payload to create mold packet
        self.__packet[:PAYLOAD_OFFSET] = self.__header
        self.__packet[PAYLOAD_OFFSET:] = self.__buffer
        self.__publisher.publish(self.__packet)
        self.__seq += self.__msgcount
        self.__offset = 0
        self.__msgcount = 0

    def session(self, session):
        self.__session = session

    def seq(self, seq):
        self.__seq = seq

    def msgcount(self):
        return len(self.__msgblks)

    def add_msg(self, msg):
        if (msg == None):
            return
        self.__msgblks.append(msg)
        self.__left -= len(msg)
        # force encode if buffer is filled
        if (self.__left < (MESSAGE_SIZE_FIELD_LEN + 1)):
            self.__encode()

    def process(self):
        while (self.msgcount() > 0):
            self.__encode()
