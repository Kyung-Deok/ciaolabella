"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import base64
import json
import io
import os
from PIL import Image
import pandas as pd
from pprint import pprint

import torch
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

@app.route('/',methods=["GET", "POST"])
def predict():
    if request.method == 'POST':
        image = request.files['image']
        if not image:
            return jsonify({'result':'no image', 'msg': '선택한 이미지가 없습니다!'})

        img_bytes = image.read()
        img = Image.open(io.BytesIO(img_bytes))
        imgs = [img]
        model.conf = 0.5
        results = model(imgs)
        '''
        results.imgs
        results.render()
        buffered = io.BytesIO()
        for img in results.imgs:
            img_base64 = Image.fromarray(img)
            img_base64.save(buffered, format="JPEG")
            print(base64.b64encode(buffered.getvalue()).decode('utf-8'))        
        '''
        results.save(save_dir="/home/ubuntu/multi_pjt3/ciaolabella/static/ecopoint_static/img_output/ecopoint1/")

        print(type(results)) #<class 'models.common.Detections'>
        print(results)
        # to_json으로 변경하면 '[{}, {}, {}, {}]' 와 같이 문자열이 되기 때문에 json.loads 로 파이썬 객체로 변경 후 보내야 함
        print(results.pandas().xyxy[0][['name', 'confidence']])
        print(type(results.pandas().xyxy[0][['name', 'confidence']]))
        result = json.loads(results.pandas().xyxy[0][['name', 'confidence']].to_json(orient='records'))
        print(result)
        print(type(result))
        #print(result) #[{"name":"label","confidence":0.9791944623},{"name":"plastic","confidence":0.3288115859}]
        #print(type(result)) #<class 'str'>
        #return jsonify({'result': result, 'result_img': image})
        return jsonify({'result': result})



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=8001, type=int, help="port number")
    args = parser.parse_args()

    # yolo model 불러오기
    model = torch.hub.load('./yolov5' , 'custom', path='./yolov5/runs/train/rreal_final13/weights/best.pt', source='local')
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
