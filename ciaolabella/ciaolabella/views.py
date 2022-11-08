from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
import logging
from datetime import datetime
from member.models import MEMBER,ECOPOINT
from . import ocr
import random
from pymongo import MongoClient
from PIL import Image
import gridfs
from bson.objectid import ObjectId
import codecs
from django.core.cache import cache

def index(request): # main

    try :
        # 회원 로그 수집
        # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
        # login_logger = logging.getLogger('log')
        # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
        #         'log_tm':str(datetime.now()), 'log_kb': 'main'}
        # login_logger.info('menu_log', extra = data)

        return render(request, 'ciaolabella/index.html')

    except KeyError:
        # 비회원인 경우, session에 row_id 없어서 key error 발생됨.
        '''
        request.session['user_id'] = ''

        # 비회원 로그 수집
        login_logger = logging.getLogger('log')
        data = {'user_id': request.session['user_id'], 'log_tm':datetime.now(), 'log_kb': 'main' }
        login_logger.info('menu_log', extra = data)
        '''

        return render(request, 'ciaolabella/index.html')


def about(request):
    try :
        # 회원 로그 수집
        # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
        # login_logger = logging.getLogger('log')
        # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
        #         'log_tm':str(datetime.now()), 'log_kb': 'about'}
        # login_logger.info('menu_log', extra = data)

        return render(request, 'ciaolabella/about.html')

    except KeyError:
        # 비회원
        return render(request, 'ciaolabella/about.html')


