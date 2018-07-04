
import json
import csv
import io
from collections import OrderedDict
import logging

from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.traffic.tg_helper import (get_reservation_resources, get_address, is_blocking, attach_stats_csv,
                                          get_family_attribute)

from trafficgenerator.tgn_utils import ApiType
from testcenter.stc_app import init_stc, StcSequencerOperation
from testcenter.stc_statistics_view import StcStats


class StcHandler(object):

    def initialize(self, context, logger):

        self.logger = logger
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().addHandler(logging.FileHandler(self.logger.handlers[0].baseFilename))

        controller = context.resource.attributes['Controller Address']
        port = context.resource.attributes['Controller TCP Port']
        port = int(port) if port else 8888
        self.stc = init_stc(ApiType.rest, self.logger, rest_server=controller, rest_port=port)
        self.stc.connect()

    def tearDown(self):
        self.stc.disconnect()

    def load_config(self, context, stc_config_file_name):
        """
        :param stc_config_file_name: full path to STC configuration file (tcc or xml)
        """

        self.stc.load_config(stc_config_file_name)
        config_ports = self.stc.project.get_ports()

        reservation_id = context.reservation.reservation_id
        my_api = CloudShellSessionContext(context).get_api()

        reservation_ports = {}
        for port in get_reservation_resources(my_api, reservation_id,
                                              'Generic Traffic Generator Port',
                                              'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorPort',
                                              'STC Chassis Shell 2G.GenericTrafficGeneratorPort'):
            reservation_ports[get_family_attribute(my_api, port, 'Logical Name').Value.strip()] = port

        for name, port in config_ports.items():
            if name in reservation_ports:
                address = get_address(reservation_ports[name])
                self.logger.debug('Logical Port {} will be reserved on Physical location {}'.format(name, address))
                port.reserve(address, force=True, wait_for_up=False)
            else:
                self.logger.error('Configuration port "{}" not found in reservation ports {}'.
                                  format(port, reservation_ports.keys()))
                raise Exception('Configuration port "{}" not found in reservation ports {}'.
                                format(port, reservation_ports.keys()))

        self.logger.info("Port Reservation Completed")

    def send_arp(self):
        self.stc.send_arp_ns()

    def start_devices(self):
        self.stc.start_devices()

    def stop_devices(self):
        self.stc.stop_devices()

    def start_traffic(self, blocking):
        self.stc.clear_results()
        self.stc.start_traffic(is_blocking(blocking))

    def stop_traffic(self):
        self.stc.stop_traffic()

    def get_statistics(self, context, view_name, output_type):

        stats_obj = StcStats(self.stc.project, view_name)
        stats_obj.read_stats()
        statistics_ = stats_obj.statistics

        if output_type.strip().lower() == 'json':
            statistics_str = json.dumps(statistics_, indent=4, sort_keys=True, ensure_ascii=False)
            return json.loads(statistics_str)
        elif output_type.strip().lower() == 'csv':
            statistics = OrderedDict()
            for obj_name in statistics_['topLevelName']:
                statistics[obj_name] = stats_obj.get_object_stats(obj_name)
            captions = statistics[statistics_['topLevelName'][0]].keys()
            output = io.BytesIO()
            w = csv.DictWriter(output, captions)
            w.writeheader()
            for obj_name in statistics:
                w.writerow(statistics[obj_name])
            attach_stats_csv(context, self.logger, view_name, output.getvalue().strip())
            return output.getvalue().strip()
        else:
            raise Exception('Output type should be CSV/JSON - got "{}"'.format(output_type))

    def sequencer_command(self, command):
        if StcSequencerOperation[command.lower()] == StcSequencerOperation.start:
            self.stc.clear_results()
        self.stc.sequencer_command(StcSequencerOperation[command.lower()])

    def get_session_id(self):
        return self.stc.api.session_id

    def get_children(self, obj_ref, child_type):
        children_attribute = 'children-' + child_type if child_type else 'children'
        return self.stc.api.ls.get(obj_ref, children_attribute).split()

    def get_attributes(self, obj_ref):
        return self.stc.api.ls.get(obj_ref)

    def set_attribute(self, obj_ref, attr_name, attr_value):
        return self.stc.api.ls.config(obj_ref, **{attr_name: attr_value})

    def perform_command(self, command, parameters_json):
        return self.stc.api.ls.perform(command, json.loads(parameters_json))
