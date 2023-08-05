# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from admobilize.proto.devicemanagement.v1alpha2 import device_manager_pb2 as admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2
from admobilize.proto.devicemanagement.v1alpha2 import resources_pb2 as admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DeviceManagerStub(object):
    """The service that an application uses to create, update, delete, manipulate and obtain
    devices.

    [START device management service]
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateDevice = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/CreateDevice',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
                )
        self.GetDevice = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/GetDevice',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.GetDeviceRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
                )
        self.ListDevices = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/ListDevices',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListDevicesRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListDevicesResponse.FromString,
                )
        self.UpdateDevice = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/UpdateDevice',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.UpdateDeviceRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
                )
        self.DeleteDevice = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/DeleteDevice',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.DeleteDeviceRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.InstallApplication = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/InstallApplication',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.InstallApplicationRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
                )
        self.CreateProject = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/CreateProject',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
                )
        self.GetProject = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/GetProject',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.GetProjectRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
                )
        self.ListProjects = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/ListProjects',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListProjectsRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListProjectsResponse.FromString,
                )
        self.UpdateProject = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/UpdateProject',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.UpdateProjectRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
                )
        self.DeleteProject = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/DeleteProject',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.DeleteProjectRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.BatchCreateDevices = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/BatchCreateDevices',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.BatchCreateDevicesRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.BatchCreateDevicesResponse.FromString,
                )
        self.ProvisionDevices = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/ProvisionDevices',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ProvisionDevicesRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ProvisionDevicesResponse.FromString,
                )
        self.VerifyDeviceToken = channel.unary_unary(
                '/admobilize.devicemanagement.v1alpha2.DeviceManager/VerifyDeviceToken',
                request_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.VerifyDeviceTokenRequest.SerializeToString,
                response_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
                )


class DeviceManagerServicer(object):
    """The service that an application uses to create, update, delete, manipulate and obtain
    devices.

    [START device management service]
    """

    def CreateDevice(self, request, context):
        """--- Standard methods -----------------------------------------------------------

        Creates a device
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDevice(self, request, context):
        """Gets a device
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListDevices(self, request, context):
        """Lists devices in a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDevice(self, request, context):
        """Updates a device
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDevice(self, request, context):
        """Deletes a device
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InstallApplication(self, request, context):
        """Application methods
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProject(self, request, context):
        """Creates a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProject(self, request, context):
        """Gets a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProjects(self, request, context):
        """List the projects to which the current authenticated user has access to
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProject(self, request, context):
        """Updates a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProject(self, request, context):
        """Deletes a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchCreateDevices(self, request, context):
        """--- Custom methods -----------------------------------------------------------

        Create many devices at once
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProvisionDevices(self, request, context):
        """Provision a device
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyDeviceToken(self, request, context):
        """Validates if a given token is a legitimate device token, this is
        the signature matches the registered public key
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeviceManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDevice,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
            ),
            'GetDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDevice,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.GetDeviceRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
            ),
            'ListDevices': grpc.unary_unary_rpc_method_handler(
                    servicer.ListDevices,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListDevicesRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListDevicesResponse.SerializeToString,
            ),
            'UpdateDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDevice,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.UpdateDeviceRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
            ),
            'DeleteDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDevice,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.DeleteDeviceRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'InstallApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.InstallApplication,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.InstallApplicationRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
            ),
            'CreateProject': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProject,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.SerializeToString,
            ),
            'GetProject': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProject,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.GetProjectRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.SerializeToString,
            ),
            'ListProjects': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProjects,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListProjectsRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListProjectsResponse.SerializeToString,
            ),
            'UpdateProject': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateProject,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.UpdateProjectRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.SerializeToString,
            ),
            'DeleteProject': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteProject,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.DeleteProjectRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'BatchCreateDevices': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchCreateDevices,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.BatchCreateDevicesRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.BatchCreateDevicesResponse.SerializeToString,
            ),
            'ProvisionDevices': grpc.unary_unary_rpc_method_handler(
                    servicer.ProvisionDevices,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ProvisionDevicesRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ProvisionDevicesResponse.SerializeToString,
            ),
            'VerifyDeviceToken': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyDeviceToken,
                    request_deserializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.VerifyDeviceTokenRequest.FromString,
                    response_serializer=admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'admobilize.devicemanagement.v1alpha2.DeviceManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DeviceManager(object):
    """The service that an application uses to create, update, delete, manipulate and obtain
    devices.

    [START device management service]
    """

    @staticmethod
    def CreateDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/CreateDevice',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/GetDevice',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.GetDeviceRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListDevices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/ListDevices',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListDevicesRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListDevicesResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/UpdateDevice',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.UpdateDeviceRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/DeleteDevice',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.DeleteDeviceRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InstallApplication(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/InstallApplication',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.InstallApplicationRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/CreateProject',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/GetProject',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.GetProjectRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListProjects(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/ListProjects',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListProjectsRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ListProjectsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/UpdateProject',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.UpdateProjectRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Project.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/DeleteProject',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.DeleteProjectRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchCreateDevices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/BatchCreateDevices',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.BatchCreateDevicesRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.BatchCreateDevicesResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ProvisionDevices(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/ProvisionDevices',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ProvisionDevicesRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.ProvisionDevicesResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VerifyDeviceToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/admobilize.devicemanagement.v1alpha2.DeviceManager/VerifyDeviceToken',
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_device__manager__pb2.VerifyDeviceTokenRequest.SerializeToString,
            admobilize_dot_devicemanagement_dot_v1alpha2_dot_resources__pb2.Device.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
