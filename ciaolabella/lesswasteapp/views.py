from django.shortcuts import render
from pymongo import MongoClient
import pandas as pd
import logging
from datetime import datetime
from member.models import MEMBER
import json

def km_to_mile(km):
    mile = km * 0.621371
    return float(mile)

def get_points(collection, coords, distance):
    client = MongoClient("mongodb://127.0.0.1", 27017)
    db = client['multi_pjt3']
    coll = db[collection]
    dist = km_to_mile(distance) / 3963.2
    collection_list = []
    cursor = coll.find({
        'location': {
            '$geoWithin': {
                '$centerSphere': [coords, dist]
            }
        }
    }, {'_id': 0})
    for doc in cursor:
        data = dict()
        data['title'] = doc['name']
        data['latlng'] = [doc['location']['coordinates'][1], doc['location']['coordinates'][0]]
        collection_list.append(data)

    return collection_list

def map(request):
    lng = 126.912583627
    lat = 37.483568434
    zerowasteshop = get_points('zerowasteshop', [lng, lat], 10)
    recyclebox = get_points('recyclebox', [lng, lat], 10)
    center = [lat, lng]
    if request.method == 'GET':
        try:
            # 로그 수집
            rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            login_logger = logging.getLogger('log')
            data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                    'log_tm':str(datetime.now()), 'log_kb': 'lesswaste'}
            login_logger.info('menu_log', extra = data)
            return render(request, 'lesswasteapp/lesswaste.html', 
                {'center': center, 'zerowasteshop': zerowasteshop, 'recyclebox': recyclebox})

        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)
    
    else:
        try:
            lat = float(request.POST['userLat'].strip())
            lng = float(request.POST['userLng'].strip())
            center = [lat, lng]
            zerowasteshop = get_points('zerowasteshop', [lng, lat], 10)
            recyclebox = get_points('recyclebox', [lng, lat], 10)
            return render(request, 'lesswasteapp/lesswaste.html', 
                {'center': center, 'zerowasteshop': zerowasteshop, 'recyclebox': recyclebox})
        except:
            return render(request, 'lesswasteapp/lesswaste.html', 
                {'center': center, 'zerowasteshop': zerowasteshop, 'recyclebox': recyclebox})

