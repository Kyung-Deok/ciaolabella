from django.shortcuts import render
from .models import ADMIN

# Create your views here.

def admin_signin(request):
    if request.method == "GET":
        return render(request, 'ciaoadmin/signin.html')

    elif request.method == "POST":
        context = {}
        admin_id = request.POST.get('admin_id')
        admin_pw = request.POST.get('admin_pw')

        am = ADMIN.objects.filter(admin_id=admin_id, admin_pw=admin_pw ).first()

        if am is not None:

            # OK - 로그인
            request.session['admin_id'] = am.admin_id

            context['admin_id'] = am.admin_id

            return render(request, 'ciaoadmin/eventlog.html', context)

        else:
            context['message'] = "로그인 정보가 맞지않습니다.\\n\\n 확인하신 후 다시 시도해 주십시오."
            return render(request, 'admin/signin.html', context)

def event_log(request):
    return render(request, 'ciaoadmin/eventlog.html')
