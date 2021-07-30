global ROOMNUM

class USER:
    __name = ''
    __pw = ''

    def __init__(self):
        print("INITIALIZE")

class ROOM:
    number = 1

    def __init__(self, count):
        number = count

class Camera:
    def __init__(self):
        print("This is Camera")