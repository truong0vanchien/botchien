from database import supabase_db as db
from library import customLLM as cllm
from model.message import message as mMessage

def askQuestion(question, subject):
    name = question.name
    
    if name not in ('Cody', 'Chien', 'Asky'):
        return False

    # Connect database.
    valid = db.connect(question)

    # Read definition and training from Supabase
    subject_data = db.getSubjectData(subject)
    
    lstRecord = []
    # 1. Add definition (role: system)
    if subject_data.get('definition'):
        lstRecord.append({
            'role': 'system',
            'content': subject_data['definition']
        })
    
    # 2. Add training (role: system)
    if subject_data.get('training'):
        lstRecord.append({
            'role': 'system',
            'content': subject_data['training']
        })

    # 3. Add user question (role: user)
    lstRecord.append({
        'role': question.role,
        'content': question.content
    })
    
    # Connect LLM.
    valid = cllm.connectCody()

    # Ask LLM and get answer.
    response = cllm.submitCody(lstRecord)

    if response == False:
        return False
    
    role = response['role']
    action = 'answer'
    content = response['content']

    answer = mMessage(name=name, role=role, action=action, content=content)

    # Create answer.
    valid = db.createOne(answer)

    result = False
    if valid:
        result = answer

    # Return answer.
    return result