def aboutecopoint(request):
    if request.method == 'GET':
        try:
            # 로그 수집
            # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            # login_logger = logging.getLogger('log')
            # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
            #         'log_tm':str(datetime.now()), 'log_kb': 'aboutecopoint'}
            # login_logger.info('menu_log', extra = data)
            return render(request, 'ecopointapp/aboutecopoint.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)


def ecopoint(request):
    if request.method == 'GET':
            # 로그 수집

            # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            # login_logger = logging.getLogger('log')
            # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
            #         'log_tm':str(datetime.now()), 'log_kb': 'ecopoint'}
            # login_logger.info('menu_log', extra = data)
        try:
            # 로그 수집
            # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            # login_logger = logging.getLogger('log')
            # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
            #         'log_tm':str(datetime.now()), 'log_kb': 'ecopoint'}
            # login_logger.info('menu_log', extra = data)
            return render(request, 'ecopointapp/ecopoint.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)
        
    else:
        if "image" not in request.FILES:
            return redirect(request.url)
        image = request.FILES['image']
        member_id = request.session['member_id']

        # 사진 용량 제한
        if image.size > 16*2**20: # 16MB 초과
            message = '16MB이하의 사진만 업로드 가능합니다.'
            return JsonResponse({'msg': message})

        # 사진 메타데이터 인식 및 촬영 날짜 제한
        try:
            pic_time = Image.open(image)._getexif()[36867]
            if pic_time[:10] != datetime.now().strftime("%Y:%m:%d"):
                message = '오늘 촬영한 사진을 업로드해 주세요.'
                return JsonResponse({'msg': message})
        except:
            message = '사진 촬영시각이 확인되지 않습니다. 사진을 다시 촬영하여 업로드해 주세요.'
            return JsonResponse({'msg': message})

        # 사진 메타데이터로 하루 2번 제한 검증
        eco_cache = cache.get(f'{member_id}_1')
        if eco_cache and eco_cache[0] == datetime.now().strftime("%Y:%m:%d"):
            if eco_cache[1][0] == 1 and pic_time == eco_cache[1][1]:
                message = '이미 에코포인트를 적립받은 이미지 입니다.'
                return JsonResponse({'msg': message})
            elif eco_cache[1][0] > 1:
                message = '오늘은 더이상 등록하실 수 없습니다.'
                return JsonResponse({'msg': message})

        # image mongoDB에 저장
        client = MongoClient("mongodb://admin:qwer1234@218.154.53.236", 27721)
        db = client['rawimg']
        fs = gridfs.GridFS(db)
        file_id = fs.put(image.read(), member_id=member_id, pic_time=pic_time)
        #file_id = '63662953b4b738429945f671'

        # Flask와 통신하여 모델 적용
        data = {'file_id': str(file_id), 'member_id': member_id, 'pic_time': pic_time}
        url = 'http://3.35.17.248:8001/'
        try:
            resp = requests.post(url, data=data)
            result = resp.json() #json 문자열을 파이썬 객체로 변환
            modelfile_id = result['modelfile_id']
            result_list = result['result']
        except:
            message = '다른 사진을 업로드 해주세요.'
            return JsonResponse({'msg': message})

        # mongoDB에서 결과 이미지 로드
        db = client['ecopoint']
        fs = gridfs.GridFS(db)
        img_binary = fs.get(ObjectId(modelfile_id)).read()
        img_base64 = codecs.encode(img_binary, 'base64')
        decode_img = img_base64.decode('utf-8')

        # ecopoint
        plastic, label = 0, 0
        for i in result_list:
            if i['name'] == 'plastic' and i['confidence'] >= 0.5:
                plastic += 1
            elif i['name'] == 'label' and i['confidence'] >= 0.5:
                label += 1
        if plastic < 1:
            message = "플라스틱이 아닙니다!"
        elif plastic >= 1:
            if label >= 1:
                message = f"{label} 개의 불순물이 감지되었습니다. \n깨끗하게 씻어서 분리수거 해주세요!"
            else:
                count = 2 if cache.get(f'{member_id}_1') else 1
                ecopoint = plastic*10
                message = f'{plastic} 개를 깨끗하게 분리수거하셨네요! \n덕분에 지구가 시원해졌어요! \n{ecopoint} ECO POINT 가 적립되었습니다!'
                # 에코 포인트 적립
                month_kb = datetime.now().strftime('%Y-%m')
                user_ecopoint = ECOPOINT.objects.filter(month_kb=month_kb, member_id=member_id)
                if user_ecopoint.exists():
                    org_point = user_ecopoint.first().point_amt
                    user_ecopoint.update(
                        point_amt = org_point + ecopoint
                    )
                else:
                    ECOPOINT.objects.create(
                        member_id = member_id,
                        month_kb = month_kb,
                        point_amt = ecopoint
                    )

                eco_cache = [datetime.now().strftime("%Y:%m:%d"), count, pic_time]
                cache.set(f'{member_id}_1', eco_cache, 86400)  # 하루 동안 유지

        return JsonResponse({'msg': message, 'decode_img': decode_img})


def ecopoint2(request):
    if request.method == 'GET':
        try:
            # 로그 수집
            # rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            # login_logger = logging.getLogger('log')
            # data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
            #         'log_tm':str(datetime.now()), 'log_kb': 'ecopoint2'}
            # login_logger.info('menu_log', extra = data)
            return render(request, 'ecopointapp/ecopoint2.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)

    else:
        if "image" not in request.FILES:
            return redirect(request.url)

        member_id = request.session['member_id']

        # 하루 1번 제한
        eco_cache = cache.get(f'{member_id}_2')
        print(f'{member_id}_2', '캐시확인:', eco_cache)
        if eco_cache and eco_cache[0] == datetime.now().strftime("%Y:%m:%d"):
            message = '오늘은 이미 에코포인트를 적립받으셨습니다.'
            return JsonResponse({'msg': message})

        image = request.FILES['image']
        result = ocr.ecopointtwo(image)

        if ('무라벨'or'무라밸'or'라벨X'or'라밸X'or'라벨x'or'라밸X') in result:

            ecopoint = random.randrange(10, 51, 10)
            message = f"무라벨 제품을 구매하셨군요! \n{ecopoint} ECO POINT 가 적립되었습니다!"

            # 에코 포인트 적립
            month_kb = datetime.now().strftime('%Y-%m')
            user_ecopoint = ECOPOINT.objects.filter(month_kb=month_kb, member_id=member_id)
            if user_ecopoint.exists():
                org_point = user_ecopoint.first().point_amt
                user_ecopoint.update(
                    point_amt=org_point + ecopoint
                )
            else:
                ECOPOINT.objects.create(
                    member_id=member_id,
                    month_kb=month_kb,
                    point_amt=ecopoint
                )

            eco_cache = [datetime.now().strftime("%Y:%m:%d")]
            cache.set(f'{member_id}_2', eco_cache, 86400)  # 하루 동안 유지

        else:
            message = '무라벨 제품이 아닙니다'

        return JsonResponse({'msg': message})
