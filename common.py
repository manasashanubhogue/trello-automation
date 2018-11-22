import logging
import requests
from datetime import datetime

from constant_urls import SEARCH_URL, CREATE_BOARD_URL, BOARD_LIST_URL, CARD_URL, CREATE_CARD_URL, MOVE_CARDS_URL, \
    MEMBER_URL, BOARD_URL, LISTS_URL, PUT_CARD_URL, COMMENT_URL
from resources import TRELLO_API_KEY, TRELLO_TOKEN

list_mapper = []
card_names = []

LOG_FILENAME = 'log-file.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


def request_api(type, url, querystring):
    """
    :param type: Request method - GET, POST..
    :param querystring: query param
    :param url: trello url
    :return: response
    """
    querystring.update({"key": TRELLO_API_KEY,
                        "token": TRELLO_TOKEN})
    response = requests.request(type, url, params=querystring)
    return response


def get_member_details():
    """
    :return: Get loggedin users details
    """
    response = request_api("GET", MEMBER_URL, {})
    return response.json()


def get_board_id(board_name):
    """
    :param board_name:  Trello board name
    :return: board id corresponing to board name
    """
    board_list = request_api("GET", BOARD_URL, {})
    for board in board_list.json():
        if board['name'] == board_name:
            logging.info("{} is id for board_name {}".format(board['id'], board_name))
            return board['id']
    return None


def get_all_cards(board_name):
    """
    :param board_name: Trello board name
    :return: Return board_id and details of all cards present
    """
    board_id = get_board_id(board_name)
    if board_id:
        cards_list = request_api("GET", CARD_URL.format(board_id), {})
        return board_id, cards_list.json()
    return None


def get_list_id_based_on_name(board_id, list_name):
    """
    :param board_id: Trello board id
    :param list_name: Name of the list
    :return: List details
    """
    response = request_api("GET", LISTS_URL.format(board_id), {})
    for data in response.json():
        if data['name'] == list_name:
            return data


def get_card_details(card_list, card_name):
    """
    :param card_list: List of cards present in board
    :param card_name: Name of card required
    :return: Details of card required
    """
    for card in card_list:
        if card['name'] == card_name:
            card_data = {
                'id': card['id'],
                'board_id': card['idBoard'],
                'list_id': card['idList'],
            }
            return card_data


def move_card(card_id, list_id):
    """
    :param card_id: Card id to be moved
    :param list_id: List id to which card is to be moved
    :return:
    """
    request_api("PUT", PUT_CARD_URL.format(card_id), {"idList": list_id})


def comment_card(card_id, list_name, moved_by, card_present):
    """
    :param card_id: Card id to whoch comment is to be added
    :param list_name: Name of the list
    :param moved_by: Moved by memeber name
    :param card_present: Check on list id of the card
    :return:
    """
    if card_present:
        comment = "Card in " + list_name + " list. Ignored by " + moved_by + "-" + datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')
    else:
        comment = "Moved to " + list_name + " by " + moved_by + "-" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request_api("POST", COMMENT_URL.format(card_id), {"text": comment})


def check_board_exists(board_name):
    """
    :param board_name: Trello board name
    :return: board id if trello board exists else None
    """
    response = request_api("GET", SEARCH_URL, {"query": board_name})
    if (len(response.json()['boards']) > 0):
        board_id = response.json()['boards'][0]['id']
        return board_id
    return None


def create_board(board_name):
    """
    :param board_name: Trello board name to be created
    :return: board_id of the trello board created
    """
    response = request_api("POST", CREATE_BOARD_URL,
                           {"name": board_name, "defaultLists": "false"})
    board_id = response.json()['id']
    return board_id


def check_list_exists(board_id):
    """
    :param board_id: Trello board Id
    :return: None if list doesnt exist, else name and id's of list present in board
    """
    response = request_api("GET", BOARD_LIST_URL.format(board_id), {})
    if (len(response.json()) > 0):
        for value_dict in response.json():
            list_mapper.append({
                "name": value_dict['name'],
                "id": value_dict['id']
            })
        return list_mapper
    return None


def create_lists(board_id, list_names):
    """
    :param list_names : name of lists to be created in board
    :param board_id: Trello board ID
    :return: name and id's of list created in board
    """
    for name in list_names:
        querystring = {"name": name}
        response = request_api("POST", BOARD_LIST_URL.format(board_id), querystring)
        list_mapper.append({
            "name": response.json()['name'],
            "id": response.json()['id']
        })
    return list_mapper.reverse()


def check_card_exists(board_id, team_mates):
    """
    :param board_id: Trello board ID
    :param team_mates: Cards of teammates to be created
    :return: True if cards are present, else False
    """
    response = request_api("GET", CARD_URL.format(board_id), {})
    if (len(response.json()) > 0):
        for card in response.json():
            card_names.append(card['name'])
        if cmp(card_names, team_mates) == 0:
            return True
    return False


def create_cards(card_names, list_mapper):
    for name in card_names:
        logging.info("Creating card {}".format(name))
        request_api("POST", CREATE_CARD_URL, {"idList": list_mapper[0]['id'], "name": name})


def move_all_card(list_mapper, board_id):
    for option, value in enumerate(list_mapper):
        if ((option + 1) < len(list_mapper)):
            request_api("POST", MOVE_CARDS_URL.format(list_mapper[option]['id']),
                        {"idBoard": board_id, "idList": list_mapper[option + 1]['id']})
            logging.info("Moved cards to {}".format(list_mapper[option + 1]['name']))

