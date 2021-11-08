from rest_framework import views
from rest_framework import response
from rest_framework import status
from cloud.services.daos import VirtualMachineDAO
from api.models import APIStat

from django.db.models import Avg


class ClodStatView(views.APIView):

    def get(self, request, *args, **kwargs):
        data = {
            'vm_count': VirtualMachineDAO.get_vms_count(),
            'request_count': APIStat.objects.count(),
            'average_request_time': APIStat.objects.all().aggregate(Avg('response_time'))['response_time__avg']
        }
        return response.Response(status=status.HTTP_200_OK, data=data)
