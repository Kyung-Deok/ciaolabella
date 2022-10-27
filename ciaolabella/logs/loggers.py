import logging
from member.models import MEMBER
from datetime import datetime

'''
#이벤트별 logger
UserLogin, UserLogout => ciaolabella.userinout #카멜 표기법으로?
UserClickMenu => ciaolabella.menu #별로임
UserUsedEcopoint1, UserUsedEcopoint2 => ciaolabella.ecopoint
UserSearchProduct, UserClickProduct => ciaolabella.nolabel
UserSearchLesswaste => ciaolabella.lesswaste
Page Viewed => django.request
'''

#회원만 이용할 수 있는 event
def UserLogin(request):
    login_id = request.session.get("row_id")
    rs = MEMBER.objects.filter(id=request.session['row_id']).first()

    #로그의 목적별로 logger를 따로 할 것!
    UserLogin_logger = logging.getLogger('')

    #기본적인 4개 + 시간 + @
    #str(datetime.now()) : '2022-10-26 17:35:03.955527'
    data = {'user_id': rs.id, 'user_gender': rs.gender_kb, 'user_age': rs.birth_nb, 'user_region': rs.region_kb, 'login_date':str(datetime.now())}

    UserLogin_logger.info('UserLogin', extra=data)


#비회원도 이용할 수 있는 event
def UserSearchLesswaste(request):
    #login시 => 해당 유저의 id, unlogin시 => None
    login_id = request.session.get("row_id", None)

    #로그인시
    if login_id:
        rs = MEMBER.objects.filter(id=request.session['row_id']).first()

        #로그의 목적별로 logger를 따로 할 것!
        UserLogin_logger = logging.getLogger('')

        #기본적인 4개 + 시간 + @
        #str(datetime.now()) : '2022-10-26 17:35:03.955527'
        data = {'user_id': rs.id, 'user_gender': rs.gender_kb, 'user_age': rs.birth_nb, 'user_region': rs.region_kb, 'searchclick_date': str(datetime.now())}
    #비로그인시
    else:
        pass

    UserLogin_logger.info('UserLogin', extra=data)