import csv
from dotenv import load_dotenv
load_dotenv()

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, json

from model.message import message as mMessage
from controller import message as cMessage
from library import handler as hdl
import datetime # For deploying.

app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    import os
    subject_list_str = os.environ.get('SUBJECT_LIST', 'Detect PII, Detect single char var or func, Detect collecting voucher or coupon')
    subjects = [s.strip() for s in subject_list_str.split(',')]

    return render_template('index.jinja', subjects=subjects)



@app.route('/api/chien/<string:action>', methods=['POST'])
def chien(action):
    data = request.get_json()

    content = data['content']
    subject = data.get('subject') # Get subject directly
    name = 'Chien'
    if action == 'question':
        role = 'user'
        question = mMessage(name=name, role=role, action=action, content=content)
        # Wait for answer.
        answer = cMessage.askQuestion(question, subject)
        result = {'error': 'No answer.'}
        if answer != False:
            result = {'data': answer.__dict__}
    else:
        result = {'error': 'Wrong action.'}

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/chien/data', methods=['GET'])
def get_chien_data():
    subject = request.args.get('subject')
    if not subject:
        return json.dumps({'error': 'Subject is required.'}), 400
    from database import supabase_db as db
    result = db.getSubjectData(subject)
    return app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/chien/update', methods=['POST'])
def update_chien_data():
    data = request.get_json()
    subject = data.get('subject')
    action = data.get('action') # definition or training
    content = data.get('content')
    if not subject or not action or content is None:
        return json.dumps({'error': 'subject, action and content are required.'}), 400
    from database import supabase_db as db
    success = db.updateRecord(subject, action, content)
    if success:
        return app.response_class(
            response=json.dumps({'message': 'Success'}),
            status=200,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response=json.dumps({'error': 'Failed to update record.'}),
            status=500,
            mimetype='application/json'
        )


# AI Agent.
@app.route('/api/handy/<string:action>', methods=['POST'])
def handy(action):
    pass

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=5000, debug=True)

