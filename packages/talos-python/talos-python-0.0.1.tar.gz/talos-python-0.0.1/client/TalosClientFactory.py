#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

from client.TalosClientConfig import TalosClientConfig
from thrift.auth.ttypes import Credential
from thrift.common.ttypes import Version
from thrift.topic import TopicService
from thrift.message import MessageService
from thrift.consumer import ConsumerService
from client.TalosErrors import InvalidArgumentError
from client.Constants import Constants
from thrift.protocol.TCompactProtocol import TCompactProtocol
from client.TalosHttpClient import TalosHttpClient
import logging
import platform
import httplib


class ConsumerClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def renew(self, request=None):
        self.talosHttpClient.set_query_string("type=renew")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).renew(request)

    def lock_worker(self, request=None):
        self.talosHttpClient.set_query_string("type=lockWorker")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).lockWorker(request)

    def query_worker(self, request=None):
        self.talosHttpClient.set_query_string("type=queryWorker")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).queryWorker(request)

    def lock_partition(self, request=None):
        self.talosHttpClient.set_query_string("type=lockPartition")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).lockPartition(request)

    def unlock_partition(self, request=None):
        self.talosHttpClient.set_query_string("type=unlockPartition")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).unlockPartition(request)

    def query_offset(self, request=None):
        self.talosHttpClient.set_query_string("type=queryOffset")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).queryOffset(request)

    def update_offset(self, request=None):
        self.talosHttpClient.set_query_string("type=updateOffset")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).updateOffset(request)


class TopicClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def get_describe_info(self, request=None):
        self.talosHttpClient.set_query_string("type=getDescribeInfo")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).getDescribeInfo(request)


class MessageClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def get_message(self, request=None):
        self.talosHttpClient.set_query_string("type=getMessage")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).getMessage(request)

    def put_message(self, request=None):
        self.talosHttpClient.set_query_string("type=putMessage")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).putMessage(request)


class TalosClientFactory:
    logger = logging.getLogger("TalosClientFactory")
    _USER_AGENT_HEADER = "User-Agent"
    _SID = "galaxytalos"
    _DEFAULT_CLIENT_CONN_TIMEOUT = 5000

    _version = Version
    _talosClientConfig = TalosClientConfig
    _credential = Credential
    _customHeaders = dict
    _httpClient = httplib.HTTPConnection
    _agent = str
    _clockOffset = int

    def __init__(self, clientConfig=None, credential=None):
        self._talosClientConfig = clientConfig
        self._credential = credential
        self._customHeaders = None
        self._version = Version()
        self._clockOffset = 0

    def new_topic_client(self):
        headers = dict()
        headers[self._USER_AGENT_HEADER] = self.create_user_agent_header()
        if self._customHeaders:
            for k in self._customHeaders:
                headers[k] = self._customHeaders[k]
        # setting 'supportAccountKey' to true for using Galaxy-V3 auth
        talosHttpClient = TalosHttpClient(self._talosClientConfig.get_service_endpoint()
                                          + Constants.TALOS_TOPIC_SERVICE_PATH,
                                          self._credential, self._clockOffset, True)
        talosHttpClient.set_custom_headers(headers)
        talosHttpClient.set_timeout(self._talosClientConfig.get_client_conn_timeout())
        return TopicClient(talosHttpClient)

    def new_consumer_client(self):
        headers = dict()
        headers[self._USER_AGENT_HEADER] = self.create_user_agent_header()
        if self._customHeaders:
            for k in self._customHeaders:
                headers[k] = self._customHeaders[k]
        # setting 'supportAccountKey' to true for using Galaxy-V3 auth
        talosHttpClient = TalosHttpClient(self._talosClientConfig.get_service_endpoint()
                                          + Constants.TALOS_CONSUMER_SERVICE_PATH,
                                          self._credential, self._clockOffset, True)
        talosHttpClient.set_custom_headers(headers)
        talosHttpClient.set_timeout(self._talosClientConfig.get_client_conn_timeout())
        return ConsumerClient(talosHttpClient)

    def new_message_client(self):
        headers = dict()
        headers[self._USER_AGENT_HEADER] = self.create_user_agent_header()
        if self._customHeaders:
            for k in self._customHeaders:
                headers[k] = self._customHeaders[k]
        # setting 'supportAccountKey' to true for using Galaxy-V3 auth
        talosHttpClient = TalosHttpClient(self._talosClientConfig.get_service_endpoint()
                                          + Constants.TALOS_MESSAGE_SERVICE_PATH,
                                          self._credential, self._clockOffset, True)
        talosHttpClient.set_custom_headers(headers)
        talosHttpClient.set_timeout(self._talosClientConfig.get_client_conn_timeout())
        return MessageClient(talosHttpClient)

    def check_credential(self):
        if not self._credential:
            raise InvalidArgumentError("Credential is not set")

    def create_user_agent_header(self):
        return "Python-SDK/" + str(self._version.major) + "." + str(self._version.minor) + "." + str(self._version.revision) + " Python/" + platform.python_version()


