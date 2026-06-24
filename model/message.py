import uuid
import time

class message():
    def __init__(self, name, role, action, content):
        self.id = str(uuid.uuid4())
        self.timestamp = int(time.time())
        self.name = name
        self.role = role
        self.action = action
        self.content = content