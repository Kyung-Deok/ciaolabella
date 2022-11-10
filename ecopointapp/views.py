"""
Simple app to upload an image via a web form
and view the inference results on the image in the browser.
"""
import argparse
import json
import io
from PIL import Image
import torch
from flask import Flask, request, jsonify
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId
import pytesseract

app = Flask(__name__)


@app.route('/ecopoint1', methods=["GET", "POST"])
def predict():
    if request.method == 'POST':
        ##### Django로부터 요청 받은 변수 저장 #####
        file_id = request.form['file_id']
        member_id = request.form['member_id']
        pic_time = request.form['pic_time']
        # print('from Django:',file_id, user_id, pic_time)

        ##### mongodb에서 원본 이미지 로드 후 모델 적용#####
        # client = MongoClient("mongodb://127.0.0.1", 27017)
        client = MongoClient("mongodb://admin:qwer1234@218.154.53.236", 27721)
        db = client['rawimg']
        fs = gridfs.GridFS(db)
        # 파일을 db에서 binary 형태로 로드
        img_binary = fs.get(ObjectId(file_id)).read()
        # pillow 모듈 이용하여 이미지객체로 변환 후 모델 적용
        img = Image.open(io.BytesIO(img_binary))
        model.conf = 0.5
        results = model([img])

        ##### 모델 결과 이미지 mongodb 저장 #####
        db = client['ecopoint']
        fs = gridfs.GridFS(db)
        # 모델 결과값 저장 가능한 파일 형태로 변환
        file = Image.fromarray(results.render()[0])
        buffer = io.BytesIO()
        file.save(buffer, format="JPEG")
        contents = buffer.getvalue()
        modelfile_id = fs.put(contents, member_id=member_id, pic_time=pic_time)

        ##### 모델 결과 Django로 재전송 #####
        result = json.loads(results.pandas().xyxy[0][['name', 'confidence']].to_json(orient='records'))

        return jsonify({'result': result, 'modelfile_id': str(modelfile_id)})

    else:
        return '*****Ecopointapp-ecopoint1*****'


@app.route('/ecopoint2', methods=["GET", "POST"])
def ocr():
    if request.method == 'POST':
        image = request.files['image']
        img_pil = Image.open(io.BytesIO(image.read()))
        img_pytesseract = pytesseract.image_to_string(img_pil, lang='kor').replace(' ', '')
        return jsonify({'result': img_pytesseract})

    else:
        return '*****Ecopointapp-ecopoint2*****'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8001, type=int, help="port number")
    args = parser.parse_args()

    # yolo model 불러오기
    model = torch.hub.load('./yolov5', 'custom', path='./yolov5/runs/train/rreal_final13/weights/best.pt',
                           source='local')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat