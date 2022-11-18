from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from django.http import JsonResponse
from ciaolabella.env_settings import ES_PORT
from ciaolog.loggers import UserClickMenu, UserSearchProduct, UserClickProduct
from datetime import datetime

def trans(hits):
    hits_list = []
    for hit in hits:
        hits_list.append(hit['_source'])
    return hits_list

def search(request):
    if request.method == 'GET':
        menuclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        UserClickMenu(request, 'nolabel', menuclick_time)
        return render(request, 'nolabelapp/nolabel.html')
    else:
        searchclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        keyword = request.POST['keyword']
        UserSearchProduct(request, keyword, searchclick_time)
        if not keyword:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'keyword param is missing'})
        es = Elasticsearch([ES_PORT])
        res = es.search(index='nolabel', 
                        query={"multi_match": {"query": keyword,
                                                "fields": ["title", "volume"]}}, 
                        size=30)
        hits = res['hits']['hits']
        hits_list = trans(hits)
        return JsonResponse({'list': hits_list})
def click(request):
    productclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    UserClickProduct(request, request.POST['product_name'], request.POST['product_volume'],
                     request.POST['product_unitprice'], productclick_time)
    return JsonResponse({'msg': 'success'})