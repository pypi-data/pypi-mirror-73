# -*- coding:utf8 -*-
#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

from client.TalosClientConfig import TalosClientConfig
from client.compression.Compression import Compression
from client.TalosClientFactory import TalosClientFactory
from thrift.topic.ttypes import TopicAndPartition
from thrift.topic.TopicService import GetDescribeInfoRequest
from thrift.topic.TopicService import GetDescribeInfoResponse
from thrift.message import MessageService
from thrift.message.ttypes import Message
from thrift.message.ttypes import MessageType
from thrift.message.ttypes import PutMessageRequest
from atomic import AtomicLong
from utils import Utils
import logging


class SimpleProducer(object):
    logger = logging.getLogger("SimpleConsumer")

    producerConfig = TalosClientConfig
    topicAndPartition = TopicAndPartition
    messageClient = MessageService.Iface
    requestId = AtomicLong
    clientId = str
    isActive = bool

    def __init__(self, producerConfig=None, topicName=None, partitionId=None, credential=None):
        Utils.check_topic_name(topicName)
        talosClientFactory = TalosClientFactory(producerConfig, credential)
        self.get_topic_info(talosClientFactory.new_topic_client(), topicName, partitionId)
        self.producerConfig = producerConfig
        self.messageClient = talosClientFactory.new_message_client()
        self.clientId = Utils.generate_client_id('SimpleProducer')
        self.requestId = AtomicLong(1)
        self.isActive = True

    def get_topic_info(self, topicClient=None, topicName=None, partitionId=None):
        response = topicClient.getDescribeInfo(GetDescribeInfoRequest(topicName))
        self.topicAndPartition = TopicAndPartition(topicName=topicName,
                                                   topicTalosResourceName=response.topicTalosResourceName,
                                                   partitionId=partitionId)

    def put_message(self, msgList=None):
        if (not msgList) or len(msgList) == 0:
            return True

        try:
            self.put_message_list(msgList)
            return True
        except Exception as e:
            self.logger.error("putMessage error， please try to put again", e)

        return False

    def put_message_list(self, msgList=None):
        if (not msgList) or len(msgList) == 0:
            return

        # check data validity
        for message in msgList:
            # set timestamp and messageType if not set
            Utils.update_message(message, MessageType.BINARY)

        # check data validity
        Utils.check_message_list_validity(msgList)

        self._do_put(msgList)

    def _do_put(self, msgList=None):
        messageBlock = self._compress_message_list(msgList)
        messageBlockList = [messageBlock]

        requestSequenceId = Utils.generate_request_sequence_id(self.clientId, self.requestId)
        putMessageRequest = PutMessageRequest(self.topicAndPartition, messageBlockList, len(msgList), requestSequenceId)
        try:
            putMessageResponse = self.messageClient.put_message(putMessageRequest)
        except Exception as e:
            self.logger.error("put message request failed." + e.message)

    def _compress_message_list(self, msgList=None):
        return Compression.compress(msgList, self.producerConfig.get_compression_type())




