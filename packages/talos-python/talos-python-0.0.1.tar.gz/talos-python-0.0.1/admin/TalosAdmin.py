#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
#
from thrift.auth.ttypes import Credential
from client.TalosClientFactory import MessageClient
from client.TalosClientFactory import ConsumerClient
from client.TalosClientFactory import TopicClient
import logging


class TalosAdmin(object):
    logger = logging.getLogger("TalosAdmin")
    topicClient = TopicClient
    messageClient = MessageClient
    consumerClient = ConsumerClient
    credential = Credential()

    def __init__(self, talosClientFactory=None):
        self.topicClient = talosClientFactory.new_topic_client()

    # topicAttribute for partitionNumber required

    def get_describe_info(self, request=None):
        return self.topicClient.get_describe_info(request)

