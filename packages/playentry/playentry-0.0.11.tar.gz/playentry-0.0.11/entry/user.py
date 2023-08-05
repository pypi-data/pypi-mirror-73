from .object import Object
from .enums import UserRole

class User(Object):
    """엔트리 사용자를 나타냅니다. 이 클래스의 인스턴스를 직접 만드는 것은 권장하지 않습니다.
    """
    def __init__(self, *, data):
        self.id = None
        self.username = None
        self.role = None
        self.language = None
        self.login_count = None
        self.description = None

        if '_id' in data:
            self.id = data['_id']
        if 'username' in data:
            self.username = data['username']
        if 'role' in data:
            if data['role'] in UserRole.__dict__:
                self.role = UserRole.__getattr__(data['role'])
        if 'language' in data:
            self.language = data['language']
        if 'loginCount' in data:
            self.login_count = data['loginCount']
        if 'description' in data:
            self.description = data['description']