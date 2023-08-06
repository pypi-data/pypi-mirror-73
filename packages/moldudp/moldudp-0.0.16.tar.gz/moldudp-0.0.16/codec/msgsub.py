# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# Message subscriber interface
#
class MsgSubscriber:

    # on heart beat
    def on_hb(self):
        pass

    # on end of session
    def on_eos(self):
        pass

    # on message block received
    def on_msgblk(self, msg):
        pass
