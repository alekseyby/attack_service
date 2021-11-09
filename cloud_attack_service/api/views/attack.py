from rest_framework import views
from rest_framework.request import Request
from rest_framework import response
from rest_framework import status
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.permissions import AllowAny

from cloud.services.cloud_relation_manager import CloudRelationManager
from cloud.services.daos import VirtualMachineDAO


class AttackViewParamsSerializer(serializers.Serializer):
    vm_id = serializers.CharField(required=True, )

    def validate_vm_id(self, value):
        if not VirtualMachineDAO.is_machine_exists(value):
            raise ValidationError('vm not found')
        return value


class AttackView(views.APIView):
    params_serializer_class = AttackViewParamsSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> response.Response:
        params_serializer = AttackViewParamsSerializer(data=request.query_params)
        if params_serializer.is_valid():
            machine = params_serializer.data['vm_id']
            attackers = CloudRelationManager().get_machines_who_can_possible_access_the_vm_by_vm_id(machine)
            return response.Response(status=status.HTTP_200_OK, data=attackers)
        return response.Response(status=status.HTTP_400_BAD_REQUEST, data=params_serializer.errors)
