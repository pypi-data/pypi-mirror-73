#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
#
from client.TalosClientConfig import TalosClientConfig
from thrift.auth.ttypes import Credential
from thrift.topic.ttypes import TopicAndPartition
from consumer.TalosConsumer import TalosConsumer
from consumer.MessageProcessor import MessageProcessor
from consumer.MessageProcessorFactory import MessageProcessorFactory
from thrift.auth.ttypes import UserType
from atomic import AtomicLong
import logging


logger = logging.getLogger("TalosConsumerDemo")
successGetNumber = AtomicLong(0)


# callback for consumer to process messages, that is, consuming logic
class MyMessageProcessor(MessageProcessor):
    topicAndPartition = TopicAndPartition
    messageOffset = int

    def init(self, topicAndPartition=None, messageOffset=None):
        self.topicAndPartition = topicAndPartition
        self.messageOffset = messageOffset

    def process(self, messages=None, messageCheckPointer=None):
        try:
            # add your process logic for 'messages
            for messageAndOffset in messages:
                logger.info("Message content: " + messageAndOffset.message.message)
                print("Message content: " + messageAndOffset.message.message)
            successGetNumber.get_and_set(successGetNumber.value + len(messages))
            count = successGetNumber.value
            logger.info("Consuming total data so far: " + str(count))
            print("Consuming total data so far: " + str(count))

            # if user has set 'galaxy.talos.consumer.checkpoint.auto.commit' to false,
            # then you can call the 'checkpoint' to commit the list of messages.
            # messageCheckPointer.check_point()

        except Exception as e:
            logger.error("process error, " + e.message)

    def shutdown(self, messageCheckpointer=None):
        pass


# using for thread-safe when processing different partition data
class MyMessageProcessorFactory(MessageProcessorFactory):

    def create_processor(self):
        return MyMessageProcessor()


class TalosConsumerDemo():
    accessKey = "$yourAccessKey"
    accessSecret = "$yourSecretKey"
    topicName = "$yourTopicName"
    consumerGroup = "$yourConsumerGroup"
    clientPrefix = "$yourDepartmentName"

    pro = dict()
    pro["galaxy.talos.service.endpoint"] = "$yourEndpoint"
    consumerConfig = TalosClientConfig
    credential = Credential

    talosConsumer = TalosConsumer

    def __init__(self):
        self.consumerConfig = TalosClientConfig(self.pro)
        # credential
        self.credential = Credential(UserType.DEV_XIAOMI,
                                     self.accessKey,
                                     self.accessSecret)

    def start(self):
        self.talosConsumer = TalosConsumer(consumerGroup=self.consumerGroup,
                                           consumerConfig=self.consumerConfig,
                                           credential=self.credential,
                                           topicName=self.topicName,
                                           messageProcessorFactory=
                                           MyMessageProcessorFactory(),
                                           clientPrefix=self.clientPrefix)


consumerDemo = TalosConsumerDemo()
consumerDemo.start()

