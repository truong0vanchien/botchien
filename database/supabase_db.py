import os
import requests
import re
import uuid

def connect(record):
    """
    Supabase REST connection is stateless.
    """
    return True

def createOne(record):
    """
    Since each subject in the 'chien' table only has 2 actions: definition and training,
    we do not store chat histories (question/answer) in the Supabase table.
    """
    return True

def readCondition(condition):
    """
    Reads chien definitions and training records from Supabase chien table.
    """
    record = condition['question']
    
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        print("Supabase credentials not found.")
        return []
        
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    note = record.note
    subjects = []
    regex = '(?<= - ).+'
    find = re.search(regex, note)
    if find:
        subject_str = find.group(0)
        subjects = [s.strip() for s in subject_str.split(', ')]
        
    if not subjects:
        return []
        
    subjects_formatted = ','.join(f'"{s}"' for s in subjects)
    url = f"{supabase_url}/rest/v1/chien"
    params = {
        'select': 'id,subject_name,name,role,action,content',
        'subject_name': f'in.({subjects_formatted})',
        'action': 'in.(definition,training)'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        rows = response.json()
        rows.sort(key=lambda r: 0 if r.get('action') == 'definition' else 1)
        return rows
    except Exception as e:
        print(f"Error querying Supabase for Cody: {e}")
        return []

def getSubjectData(subject):
    """
    Retrieves definition and training content for a single subject from Supabase.
    """
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        return {"definition": "", "training": ""}
        
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    url = f"{supabase_url}/rest/v1/chien"
    params = {
        'select': 'action,content',
        'subject_name': f'eq.{subject}',
        'action': 'in.(definition,training)'
    }
    
    result = {"definition": "", "training": ""}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        rows = response.json()
        for row in rows:
            if row['action'] == 'definition':
                result['definition'] = row['content']
            elif row['action'] == 'training':
                result['training'] = row['content']
        return result
    except Exception as e:
        print(f"Error fetching subject data: {e}")
        return result

def updateRecord(subject, action, content):
    """
    Overwrites the definition or training content for a subject in Supabase.
    """
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    if not supabase_url or not supabase_key:
        return False
        
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    # 1. Delete existing row for this subject and action
    delete_url = f"{supabase_url}/rest/v1/chien?subject_name=eq.{subject}&action=eq.{action}"
    try:
        requests.delete(delete_url, headers=headers)
    except Exception as e:
        print(f"Error clearing old record: {e}")
        return False
        
    # 2. Insert new row
    payload = {
        'id': str(uuid.uuid4()),
        'subject_name': subject,
        'name': 'Cody',
        'role': 'system',
        'action': action,
        'content': content
    }
    
    url = f"{supabase_url}/rest/v1/chien"
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error inserting new record: {e}")
        return False
