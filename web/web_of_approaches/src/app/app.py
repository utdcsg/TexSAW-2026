from flask import Flask, render_template, request, make_response
import random
import time
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    #print(request.headers)
    response = make_response(render_template('index.html'))
    return response

@app.route('/gbsgTh9Xms3X', methods=['POST'])
def check_answers():
    wrong_response = make_response({"response": "I9gV33sgt k9Xms3X. a4skXs s9X23s k44 sAKXtK9G E2sXtKV9X bkws k gV33sgt k9Xms3."}, 200)
    answers = request.json
    correct_answers = {
        "E2sXtKV9-1": "XRk9",
        "E2sXtKV9-2": "V4",
        "E2sXtKV9-4": "s7",
        "E2sXtKV9-5": "o3"
    }
    for question, answer in answers.items():
        if question in correct_answers:
            if correct_answers[question] != answer:
                return wrong_response
        elif question == "E2sXtKV9-3":
            return wrong_response
            
    flag_segment = "FSzGC4==kUvTIP==HUAXIJ==iSb4Ia==gSJZiJ==gZNvoe==idNekM==oSmGoT==CUFTIJ==iSzGgv==CUJZHe==kWNekB==C1P4IJ==sUp8Ia==o7pZo1==HUAXsl==IS8RCQ==kj0Gom==i7FZoJ==o5p3Ia==IWhGIj==IWhGIB==IWhGIB==IWhGIh==IWhGIS==IWhGIY=="
    return make_response({"response": f'WV33sgt k9Xms3X! ak3t VD tbs D4kG KX: {flag_segment}'}, 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
