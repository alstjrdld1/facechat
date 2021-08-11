class User:

    name = None
    phNum = None 
    email = None 
    nickName = None 
    id = None 
    password = None 
    greeting = None 

    def __init__(self, Name, PhNum, Email, NickName, Id, Password, Greeting):
        self.name = Name
        self.phNum = PhNum
        self.email = Email
        self.nickName = NickName
        self.id = Id
        self.password = Password
        self.greeting = Greeting

    def setUser(self, Name, PhNum, Email, NickName, Id, Password, Greeting):
        self.name = Name
        self.phNum = PhNum
        self.email = Email
        self.nickName = NickName
        self.id = Id
        self.password = Password
        self.greeting = Greeting

    def getName(self):
        return self.name 
    def setName(self, Name):
        self.name = Name

    def getPhNum(self):
        return self.phNum
    def setPhNum(self, PhNum):
        self.phNum = PhNum
    
    def getEmail(self):
        return self.email
    def setEmail(self, Email):
        self.email = Email

    def getNickName(self):
        return self.nickName
    def setNickName(self, nickname):
        self.nickName = nickname

    def getId(self):
        return self.id
    def setId(self, myid ):
        self.id = myid

    def getPw(self):
        return self.password
    def setPw(self, pw):
        self.password = pw 

    def getGreeting(self):
        return self.greeting 
    def setGreeting(self, message):
        self.greeting = message 