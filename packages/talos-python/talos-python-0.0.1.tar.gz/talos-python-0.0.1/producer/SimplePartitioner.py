#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

import sys
from utils.Utils import HashCode
from producer import Partitioner


class SimplePartitioner(Partitioner):

    def partition(self, partitionKey=None, partitionNum=None):
        partitionInterval = sys.maxsize / partitionNum
        return ((HashCode.HashCode(partitionKey) & 0x7FFFFFFF) / partitionInterval) % partitionNum