from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import MEMBER, ECOPOINT
from ciaolog.loggers import UserLogin, UserLogout
from ciaolabella.env_settings import REDIS_NODES, REDIS_PW
from datetime import datetime
import time
from django.db.models import Sum
from . import ecograph
from django.http import JsonResponse
from rediscluster import RedisCluster


def member_page(request):

    context={}
    member_id = request.session['member_id']

    # 회원정보
    rs = MEMBER.objects.filter(member_id=member_id).first()
    context['member'] = rs

    # 회원 포인트 정보 - 내림차순
    point = ECOPOINT.objects.filter(member_id=member_id)
    context['point'] = point

    # 총 포인트
    # {'point_amt__sum': 70 }
    total = point.aggregate(Sum('point_amt'))['point_amt__sum']
    context['total'] = total

    # 에코 등급
    try :
        if total <= 10:
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

    # 실시간 검색어
    search_dic = {}
    date = datetime.today().strftime('%Y%m%d')
    age_cri = 10*((datetime.today().year - int(rs.birth_dt[:4]))//10)
    context['age_cri'] = age_cri
    gen_cri = rs.gender_kb
    context['gender_cri'] = '남성' if gen_cri == 'M' else '여성'

    r = RedisCluster(startup_nodes=REDIS_NODES, password=REDIS_PW, decode_responses=True)

    age_search, gen_search = {}, {}
    for key in r.scan_iter(match=f'search:{date}:*:{age_cri}:*', count=100):
        word = key.split(':')[-1]
        count = r.hget(key, 'count')
        age_search[word] = count
    age_search = sorted(age_search.items(), key = lambda x: -int(x[1]))
    for i in range(min(5, len(age_search))):
        search_dic[f'age{i+1}'] = age_search[i][0]

    for key in r.scan_iter(match=f'search:{date}:{gen_cri}:*', count=100):
        word = key.split(':')[-1]
        count = r.hget(key, 'count')
        gen_search[word] = count
    gen_search = sorted(gen_search.items(), key = lambda x: -int(x[1]))
    for i in range(min(5, len(gen_search))):
        search_dic[f'gen{i+1}'] = gen_search[i][0]

    context['search'] = search_dic
        
    # 기간별 에코포인트
    try:
        context['graph'] = ecograph.ecopoint(member_id)
    except:
        context['graph'] = None

    return render(request, 'member/mypage.html', context)

#회원 가입
def member_reg(request):
    if request.method == "GET":
        if request.session.get("member_id", None) is not None :
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
        birth_dt = request.POST.get("birth_dt", False)
        gender_kb = request.POST.get("gender_kb", False)

        # 회원가입 중복체크
        rs = MEMBER.objects.filter(user_id=user_id)

        if rs.exists():
            context['message'] = user_id + "가 중복됩니다."
            context['id_check'] = 0
            return JsonResponse(context)
            #return render(request, 'member/register.html', context)
        # elif 비밀번호 != 비밀번호 재입력 : 비밀번호 다시 확인해달라는 창
        else:
            MEMBER.objects.create(
                user_id=user_id, user_pw=user_pw, user_nm=user_nm, email_txt=email_txt,
                phone_nb=phone_nb, region_kb=region_kb, birth_dt=birth_dt, gender_kb=gender_kb,
                register_dt=datetime.now().strftime('%Y-%m-%d'))
            context['message'] = user_id + "님 회원가입 되었습니다."
            context['id_check'] = 1
            return JsonResponse(context)
            #return render(request, 'ciaolabella/index.html', context)


def member_login(request):
    if request.method == "GET":
        if request.session.get("member_id", None) is not None :
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
            request.session['member_id'] = rs.member_id
            request.session['user_gender'] = rs.gender_kb
            user_age = int(datetime.today().year) - int(rs.birth_dt[:4]) + 1
            request.session['user_age'] = user_age
            request.session['user_region'] = rs.region_kb
            request.session['_session_init_timestamp_'] = time.time()
            login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            UserLogin(request, login_time)

            context['user_id'] = rs.user_id
            context['user_nm'] = rs.user_nm
            context['message'] = rs.user_nm + "님이 로그인하셨습니다."
            context['login_chk'] = 1
        else:
            context['message'] = "로그인 정보가 맞지않습니다.\n확인하신 후 다시 시도해 주십시오."

        return JsonResponse(context)

def member_logout(request):
    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    UserLogout(request, 'ButtonClicked', logout_time)
    request.session.flush()
    return redirect('index')

def member_logout2(request):
    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.session.get('row_id', None):
        UserLogout(request, 'BrowserClosed', logout_time)
        request.session.flush()
    return JsonResponse({'msg': 'success'})
