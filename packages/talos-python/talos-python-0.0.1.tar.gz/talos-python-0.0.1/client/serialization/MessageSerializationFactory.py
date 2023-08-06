#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

from client.serialization import MessageVersion
from client.serialization import MessageSerializerV1
from client.serialization import MessageSerializerV2
from client.serialization import MessageSerializerV3
from client.serialization import MessageSerializer
import logging


class MessageSerializationFactory:

    _messageSerializer = {
        "V1": MessageSerializerV1.MessageSerializerV1(),
        "V2": MessageSerializerV2.MessageSerializerV2(),
        "V3": MessageSerializerV3.MessageSerializerV3()
    }

    def get_default_message_version(self):
        return 'V3'

