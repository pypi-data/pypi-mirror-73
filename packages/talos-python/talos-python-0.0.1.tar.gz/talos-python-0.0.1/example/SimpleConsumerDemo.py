#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
#

from client.TalosClientConfig import TalosClientConfig
from thrift.auth.ttypes import Credential
from thrift.auth.ttypes import UserType
from consumer.SimpleConsumer import SimpleConsumer
import time
import logging


class SimpleConsumerDemo:
    logging.basicConfig()
    logger = logging.getLogger("SimpleConsumerDemo")
    accessKey = "$yourAccessKey"
    accessSecret = "$yourSecretKey"
    topicName = "$yourTopicName"
    partitionId = 0

    pro = dict()
    pro["galaxy.talos.service.endpoint"] = "$yourEndPoint"
    clientConfig = TalosClientConfig
    credential = Credential

    simpleConsumer = SimpleConsumer

    def __init__(self):
        self.clientConfig = TalosClientConfig(self.pro)
        # credential
        self.credential = Credential(UserType.DEV_XIAOMI, self.accessKey, self.accessSecret)

    def start(self):
        # init consumer
        self.simpleConsumer = SimpleConsumer(clientConfig=self.clientConfig, topicName=self.topicName, partitionId=self.partitionId, credential=self.credential)
        finishedOffset = -1
        maxFetchNum = 5

        # a toy demo for getting messages to Talos server continuously
        # by using a infinite loop
        while True:
            try:
                messageList = self.simpleConsumer.fetch_message(finishedOffset + 1, maxFetchNum)
                i = 0
                while i < len(messageList):
                    print("message content is: " + str(messageList[i].message.message))
                    i += 1
                time.sleep(2)
            except Exception as e:
                self.logger.error("get message failed, try again." + e.message)
                continue
            if len(messageList) == 0:
                continue
            finishedOffset = messageList[len(messageList) - 1].messageOffset
            print("success get message count: " + str(len(messageList)))
            self.logger.info("success get message count: " + str(len(messageList)))


simpleConsumerDemo = SimpleConsumerDemo()
simpleConsumerDemo.start()
