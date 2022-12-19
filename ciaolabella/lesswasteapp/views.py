from django.shortcuts import render
from pymongo import MongoClient
from datetime import datetime
from ciaolog.loggers import UserClickMenu, UserSearchLesswaste
from ciaolabella.env_settings import MONGO_URL, MONGO_PORT

def km_to_mile(km):
    mile = km * 0.621371
    return float(mile)

def get_points(collection, coords, distance):
    client = MongoClient(MONGO_URL, MONGO_PORT)
    db = client['lesswaste']
    coll = db[collection]
    dist = km_to_mile(distance) / 3963.2
    collection_list = []
    cursor = coll.find({
        'location': {
            '$geoWithin': {
                '$centerSphere': [coords, dist]
            }
        }
    })
    for doc in cursor:
        data = dict()
        if collection == 'zerowasteshop':
            data['title'] = doc['store_nm']
        else:
            data['title'] = doc['box_nm']
        data['latlng'] = [doc['location']['coordinates'][1], doc['location']['coordinates'][0]]
        collection_list.append(data)
    return collection_list

def map(request):
    lng, lat = 126.912583627, 37.483568434
    zerowasteshop = get_points('zerowasteshop', [lng, lat], 10)
    recyclebox = get_points('recyclebox', [lng, lat], 10)
    center = [lat, lng]

    if request.method == 'GET':
        menuclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        UserClickMenu(request, 'lesswaste', menuclick_time)
        return render(request, 'lesswasteapp/lesswaste.html',
            {'center': center, 'zerowasteshop': zerowasteshop, 'recyclebox': recyclebox})
    else:
        searchclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            lat = float(request.POST['userLat'].strip())
            lng = float(request.POST['userLng'].strip())
            radius_km = int(request.POST['radius'])
            center = [lat, lng]
            zerowasteshop = get_points('zerowasteshop', [lng, lat], radius_km)
            recyclebox = get_points('recyclebox', [lng, lat], radius_km)
            UserSearchLesswaste(request, radius_km, center, searchclick_time)
            return render(request, 'lesswasteapp/lesswaste.html', 
                {'center': center, 'zerowasteshop': zerowasteshop, 'recyclebox': recyclebox})
        except:
            return render(request, 'lesswasteapp/lesswaste.html', 
                {'center': center, 'zerowasteshop': zerowasteshop, 'recyclebox': recyclebox})

