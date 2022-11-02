import logging
from pprint import pprint
from datetime import datetime
from .handlers import KafkaHandler
'''
 logger 별 이벤트
- userlog.duration : UserLogin, UserLogout
- userlog.menuclick : UserClickMenu
- userlog.ecopoint : UserUsedEcopoint1, UserUsedEcopoint2
- userlog.nolabel : UserSearchProduct, UserClickProduct
- userlog.lesswaste : UserSearchLesswaste

'''
def UserInfo(request):
    user_id = request.session.get("row_id", "none")
    user_gender = request.session.get("user_gender", "none")
    user_age = request.session.get("user_age", "none")
    user_region = request.session.get("user_region", "none")
    return user_id, user_gender, user_age, user_region

def UserLogin(request):
    user_info = UserInfo(request)
    data = {
            'topic' : 'duration_test',
            'key':'login',
            'user_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'login_time': request.session.get("login_time")
    }
    logger = logging.getLogger('userlog.duration')
    logger.info('UserLogin', extra=data)

def UserLogout(request, logout_method, logout_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'duration_test',
            'key': 'logout',
            'user_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'logout_method': logout_method,
            'logout_time': logout_time
    }
    logger = logging.getLogger('userlog.duration')
    logger.info('UserLogout', extra=data)

def UserClickMenu(request, selected_menu, menuclick_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'menuclick_test',
            'key': 'click',
            'user_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'selected_menu': selected_menu,
            'menuclick_page': request.headers.get('Referer'),
            'menuclick_time': menuclick_time
    }
    logger = logging.getLogger('userlog.menuclick')
    logger.info('UserClickMenu', extra=data)

def UserUsedEcopoint1(request, save_ecopoint, photo_id, eco1upload_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'ecopoint_test',
            'key': '1',
            'user_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'save_ecopoint': save_ecopoint,
            'photo_id': photo_id,
            'eco1upload_time': eco1upload_time
    }
    logger = logging.getLogger('userlog.ecopoint')
    logger.info('UserUsedEcopoint1', extra=data)

def UserUsedEcopoint2(request, save_ecopoint, photo_id, eco2upload_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'ecopoint_test',
            'key': '2',
            'user_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'save_ecopoint': save_ecopoint,
            'photo_id': photo_id,
            'eco2upload_time': eco2upload_time
    }
    logger = logging.getLogger('userlog.ecopoint')
    logger.info('UserUsedEcopoint2', extra=data)

def UserSearchProduct(request, search_word, searchclick_time):
    user_info = UserInfo(request)
    data = {
            'topic': 'nolabel_test',
            'key': 'search',
            'user_id': user_info[0],
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
            'topic': 'nolabel_test',
            'key': 'cilck',
            'user_id': user_info[0],
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
            'topic': 'lesswaste_test',
            'key': '1',
            'user_id': user_info[0],
            'user_gender': user_info[1],
            'user_age': user_info[2],
            'user_region': user_info[3],
            'radius_km': radius_km,
            'searchclick_location': searchclick_location,
            'searchclick_time': searchclick_time
    }
    logger = logging.getLogger('userlog.lesswaste')
    logger.info('UserSearchLesswaste', extra=data)