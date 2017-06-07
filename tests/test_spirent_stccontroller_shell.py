#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterControllerDriver`
"""

import os
import unittest

from cloudshell.api.cloudshell_api import CloudShellAPISession

from driver import TestCenterControllerDriver
import tg_helper

client_install_path = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.71'


class TestTestCenterControllerDriver(unittest.TestCase):

    def setUp(self):
        self.session = CloudShellAPISession('localhost', 'admin', 'admin', 'Global')
        self.context = tg_helper.create_context(self.session, 'stc test', 'TestCenter Controller', client_install_path)
        self.driver = TestCenterControllerDriver()
        self.driver.initialize(self.context)

    def tearDown(self):
        self.driver.cleanup()
        self.session.EndReservation(self.context.reservation.reservation_id)
        self.session.TerminateReservation(self.context.reservation.reservation_id)

    def test_init(self):
        pass

    def test_load_config(self):
        reservation_ports = tg_helper.get_reservation_ports(self.session, self.context.reservation.reservation_id)
        self.session.SetAttributeValue(reservation_ports[0].Name, 'Logical Name', 'Port 1')
        self.session.SetAttributeValue(reservation_ports[1].Name, 'Logical Name', 'Port 2')
        self.driver.load_config(self.context, os.path.dirname(__file__).replace('\\', '/') + '/test_config.tcc')

    def test_reload_config(self):
        self.test_load_config()
        self.driver.load_config(self.context, os.path.dirname(__file__).replace('\\', '/') + '/test_config.tcc')


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
