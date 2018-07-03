#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import sys
import unittest
import time
import json

from cloudshell.api.cloudshell_api import AttributeNameValue, InputNameValue
from cloudshell.traffic.tg_helper import get_reservation_resources, set_family_attribute
from shellfoundry.releasetools.test_helper import create_session_from_cloudshell_config, create_command_context

controller = '172.40.0.163'
port = '8888'

ports = ['158/Module1/PG1/Port1', '158/Module1/PG1/Port2']
attributes = [AttributeNameValue('Controller Address', controller),
              AttributeNameValue('Controller TCP Port', port)]


class TestStcControllerDriver(unittest.TestCase):

    def setUp(self):
        self.session = create_session_from_cloudshell_config()
        self.context = create_command_context(self.session, ports, 'TestCenter Controller', attributes)

    def tearDown(self):
        reservation_id = self.context.reservation.reservation_id
        self.session.EndReservation(reservation_id)
        while self.session.GetReservationDetails(reservation_id).ReservationDescription.Status != 'Completed':
            time.sleep(1)
        self.session.DeleteReservation(reservation_id)

    def test_session_id(self):
        session_id = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                                 'Service', 'get_session_id')
        print('session_id = {}'.format(session_id.Output))
        project = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                              'Service', 'get_children',
                                              [InputNameValue('obj_ref', 'system1'),
                                               InputNameValue('child_type', 'project')])
        print('project = {}'.format(project.Output))
        project_obj = json.loads(project.Output)[0]
        project_childs = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                                     'Service', 'get_children',
                                                     [InputNameValue('obj_ref', project_obj)])
        print('Project-Children = {}'.format(project_childs.Output))

        options = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                              'Service', 'get_children',
                                              [InputNameValue('obj_ref', 'system1'),
                                               InputNameValue('child_type', 'AutomationOptions')])
        print('AutomationOptions = {}'.format(options.Output))
        options_ref = json.loads(options.Output)[0]
        options_attrs = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                                    'Service', 'get_attributes',
                                                    [InputNameValue('obj_ref', options_ref)])
        print('AutomationOptions-Attributes = {}'.format(options_attrs.Output))

        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                    'Service', 'set_attribute',
                                    [InputNameValue('obj_ref', options_ref),
                                     InputNameValue('attr_name', 'LogLevel'),
                                     InputNameValue('attr_value', 'INFO')])
        options_attrs = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                                    'Service', 'get_attributes',
                                                    [InputNameValue('obj_ref', options_ref)])
        print('AutomationOptions-Attributes = {}'.format(options_attrs.Output))\

        parameters = {'Parent': project_obj,
                      'ResultParent': project_obj,
                      'ConfigType': 'Generator',
                      'ResultType': 'GeneratorPortResults'}

        options_attrs = self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller',
                                                    'Service', 'perform_command',
                                                    [InputNameValue('command', 'ResultsSubscribe'),
                                                     InputNameValue('parameters_json', json.dumps(parameters))])

    def test_load_config(self):
        self._load_config(path.join(path.dirname(__file__), 'test_config_840.ixncfg'))

    def test_run_traffic(self):
        self._load_config(path.join(path.dirname(__file__), 'test_config_840.ixncfg'))
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'send_arp')
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'send_arp')
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'start_protocols')
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'stop_protocols')
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'start_traffic', [InputNameValue('blocking', 'True')])
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'stop_traffic')
        stats = self.session.ExecuteCommand(self.context.reservation.reservation_id,
                                            'TestCenter Controller', 'Service', 'get_statistics',
                                            [InputNameValue('view_name', 'Port Statistics'),
                                             InputNameValue('output_type', 'JSON')])
        assert(int(json.loads(stats.Output)['Port 1']['Frames Tx.']) >= 1600)

    def test_run_quick_test(self):
        self._load_config(path.join(path.dirname(__file__), 'quick_tests_840.ixncfg'))
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'run_quick_test', [InputNameValue('test', 'QuickTest3')])

    def _load_config(self, config):
        reservation_ports = get_reservation_resources(self.session, self.context.reservation.reservation_id,
                                                      'Generic Traffic Generator Port',
                                                      'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorPort',
                                                      'STC Chassis Shell 2G.GenericTrafficGeneratorPort')
        set_family_attribute(self.session, reservation_ports[0], 'Logical Name', 'Port 1')
        set_family_attribute(self.session, reservation_ports[1], 'Logical Name', 'Port 2')
        self.session.ExecuteCommand(self.context.reservation.reservation_id, 'TestCenter Controller', 'Service',
                                    'load_config', [InputNameValue('ixn_config_file_name', config)])


if __name__ == '__main__':
    sys.exit(unittest.main())
