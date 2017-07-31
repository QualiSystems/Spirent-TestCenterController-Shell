#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `TestCenterControllerDriver`
"""

import sys
import os
import logging
import unittest

from cloudshell.traffic import tg_helper

from driver import TestCenterControllerDriver

server = 'localhost'
blueprint = 'stc test'
blueprint = 'Brocade controller'
client_install_path = 'C:/Program Files (x86)/Spirent Communications/Spirent TestCenter 4.52'


class TestTestCenterControllerDriver(unittest.TestCase):

    def setUp(self):

        self.session = tg_helper.create_session_from_cloudshell_config()
        self.context = tg_helper.create_context(server, self.session, blueprint, 'TestCenter Controller',
                                                client_install_path)
        self.driver = TestCenterControllerDriver()
        self.driver.initialize(self.context)
        print self.driver.logger.handlers[0].baseFilename
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

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

    def test_run_traffic(self):
        self.test_load_config()
        self.driver.start_traffic(self.context, 'True')
        print self.driver.get_statistics(self.context, 'GeneratorPortResults', 'CSV')

    def test_devices(self):
        self.test_load_config()
        self.driver.send_arp(self.context)
        self.driver.start_devices(self.context)
        self.driver.stop_devices(self.context)
        self.driver.start_traffic(self.context, 'False')
        self.driver.stop_traffic(self.context)

    def test_reload_config(self):
        self.test_load_config()
        self.driver.load_config(self.context, os.path.dirname(__file__).replace('\\', '/') + '/test_config.tcc')


if __name__ == '__main__':
    sys.exit(unittest.main())
