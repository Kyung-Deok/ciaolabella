import requests
import uuid
import time
import json
from PIL import Image
import io

def ecopointtwo(image):
    api_url = 'https://uiasrr8pzn.apigw.ntruss.com/custom/v1/18402/8f4c6598faa01843a2a2dd9376d6bcada016623570016c2b54209d24ba61f58b/general'
    secret_key = 'Z0dsU2pMclRKS3JqYnZmU0pIWWxZWENkZ0RaU3RNQWE='

    # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'> -> <class 'str'>
    # image = str(image)

    # 이미지 저장.
    img_bytes = image.read()
    img = Image.open(io.BytesIO(img_bytes))
    img.save("/home/ubuntu/multi_pjt3/ciaolabella/static/ecopoint_static/img_output/ecopoint2/image0.jpg", "JPEG")
    # 이미지 호출.
    image_file = "/home/ubuntu/multi_pjt3/ciaolabella/static/ecopoint_static/img_output/ecopoint2/image0.jpg"

    files = [
    ('file', open(image_file,'rb'))
    ]

    
    request_json = {
    "version": "V2",
    "requestId": str(uuid.uuid4()),
    "timestamp": 0,
    "lang":"ko",
    "images": [
        {
        "format": ("png" or "jpg"),
        "name": "ocr",
        }
        ]
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    headers = {
    'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

    result = response.json()

    return result


