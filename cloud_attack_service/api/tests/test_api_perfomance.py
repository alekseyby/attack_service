import os
import time
from django.test import TestCase
from django.test import Client
from cloud.services.cloud_relation_manager import CloudRelationManager
from concurrent.futures import ThreadPoolExecutor
from api.tests.helpers.test_helpers import ATTACK_URL, STATS_URL
from cloud.services.usecases import LoadInfrastructureUsecase

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PATH = DIR_PATH + f'/data_inputs/input-3.json'
WORKERS = 100


class PerformanceApiTest(TestCase):

    """
    Sent requests in threads against GET/attack endpoint.
    PATH - path to json with vms and routing rules
    Test works for local environment in scope of pytest test.
    """

    def test_performance_api(self):
        list_of_urls = []
        LoadInfrastructureUsecase(is_delete_old=True).execute(PATH)
        all_vms = CloudRelationManager().get_all_vms()
        client = Client()
        for vm in all_vms:
            vm_id = vm.get('vm_id')
            list_of_urls.append(ATTACK_URL + f'?vm_id={vm_id}')

        threaded_start = time.time()
        threads = []
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            for url in list_of_urls:
                threads.append(executor.submit(client.get(url)))

        response = client.get(STATS_URL)
        assert response.status_code == 200
        print(response.json())
        print("Threaded time:", time.time() - threaded_start)
