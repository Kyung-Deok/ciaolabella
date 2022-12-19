from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
import logging
from ciaolog.loggers import UserClickMenu, UserUsedEcopoint1, UserUsedEcopoint2
from ciaolabella.env_settings import FLASK_PORT, MONGO_URL, MONGO_PORT
from datetime import datetime
from member.models import MEMBER, ECOPOINT
import random
from pymongo import MongoClient
from PIL import Image
import gridfs
from bson.objectid import ObjectId
import codecs
from django.core.cache import cache
import io

def index(request): # main
    return render(request, 'ciaolabella/index.html')

def about(request):
    return render(request, 'ciaolabella/about.html')

def checkmember(request):
    if request.session.get("member_id", None):
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
        member_id = request.session['member_id']

        # 사진 용량 제한
        if image.size > 16*2**20: # 16MB 초과
            message = '16MB이하의 사진만 업로드 가능합니다.'
            UserUsedEcopoint1(request, eco1upload_time, fail_msg='ImgOverSize')
            return JsonResponse({'msg': message})
        image_input = image.read()

        # 사진 메타데이터 인식 및 촬영 날짜 제한
        try:
            pic_time = Image.open(image)._getexif()[36867]
            if pic_time[:10] != datetime.now().strftime("%Y:%m:%d"):
                message = '오늘 촬영한 사진을 업로드해 주세요.'
                UserUsedEcopoint1(request, eco1upload_time, fail_msg='ImgNotToday')
                return JsonResponse({'msg': message})
        except:
            message = '사진 촬영시각이 확인되지 않습니다. 사진을 다시 촬영하여 업로드해 주세요.'
            UserUsedEcopoint1(request, eco1upload_time, fail_msg='ImgNoMeta')
            return JsonResponse({'msg': message})

        # 사진 메타데이터로 하루 2번 제한 검증
        eco_cache = cache.get(f'{member_id}_1')
        if eco_cache and eco_cache[0] == datetime.now().strftime("%Y:%m:%d"):
            if eco_cache[1] == 1 and pic_time == eco_cache[2]:
                message = '이미 에코포인트를 적립받은 이미지 입니다.'
                UserUsedEcopoint1(request, eco1upload_time, fail_msg='ImgDuplicated')
                return JsonResponse({'msg': message})
            elif eco_cache[1] > 1:
                message = '오늘은 더이상 등록하실 수 없습니다.'
                UserUsedEcopoint1(request, eco1upload_time, fail_msg='OverCount')
                return JsonResponse({'msg': message})

        # image mongoDB에 저장
        client = MongoClient(MONGO_URL, MONGO_PORT)
        db = client['rawimg']
        fs = gridfs.GridFS(db)
        file_id = fs.put(image_input, member_id=member_id, pic_time=pic_time)

        # Flask와 통신하여 모델 적용
        data = {'file_id': str(file_id), 'member_id': member_id, 'pic_time': pic_time}
        url = FLASK_PORT + 'ecopoint1'
        try:
            resp = requests.post(url, data=data)
            result = resp.json() #json 문자열을 파이썬 객체로 변환
            modelfile_id = result['modelfile_id']
            result_list = result['result']
        except:
            message = '다른 사진을 업로드 해주세요.'
            UserUsedEcopoint1(request, eco1upload_time, fail_msg='ModelError')
            return JsonResponse({'msg': message})

        # mongoDB에서 결과 이미지 로드
        db = client['ecopoint']
        fs = gridfs.GridFS(db)
        img_binary = fs.get(ObjectId(modelfile_id)).read()
        img_base64 = codecs.encode(img_binary, 'base64')
        decode_img = img_base64.decode('utf-8')

        # ecopoint
        plastic, label, ecopoint = 0, 0, 0
        for i in result_list:
            if i['name'] == 'plastic' and i['confidence'] >= 0.5:
                plastic += 1
            elif i['name'] == 'label' and i['confidence'] >= 0.5:
                label += 1
        if plastic < 1:
            message, msg = "플라스틱이 아닙니다!", 'ModelNoPlastic'
        elif plastic >= 1:
            if label >= 1:
                message, msg = f"{label} 개의 불순물이 감지되었습니다. \n깨끗하게 씻어서 분리수거 해주세요!", 'ModelYesLabel'
            else:
                count = 2 if cache.get(f'{member_id}_1') else 1
                ecopoint = plastic*10
                message, msg = f'{plastic} 개를 깨끗하게 분리수거하셨네요! \n덕분에 지구가 시원해졌어요! \n{ecopoint} ECO POINT 가 적립되었습니다!', ''
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
        UserUsedEcopoint1(request, eco1upload_time, ecopoint, file_id, msg)

        return JsonResponse({'msg': message, 'decode_img': decode_img})


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

        member_id = request.session['member_id']

        # 하루 1번 제한
        eco_cache = cache.get(f'{member_id}_2')
        if eco_cache and eco_cache[0] == datetime.now().strftime("%Y:%m:%d"):
            message = '오늘은 이미 에코포인트를 적립받으셨습니다.'
            UserUsedEcopoint2(request, eco2upload_time, 0, 'OverCount')
            return JsonResponse({'msg': message})

        image = request.FILES['image']
        url = FLASK_PORT + 'ecopoint2'
        upload = {'image': image}

        try:
            resp = requests.post(url, files=upload)
            result = resp.json()
            result = result['result']
        except:
            message = '다른 사진을 업로드 해주세요.'
            UserUsedEcopoint2(request, eco2upload_time, fail_msg='ModelError')
            return JsonResponse({'msg': message})

        if ('무라벨'or'무라밸'or'라벨X'or'라밸X'or'라벨x'or'라밸x'or'노라밸'or'노라벨') in result:
            ecopoint = random.randrange(10, 51, 10)
            message = f"무라벨 제품을 구매하셨군요! \n{ecopoint} ECO POINT 가 적립되었습니다!"
            UserUsedEcopoint2(request, eco2upload_time, ecopoint)

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
            message= '무라벨 제품이 아닙니다'
            UserUsedEcopoint2(request, eco2upload_time, 0, 'OcrNoDetect')
        try:
            img = Image.open(image)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            img_binary = buffer.getvalue()
            img_base64 = codecs.encode(img_binary, 'base64')
            decode_img = img_base64.decode('utf-8')
        except:
            decode_img = ''

        return JsonResponse({'msg': message, 'decode_img':decode_img})