#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

import unittest

from thrift.message.ttypes import MessageAndOffset
from thrift.message.ttypes import Message
from thrift.consumer.ttypes import UpdateOffsetResponse
from thrift.consumer.ttypes import LockPartitionResponse
from thrift.consumer.ttypes import QueryOffsetResponse
from thrift.consumer.ttypes import QueryOffsetRequest
from thrift.consumer.ttypes import UpdateOffsetRequest
from thrift.consumer.ttypes import CheckPoint
from thrift.topic.ttypes import TopicTalosResourceName
from thrift.topic.ttypes import TopicAndPartition
from thrift.common.ttypes import GalaxyTalosException
from thrift.common.ttypes import ErrorCode
from consumer.SimpleConsumer import SimpleConsumer
from consumer.MessageReader import MessageReader
from consumer.TalosMessageReader import TalosMessageReader
from consumer.PartitionFetcher import PartitionFetcher
from consumer.MessageProcessor import MessageProcessor
from client.TalosClientFactory import ConsumerClient
from client.TalosClientFactory import MessageClient
from client.TalosClientFactory import TopicClient
from client.TalosClientConfig import TalosClientConfig
from client.TalosClientConfigkeys import TalosClientConfigKeys
from mock import Mock
import time


class test_SimpleConsumer(unittest.TestCase):
    topicName = "MyTopic"
    resourceName = "12345#MyTopic#34595fkdiso456i390"
    talosResourceName = TopicTalosResourceName(resourceName)
    partitionId = 7
    partitionNum = 10
    startOffset = 0
    topicAndPartition = TopicAndPartition
    producerConfig = TalosClientConfig
    consumerConfig = TalosClientConfig
    messageClientMock = MessageClient
    topicClientMock = TopicClient
    messageList = []
    messageAndOffsetList = []
    simpleConsumer = SimpleConsumer
