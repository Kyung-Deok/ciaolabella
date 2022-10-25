from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
import logging
from datetime import datetime
from member.models import MEMBER,ECOPOINT
from . import ocr
import random

def index(request): # main

    try :
        # 회원 로그 수집
        rs = MEMBER.objects.filter(id=request.session['row_id']).first()
        login_logger = logging.getLogger('log')
        data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                'log_tm':str(datetime.now()), 'log_kb': 'main'}
        login_logger.info('menu_log', extra = data)

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
        rs = MEMBER.objects.filter(id=request.session['row_id']).first()
        login_logger = logging.getLogger('log')
        data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                'log_tm':str(datetime.now()), 'log_kb': 'about'}
        login_logger.info('menu_log', extra = data)

        return render(request, 'ciaolabella/about.html')

    except KeyError:
        # 비회원
        return render(request, 'ciaolabella/about.html')


def aboutecopoint(request):
    if request.method == 'GET':
        try:
            # 로그 수집
            rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            login_logger = logging.getLogger('log')
            data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                    'log_tm':str(datetime.now()), 'log_kb': 'aboutecopoint'}
            login_logger.info('menu_log', extra = data)
            return render(request, 'ecopointapp/aboutecopoint.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)


def ecopoint(request):
    if request.method == 'GET':
        try:
            # 로그 수집
            rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            login_logger = logging.getLogger('log')
            data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                    'log_tm':str(datetime.now()), 'log_kb': 'ecopoint'}
            login_logger.info('menu_log', extra = data)
            return render(request, 'ecopointapp/ecopoint.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)
        
    else:
        if "image" not in request.FILES:
            return redirect(request.url)
        image = request.FILES['image']

        # apply image to model
        upload = {'image': image}
        url = 'http://0.0.0.0:8001/'
        resp = requests.post(url, files=upload)
        result = resp.json() #json 문자열을 파이썬 객체로 변환
        
        # ecopoint
        result_list = result['result']
        plastic = 0
        label = 0
        if result_list:
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
                    ecopoint = plastic
                    total_ecopoint = ecopoint*10
                    message = f'{plastic} 개를 깨끗하게 분리수거하셨네요! \n덕분에 지구가 시원해졌어요! \n{total_ecopoint} ECO POINT 가 적립되었습니다!'
                    # 에코 포인트 적립
                        # "ECOPOINT.user_nb" must be a "MEMBER" instance.
                    ECOPOINT.objects.create(
                        user_nb=MEMBER.objects.get(id=request.session['row_id']), save_tm = datetime.now(), point_amt=total_ecopoint
                    )
        else:
            message = '다른 사진을 선택해 주세요.'
        # print(message)
        return JsonResponse({'msg': message})


def ecopoint2(request):
    if request.method == 'GET':
        try:
            # 로그 수집
            rs = MEMBER.objects.filter(id=request.session['row_id']).first()
            login_logger = logging.getLogger('log')
            data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                    'log_tm':str(datetime.now()), 'log_kb': 'ecopoint2'}
            login_logger.info('menu_log', extra = data)
            return render(request, 'ecopointapp/ecopoint2.html')
        except KeyError:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)

    else:
        if "image" not in request.FILES:
            return redirect(request.url)

        image = request.FILES['image']
                
        results = ocr.ecopointtwo(image)

        result = results['images'][0]['fields']
        list = []
        for i in result:
            list.append(i['inferText'])
        
        if ('무라벨'or'무라밸'or'라벨X') in list:

            total_ecopoint = random.randrange(10, 51, 10)
            message = f"무라벨 제품을 구매하셨군요! \n{total_ecopoint} ECO POINT 가 적립되었습니다!"
            ECOPOINT.objects.create(
                        user_nb=MEMBER.objects.get(id=request.session['row_id']), save_tm = datetime.now(), point_amt=total_ecopoint
            )

        else:
            message = '무라벨 제품이 아닙니다'

        return JsonResponse({'msg': message})
