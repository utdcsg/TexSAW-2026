from flask import Flask, render_template, request, make_response
import random
import time
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "site.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy instance
db = SQLAlchemy(app)

class Identifier(db.Model):
    identifier = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    timeCreated = db.Column(db.Float, nullable=False)

def generate_unique_identifier(length=20):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    identifier = ''.join(random.choices(characters, k=length))
    return identifier

page_variations = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

def make_variation_route(variation):
    def route_handler():
        second = round(time.time()) % 10
        if second == page_variations.index(variation):
            return render_template('yes_found.html'), 200
        else:
            return render_template('not_found.html'), 404
    return route_handler

for i in range(10):
    variation = page_variations[i]
    route_path = f'/{variation}'
    app.add_url_rule(rule=route_path, endpoint=variation, view_func=make_variation_route(variation))


@app.route('/')
def index():
    #print(request.headers)
    response = make_response(render_template('index.html'))
    user_identifier = generate_unique_identifier()
    new_id = Identifier(identifier=user_identifier, timeCreated=time.time())
    db.session.add(new_id)
    db.session.commit()
    response.set_cookie(
        'identifier', 
        user_identifier
    )
    return response

@app.route('/GstXsG7s9t')
def getsegment():
    user_identifier = request.cookies.get('identifier')
    #print(f"Identifier from cookie: {user_identifier}")
    matching_entry = Identifier.query.filter_by(identifier=user_identifier).first()
    message = ""
    if matching_entry:
        db.session.delete(matching_entry)
        db.session.commit()
        current_time = time.time()
        elapsed_time = current_time - matching_entry.timeCreated
        if elapsed_time < 3:
            message = "Too fast"
        elif elapsed_time > 10:
            message = "Too slow"
        else:
            message = "f742Hl==oSAv6I==IjP4oM==CU8KCl==gKNvo5==idNtig==ge0GgQ==iUPtkf==iWNxkS==CdN7oO==HUgGkl==oKNxkj==CdNmgr==oeN4gr==ISCwgK==oUJx6G=="
    else:
        message = "No matching identifier found."
    #print(request.cookies)
    response = make_response({"segment": message})
    return response

@app.route('/robots.txt')
def robots_txt():
    second = round(time.time()) % 10
    return f'User-agent: *\nDisallow: /{page_variations[second]}/\n', 200, {'Content-Type': 'text/plain'}

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
            
    flag_segment = "FSbZCM==CdNmHl==g9fQIJ==o5HGHC==Iji4H9==IjNbCQ==CdmGiJ==kSlGg/==ijP8He==ijFZCl==6WNxkB==CdNQih==sUA46J==ISJ2Ca==IjfVC1==Ijnrgr==k1Nx6KhG"
    return make_response({"response": f'WV33sgt k9Xms3X! ak3t VD tbs D4kG KX: {flag_segment}'}, 200)

if __name__ == '__main__':
    with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables
    app.run(host='0.0.0.0', port=5000)
