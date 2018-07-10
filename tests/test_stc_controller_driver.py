#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import sys
import unittest
import logging

from cloudshell.traffic.tg_helper import get_reservation_resources, set_family_attribute
from shellfoundry.releasetools.test_helper import create_session_from_cloudshell_config, create_command_context

from src.driver import TestCenterControllerDriver

controller = 'localhost'
port = '8888'

ports = ['swisscom/Module1/PG2/Port3', 'swisscom/Module1/PG2/Port4']
attributes = {'Controller Address': controller,
              'Controller TCP Port': port}


class TestStcControllerDriver(unittest.TestCase):

    def setUp(self):
        self.session = create_session_from_cloudshell_config()
        self.context = create_command_context(self.session, ports, 'TestCenter Controller', attributes)
        self.driver = TestCenterControllerDriver()
        self.driver.initialize(self.context)
        print self.driver.logger.handlers[0].baseFilename
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().addHandler(logging.FileHandler(self.driver.logger.handlers[0].baseFilename))

    def tearDown(self):
        self.driver.cleanup()
        self.session.EndReservation(self.context.reservation.reservation_id)

    def test_init(self):
        pass

    def test_get_set(self):
        print('session_id = {}'.format(self.driver.get_session_id(self.context)))
        project = self.driver.get_children(self.context, 'system1', 'project')[0]
        print('project = {}'.format(project))
        print('all children = {}'.format(self.driver.get_children(self.context, 'system1')))

    def test_load_config(self):
        reservation_ports = get_reservation_resources(self.session, self.context.reservation.reservation_id,
                                                      'Generic Traffic Generator Port',
                                                      'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorPort',
                                                      'STC Chassis Shell 2G.GenericTrafficGeneratorPort')
        set_family_attribute(self.session, reservation_ports[0], 'Logical Name', 'Port 1')
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', 'Port 2')
        self.driver.load_config(self.context, path.join(path.dirname(__file__), 'test_config.tcc'))

    def test_run_traffic(self):
        self.test_load_config()
        self.driver.send_arp(self.context)
        self.driver.start_traffic(self.context, 'False')
        self.driver.stop_traffic(self.context)
        stats = self.driver.get_statistics(self.context, 'generatorportresults', 'JSON')
        assert(int(stats['Port 1']['TotalFrameCount']) <= 4000)
        self.driver.start_traffic(self.context, 'True')
        stats = self.driver.get_statistics(self.context, 'generatorportresults', 'JSON')
        assert(int(stats['Port 1']['TotalFrameCount']) == 4000)
        stats = self.driver.get_statistics(self.context, 'generatorportresults', 'csv')
        print stats

    def negative_tests(self):
        reservation_ports = get_reservation_resources(self.session, self.context.reservation.reservation_id,
                                                      'Generic Traffic Generator Port',
                                                      'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorPort',
                                                      'STC Chassis Shell 2G.GenericTrafficGeneratorPort')
        assert(len(reservation_ports) == 2)
        set_family_attribute(self.session, reservation_ports[0], 'Logical Name', 'Port 1')
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', '')
        self.assertRaises(Exception, self.driver.load_config, self.context,
                          path.join(path.dirname(__file__), 'test_config.tcc'))
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', 'Port 1')
        self.assertRaises(Exception, self.driver.load_config, self.context,
                          path.join(path.dirname(__file__), 'test_config.tcc'))
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', 'Port x')
        self.assertRaises(Exception, self.driver.load_config, self.context,
                          path.join(path.dirname(__file__), 'test_config.tcc'))
        # cleanup
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', 'Port 2')

    def test_run_sequencer(self):
        reservation_ports = get_reservation_resources(self.session, self.context.reservation.reservation_id,
                                                      'Generic Traffic Generator Port',
                                                      'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorPort',
                                                      'STC Chassis Shell 2G.GenericTrafficGeneratorPort')
        set_family_attribute(self.session, reservation_ports[0], 'Logical Name', 'Port 1')
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', 'Port 2')
        self.driver.load_config(self.context, path.join(path.dirname(__file__), 'test_sequencer.tcc'))
        self.driver.sequencer_command(self.context, 'Start')
        self.driver.sequencer_command(self.context, 'Wait')


if __name__ == '__main__':
    sys.exit(unittest.main())
