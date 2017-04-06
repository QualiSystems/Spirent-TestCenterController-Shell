#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterControllerDriver`
"""

import unittest

from cloudshell.shell.core.driver_context import (ConnectivityContext, ResourceContextDetails, InitCommandContext)
from src.stc_handler import StcHandler


class TestTestCenterControllerDriver(unittest.TestCase):

    def setUp(self):
        self.connectivity = ConnectivityContext(None, None, None, None)
        self.resource = ResourceContextDetails(None, None, None, None, None, None, None, None, None, None)
        self.resource.address = 'localhost'
        self.resource.attributes = {'Client Install Path':
                                    'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.70'}
        context = InitCommandContext(self.connectivity, self.resource)
        self.handler = StcHandler()
        self.handler.initialize(context)

    def tearDown(self):
        pass


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
