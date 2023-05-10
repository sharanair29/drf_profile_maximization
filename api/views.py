from django.shortcuts import render, redirect
from .models import Contracts
from .serializers import ContractsSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .algorithm import *
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
import time


@api_view(['POST'])
@csrf_exempt
def optimize(request):
    if request.method == 'POST':
        # start_time = time.time()

        # retrieve data via python script or postman

        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = list(JSONParser().parse(stream))

        serializer = ContractsSerializer(data=python_data, many=True)
        if serializer.is_valid():
            serializer.save()
            # get list of id primary key of saved contracts
            res_id = [sub['id'] for sub in serializer.data]
            # filter contracts by primary key of saved contracts
            contracts = Contracts.objects.filter(pk__in=res_id)
            contracts_list = []

            # create ContractName objects input for findMaxProfitContracts
            for i in contracts:
                profit = i.duration * i.price
                end = i.start + i.duration
                value = ContractName(i.id, i.start, end, profit)
                contracts_list.append(value)

            # get max profit contracts id
            output = findMaxProfitContracts(contracts_list)

            # get max profit contracts by id
            query_set = contracts.filter(pk__in=output)
            # get total income
            income = query_set.aggregate(Sum('price'))['price__sum']
            # get contract names
            contract_names = query_set.values_list('name', flat=True)
            # return json response

            # total = time.time() - start_time

            res = {"income": income, "path": contract_names}
            json_data = JSONRenderer().render(res)

            return HttpResponse(json_data, content_type='application/json')

        else:
            return HttpResponse(
                JSONRenderer().render(
                    serializer.errors),
                content_type='application/json')
