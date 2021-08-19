from Control.SingleTon import *
import pymysql

class DatabaseController(SingletonInstane):
    conn = None
    cur = None 

    def __init__(self):
        self.conn = pymysql.connect(host='163.180.116.47', user='minstone', passwd='1124MSqueen', 
                                    db='newbie', charset='utf8')
        self.cur = self.conn.cursor()

    def loadUser_id(self, Id): 
        '''
        id 입력하면 user 보내줌 
        '''
        sql = "SELECT * FROM user WHERE id = " + "'{}'".format(Id)
        user = self.sendQuery(sql)

        if len(user) == 0 :
            return None 
        else:
            return user[0]

    def get_name_id_phNum(self, PhNum, Name):
        '''
        return (id)
        휴대폰 번호 입력하면 user name id 반환 
        '''
        sql = "SELECT id FROM user WHERE phone_number = '{}' AND name = '{}'".format(PhNum, Name)
        user = self.sendQuery(sql)
        if len(user) != 0 :
            return user[0][0]
        else:
            return None
    
    def get_pw(self, Id, PhNum, Name):
        '''
        return (password)
        아이디 폰번호 이름 입력하면 비밀번호 반환 
        '''
        sql = "SELECT pw FROM user WHERE id = '{}' AND phone_number = '{}' AND name = '{}'".format(Id, PhNum, Name)
        pw = self.sendQuery(sql)
        if len(pw) != 0 :
            return pw[0][0]
        else :
            return None
        
    def insertUser(self, Name, PhNum, Email, NickName, Id, Pw, Greeting):
        sql = "INSERT INTO user(name, phone_number, email, nick_name, id, pw, greeting) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(Name, PhNum, Email, NickName, Id, Pw, Greeting)
        result = self.sendQuery(sql)
        return result 

    def changeInfo(self, Name, PhNum, Email, NickName, Id, Pw, Greeting):
        sql = "UPDATE user SET name = '{}', email = '{}', nick_name = '{}', pw = '{}', greeting = '{}' WHERE id = '{}'".format(Name, Email, NickName, Pw, Greeting, Id)
        result = self.sendQuery(sql)

        if len(result) == 0 or result == None:
            return False
        else :
            return True

    def pwCheck(self, id, pw):
        sql = "SELECT * FROM user WHERE id = '{}' AND pw = '{}'".format(id, pw)
        result = self.sendQuery(sql)
        if result:
            return result[0]   
        else:
            return None 

    def sendQuery(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return self.cur.fetchall()
        except:
            return None

# print(DatabaseController().instance().get_name_id_phNum("010-4953-8759"))