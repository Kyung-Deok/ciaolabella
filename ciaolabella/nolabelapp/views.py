from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from django.http import JsonResponse
import logging
from datetime import datetime
from member.models import MEMBER

def trans(hits):
    hits_list = []
    for hit in hits:
        hits_list.append(hit['_source'])
    return hits_list

def search(request):
    if request.method == 'GET':
        try:
            # 로그 수집
            # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            # login_logger = logging.getLogger('log')
            # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
            #         'log_tm':str(datetime.now()), 'log_kb': 'nolabel'}
            # login_logger.info('menu_log', extra = data)
            return render(request, 'nolabelapp/nolabel.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)            
    else:
        keyword = request.POST['keyword']

        if not keyword:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'keyword param is missing'})

        print(keyword)
        es = Elasticsearch(['35.79.157.151:8960'])
        res = es.search(index='nolabel', 
                        query={"multi_match": {"query": keyword,
                                                "fields": ["title", "volume"]}}, 
                        size=30)
        hits = res['hits']['hits']
        hits_list = trans(hits)
        return JsonResponse({'list': hits_list})
