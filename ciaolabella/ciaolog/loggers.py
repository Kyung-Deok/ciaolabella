import logging

'''
 logger 별 이벤트
- userlog.inout : UserLogin, UserLogout
- userlog.menuclick : UserClickMenu
- userlog.ecopoint : UserUsedEcopoint1, UserUsedEcopoint2
- userlog.nolabel : UserSearchProduct, UserClickProduct
- userlog.lesswaste : UserSearchLesswaste
'''
def UserInfo(request):
    member_id = request.session.get("member_id", "none")
    user_gender = request.session.get("user_gender", "none")
    user_age = request.session.get("user_age", "none")
    user_region = request.session.get("user_region", "none")
    return member_id, user_gender, user_age, user_region

def UserLogin(request, login_time):
    user_info = UserInfo(request)
    data = {
            'topic' : 'log_inout',
            'key':'login',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'login_time': login_time
    }
    logger = logging.getLogger('userlog.inout')
    logger.info('UserLogin', extra=data)

def UserLogout(request, logout_method, logout_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_inout',
            'key': 'logout',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'logout_method': logout_method,
            'logout_time': logout_time
    }
    logger = logging.getLogger('userlog.inout')
    logger.info('UserLogout', extra=data)

def UserClickMenu(request, selected_menu, menuclick_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_menuclick',
            'key': 'menuclick',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'selected_menu': selected_menu,
            'menuclick_page': request.headers.get('Referer'),
            'menuclick_time': menuclick_time
    }
    logger = logging.getLogger('userlog.menuclick')
    logger.info('UserClickMenu', extra=data)

def UserUsedEcopoint1(request, eco1upload_time, save_point=0, photo_id='', fail_msg=''):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_ecopoint',
            'key': '1',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'save_point': save_point,
            'photo_id': photo_id,
            'eco1upload_time': eco1upload_time,
            'fail_msg': fail_msg
    }
    logger = logging.getLogger('userlog.ecopoint')
    logger.info('UserUsedEcopoint1', extra=data)

def UserUsedEcopoint2(request, eco2upload_time, save_point=0, fail_msg=''):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_ecopoint',
            'key': '2',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'save_point': save_point,
            'eco2upload_time': eco2upload_time,
            'fail_msg': fail_msg
    }
    logger = logging.getLogger('userlog.ecopoint')
    logger.info('UserUsedEcopoint2', extra=data)

def UserSearchProduct(request, search_word, searchclick_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_nolabel',
            'key': 'search',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'search_word': search_word,
            'searchclick_time': searchclick_time
    }
    logger = logging.getLogger('userlog.nolabel')
    logger.info('UserSearchProduct', extra=data)

def UserClickProduct(request, product_name, product_volume, product_unitprice, productclick_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_nolabel',
            'key': 'click',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'product_name': product_name,
            'product_volume': product_volume,
            'product_unitprice': product_unitprice,
            'productclick_time': productclick_time
    }
    logger = logging.getLogger('userlog.nolabel')
    logger.info('UserClickProduct', extra=data)

def UserSearchLesswaste(request, radius_km, searchclick_location, searchclick_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'log_lesswaste',
            'key': 'lesswaste',
            'member_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'radius_km': radius_km,
            'searchclick_location': searchclick_location,
            'searchclick_time': searchclick_time
    }
    logger = logging.getLogger('userlog.lesswaste')
    logger.info('UserSearchLesswaste', extra=data)