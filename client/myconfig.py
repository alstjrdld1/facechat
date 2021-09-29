from PyQt5.QtCore import QSize
import os 

CURRENT_DIR = os.getcwd()

SERVER_IP = "IP"
PORT = '8888'

FACE_CHAT_PORT = '9999'
AUDIO_CHAT_PORT = 9091

###############################################################
# UTILS
###############################################################
PROGRAM_NAME = "Face Chat Application"

### PAGE NAME
LOGIN = "login"
LOGOUT = "logout"
FIND_ID = "find ID"
FIND_PW = "find PW"
SIGN_UP = "sign up"

MY_PAGE = "my page"

CHAT_ROOM = "chat room"
CHAT_LIST = "chat list"
USER_ROOM = "chat wait room"

###############################################################
# IMAGES
###############################################################

#### ICON
WINDOW_ICON = os.path.join(CURRENT_DIR, 'client/View/Images/flower.JPG')
BACK_BUTTON_ICON = os.path.join(CURRENT_DIR, 'client/View/Images/backbutton.png')
ADD_ICON = os.path.join(CURRENT_DIR, 'client/View/Images/add.png')
SEARCH_ICON = os.path.join(CURRENT_DIR, 'client/View/Images/search.png')
USER_ICON = os.path.join(CURRENT_DIR, 'client/View/Images/user.png')

###############################################################
# DESIGN
###############################################################

#### SIZE 
WINDOW_SIZE = QSize(600, 500)
WIDGET_SIZE = QSize(500, 450)

BUTTON_SIZE_LARGE = QSize(100, 40)
BUTTON_SIZE_MEDIUM = QSize(100, 40)
BUTTON_SIZE_SMALL = QSize(100, 40)

#### color 
BACKGROUND_COLOR = "background-color: white;"

### font
FONT_SIZE_LARGE = "font-size: 24px;"
FONT_SIZE_MEDIUM = "font-size: 18px;"
FONT_SIZE_SMALL = "font-size: 12px;"