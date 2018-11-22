import os

TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')


BOARD_NAME = "Aruba"
CUSTOM_BOARD_NAME = "Manasa"
LOGGED_USER_CARD_NAME = "Manasa"
MOVE_TO_LIST_ORDER = [ "1st Round", "2nd Round", "Shortlisted"]
CUSTOM_LIST_NAMES = ["Rejected", "Shortlisted", "2nd Round", "1st Round", "Scheduled"]
TEAM_MATES = ["Archit", "Ashish"]
REJECTED_CARD_NAME = "Sampath"
REJECTED_LIST_NAME = "Rejected"

# BOARD_NAME = os.environ.get('BOARD_NAME')
# CUSTOM_BOARD_NAME = os.environ.get('CUSTOM_BOARD_NAME')
# LOGGED_USER_CARD_NAME = os.environ.get('LOGGED_USER_CARD_NAME')
# MOVE_TO_LIST = os.environ.get('MOVE_TO_LIST')
# CUSTOM_LIST_NAMES = os.environ.get('CUSTOM_LIST_NAMES')
# TEAM_MATES = os.environ.get('TEAM_MATES')
# REJECTED_CARD_NAME = os.environ.get('REJECTED_CARD_NAME')
# REJECTED_LIST_NAME = os.environ.get('REJECTED_LIST_NAME')
