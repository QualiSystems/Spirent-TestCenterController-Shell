
from helper.rest_json_client import RestJsonClient


def create_quali_api_instance(context, logger):
    """
    Get needed attributes from context and create instance of QualiApiHelper
    :param context:
    :param logger:
    :return:
    """
    if hasattr(context, 'reservation') and context.reservation:
        domain = context.reservation.domain
    elif hasattr(context, 'remote_reservation') and context.remote_reservation:
        domain = context.remote_reservation.domain
    else:
        domain = None
    address = context.connectivity.server_address
    token = context.connectivity.admin_auth_token
    if token:
        instance = QualiAPIHelper(address, logger, token=token, domain=domain)
    else:
        instance = QualiAPIHelper(address, logger, username='admin', password='admin', domain=domain)
    return instance


class QualiAPIHelper(object):
    def __init__(self, server_name, logger, username=None, password=None, token=None, domain=None):
        self._server_name = server_name
        if ":" not in self._server_name:
            self._server_name += ":9000"
        self._domain = domain if domain else None
        self._logger = logger
        self._username = username
        self._password = password
        self._token = token
        self.__rest_client = RestJsonClient(self._server_name, False)

    def upload_file(self, reservation_id, file_stream, file_name):
        # self.remove_attached_files(reservation_id)
        self.attach_new_file(reservation_id, file_stream, file_name)

    def login(self):
        """
        Login
        :return:
        """
        uri = 'API/Auth/Login'
        if self._token:
            json_data = {'token': self._token, 'domain': self._domain}
        else:
            json_data = {'username': self._username, 'password': self._password, 'domain': self._domain}
        result = self.__rest_client.request_put(uri, json_data)
        self.__rest_client.session.headers.update(authorization="Basic {0}".format(result.replace('"', '')))

    def attach_new_file(self, reservation_id, file_data, file_name):
        file_to_upload = {'QualiPackage': file_data}
        data = {
            "reservationId": reservation_id,
            "saveFileAs": file_name,
            "overwriteIfExists": "true",
        }

        self.__rest_client.request_post_files('API/Package/AttachFileToReservation',
                                              data=data,
                                              files=file_to_upload)

    def get_attached_files(self, reservation_id):
        uri = 'API/Package/GetReservationAttachmentsDetails/{0}'.format(reservation_id)
        result = self.__rest_client.request_get(uri)
        return result['AllAttachments']

    def remove_attached_files(self, reservation_id):
        for file_name in self.get_attached_files(reservation_id):
            file_to_delete = {"reservationId": reservation_id,
                              "FileName": file_name
                              }
            self.__rest_client.request_post('API/Package/DeleteFileFromReservation', data=file_to_delete) or []
