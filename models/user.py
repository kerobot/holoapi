class User:
    def __init__(self, id, username, password, firstname, lastname):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__firstname = firstname
        self.__lastname = lastname

    # id
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    # username
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    # password
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    # firstname
    @property
    def firstname(self):
        return self.__firstname

    @firstname.setter
    def firstname(self, firstname):
        self.__firstname = firstname

    # lastname
    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def lastname(self, lastname):
        self.__lastname = lastname

    # ドキュメントから変換
    @classmethod
    def from_doc(cls, doc):
        if doc is None:
            return None
        user = User(doc['id'], 
                    doc['username'], 
                    doc['password'],
                    doc['firstname'],
                    doc['lastname'])
        return user

    # ドキュメントへ変換
    def to_doc(self):
        doc = { 'id': str(self.id),
                'username': str(self.username),
                'password' : str(self.password),
                'firstname' : str(self.firstname),
                'lastname' : str(self.lastname) }
        return doc
