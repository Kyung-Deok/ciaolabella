from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
import logging
from ciaolabella.loggers import UserClickMenu, UserUsedEcopoint1, UserUsedEcopoint2
from ciaolabella.env_settings import FLASK_PORT
from datetime import datetime
from member.models import MEMBER, ECOPOINT
from . import ocr
import random

def index(request): # main
    return render(request, 'ciaolabella/index.html')

def about(request):
    return render(request, 'ciaolabella/about.html')

def checkmember(request):
    if request.session.get("row_id", None):
        return True
    else:
        return False

def aboutecopoint(request):
    return render(request, 'ciaolabella/index.html')

def ecopoint(request):
    if request.method == 'GET':
        if checkmember(request):
            menuclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            UserClickMenu(request, 'ecopoint1', menuclick_time)
            return render(request, 'ecopointapp/ecopoint.html')
        else:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)
    else:
        eco1upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if "image" not in request.FILES:
            return redirect(request.url)

        image = request.FILES['image']
        upload = {'image': image}
        url = FLASK_PORT
        resp = requests.post(url, files=upload)
        result = resp.json() #json 문자열을 파이썬 객체로 변환
        print(image)
        # ecopoint
        result_list = result['result']
        plastic = 0
        label = 0
        if f"{image}" == request.session.get("eco_img", None)[0] :
            message, save_point = "중복된 이미지 입니다.", 0
        elif request.session.get("eco_img", None)[1] >= 2 :
            if request.session.get("eco_img", None)[2] == datetime.now().strftime("%y-%m-%d"):
                message, save_point = "오늘은 더이상 등록하실 수 없습니다. 죄송합니다.", 0
            else :
                request.session.get("eco_img", None)[1] = 0
        elif result_list:
            for i in result_list:
                if i['name'] == 'plastic' and i['confidence'] >= 0.5:
                    plastic += 1
                elif i['name'] == 'label' and i['confidence'] >= 0.5:
                    label += 1
            if plastic < 1:
                message, save_point = "플라스틱이 아닙니다!", 0
            elif plastic >= 1:
                if label >= 1:
                    message, save_point = f"{label} 개의 불순물이 감지되었습니다. \n깨끗하게 씻어서 분리수거 해주세요!", 0
                else:
                    count = request.session.get("eco_img", 0)[1]
                    save_ecopoint = plastic*10
                    message = f'{plastic} 개를 깨끗하게 분리수거하셨네요! \n덕분에 지구가 시원해졌어요! \n{save_ecopoint} ECO POINT 가 적립되었습니다!'
                    day_count = count + 1
                    ECOPOINT.objects.create(user_nb=MEMBER.objects.get(id=request.session['row_id']), save_tm = datetime.now(), point_amt=save_ecopoint)
                    request.session['eco_img'] = [f"{image}", day_count, datetime.now().strftime("%y-%m-%d")]
                    print(request.session['eco_img'])
        else:
            message, save_point = '다른 사진을 선택해 주세요.', 0
        photo_id = "temporary"
        UserUsedEcopoint1(request, save_ecopoint, photo_id, eco1upload_time)
        return JsonResponse({'msg': message})


def ecopoint2(request):
    if request.method == 'GET':
        if checkmember(request):
            menuclick_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            UserClickMenu(request, 'ecopoint2', menuclick_time)
            return render(request, 'ecopointapp/ecopoint2.html')
        else:
            context = {}
            context['message'] = "로그인 해주세요"
            return render(request, 'ciaolabella/index.html', context)
    else:
        eco2upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if "image" not in request.FILES:
            return redirect(request.url)
        image = request.FILES['image']
        results = ocr.ecopointtwo(image)
        result = results['images'][0]['fields']
        list = []
        for i in result:
            list.append(i['inferText'])
        
        if ('무라벨'or'무라밸'or'라벨X') in list:
            save_ecopoint = random.randrange(10, 51, 10)
            message = f"무라벨 제품을 구매하셨군요! \n{save_ecopoint} ECO POINT 가 적립되었습니다!"
            ECOPOINT.objects.create(user_nb=MEMBER.objects.get(id=request.session['row_id']), save_tm = datetime.now(), point_amt=save_ecopoint)
        else:
            message, save_point = '무라벨 제품이 아닙니다', 0

        photo_id = "temporary"
        UserUsedEcopoint2(request, save_ecopoint, photo_id, eco2upload_time)
        return JsonResponse({'msg': message})
