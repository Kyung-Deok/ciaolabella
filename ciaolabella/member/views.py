from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import MEMBER, ECOPOINT
import logging
from datetime import datetime
from django.db.models import Sum
from . import ecograph
from django.http import JsonResponse


def member_page(request):

    context={}

    mem = request.session['row_id']

    # 회원정보
    rs = MEMBER.objects.filter(id=mem).first()
    context['member'] = rs

    # 회원 포인트 정보 - 내림차순
    point = ECOPOINT.objects.filter(user_nb=mem).order_by("-save_tm")[:9]
    point_sum = ECOPOINT.objects.filter(user_nb=mem)
    context['point'] = point

    # 총 포인트
    # {'point_amt__sum': 70 }
    total = point_sum.aggregate(Sum('point_amt'))['point_amt__sum']
    context['total'] = total

    # 에코 등급
    try :
        if 0 < total <= 10:
            context['grade'] = 0
            context['temp'] = '14.5°C'
        elif 10 <  total <= 50:
            context['grade'] = 1
            context['temp'] = '14.4°C'
        elif 50 <  total <= 100:
            context['grade'] = 2
            context['temp'] = '14.3°C'
        elif 100 <  total <= 200:
            context['grade'] = 3
            context['temp'] = '14.2°C'
        elif 200 <  total <= 500:
            context['grade'] = 4
            context['temp'] = '14.1°C'
        elif 500 <  total <= 1000:
            context['grade'] = 5
            context['temp'] = '14.0°C'
        elif 1000 <  total <= 3000:
            context['grade'] = 6
            context['temp'] = '13.9°C'
        elif 3000 <  total <= 10000:
            context['grade'] = 7
            context['temp'] = '13.8°C'
        elif 10000 < total <= 50000:
            context['grade'] = 8
            context['temp'] = '13.7°C'   
        elif 50000 < total <= 100000:
            context['grade'] = 9
            context['temp'] = '13.6°C'
        else:
            context['grade'] = 10
            context['temp'] = '13.5°C' 
    except:
            context['grade'] = 0
            context['temp'] = '14.5°C'       
        
    # 기간별 에코포인트
    try:
        context['graph'] = ecograph.ecopoint(mem)
    except:
        context['graph'] = None

    return render(request, 'member/mypage.html', context)

#회원 가입
def member_reg(request):
    if request.method == "GET":
        if request.session.get("row_id", None) is not None :
            return redirect("index")
        return render(request, 'member/register.html')

    elif request.method == "POST":

        context = {}
        user_nm = request.POST.get("user_nm", False)
        user_id = request.POST.get("user_id", False)
        user_pw = request.POST.get("user_pw", False)
        email_txt = request.POST.get("email_txt", False)
        phone_nb = request.POST.get("phone_nb", False)
        region_kb = request.POST.get("region_kb", False)
        age_nb = request.POST.get("age_nb", False)
        gender_kb = request.POST.get("gender_kb", False)

        # 회원가입 중복체크
        rs = MEMBER.objects.filter(user_id=user_id)

        if rs.exists():
            context['message'] = user_id + "가 중복됩니다."
            return render(request, 'member/register.html', context)
        # elif 비밀번호 != 비밀번호 재입력 : 비밀번호 다시 확인해달라는 창
        else:
            MEMBER.objects.create(
                user_id=user_id, user_pw=user_pw, user_nm=user_nm, email_txt=email_txt, phone_nb=phone_nb, region_kb=region_kb, age_nb=age_nb, gender_kb=gender_kb,
                reg_date=datetime.now())
            context['message'] = user_id + "님 회원가입 되었습니다."
            return render(request, 'ciaolabella/index.html', context)


def member_login(request):
    if request.method == "GET":
        if request.session.get("row_id", None) is not None : 
            return redirect("index")
        return render(request, 'member/login.html')

    elif request.method == "POST":
        context = {}

        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')

        # 로그인 체크하기
        rs = MEMBER.objects.filter(user_id=user_id, user_pw=user_pw).first()

        # if rs.exists():
        if rs is not None:

            # OK - 로그인
            request.session['row_id'] = rs.id
                # request.session['user_nm'] = rs.user_nm

            context['user_id'] = rs.user_id
            context['user_nm'] = rs.user_nm
            context['message'] = rs.user_nm + "님이 로그인하셨습니다."


            # 로그인 로그 수집
            login_logger = logging.getLogger('log')
            data = {'row_id': rs.id , 'age_nb':rs.age_nb, 'gender_kb ': rs.gender_kb, 'region_kb':rs.region_kb,
                    'log_tm':str(datetime.now()), 'log_kb': 'login' }
            login_logger.info('login_log', extra = data)

            return render(request, 'ciaolabella/index.html', context)

        else:
            context['message'] = "로그인 정보가 맞지않습니다.\\n\\n 확인하신 후 다시 시도해 주십시오."
            return render(request, 'member/login.html', context)


def member_logout(request):
    request.session.flush()
    return redirect('index')