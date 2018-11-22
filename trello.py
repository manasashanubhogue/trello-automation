import logging

from common import get_member_details, get_all_cards, get_card_details, get_list_id_based_on_name, \
    move_card, comment_card, check_board_exists, create_board, check_list_exists, create_lists, check_card_exists, \
    create_cards, move_all_card
from resources import BOARD_NAME, LOGGED_USER_CARD_NAME, CUSTOM_BOARD_NAME, \
    CUSTOM_LIST_NAMES, TEAM_MATES, REJECTED_CARD_NAME, REJECTED_LIST_NAME, MOVE_TO_LIST_ORDER

LOG_FILENAME = 'log-file.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


def assignment_part_1(board_name, card_name, list_name):
    """
    Move card to all lists with comments
    :param board_name:
    :param card_name:
    :param list_name:
    :return:
    """
    member_name = get_member_details()['fullName']
    board_id, cards_list = get_all_cards(board_name)
    card_details = get_card_details(cards_list, card_name)
    list_data = get_list_id_based_on_name(board_id, list_name)
    if (list_data['id'] != card_details['list_id']):
        move_card(card_details['id'], list_data['id'])
        logging.info("Moved card {} to {}".format(member_name, list_name))
        comment_card(card_details['id'], list_name, member_name, False)
        logging.info("Commented on card")


def assignment_part_2(board_name, card_name, list_name):
    """
    :param board_name: Trello board name
    :param card_name: Card name, which is to be moved/commented
    :param list_name: List name to which card is to be moved
    :return:
    """
    member_name = get_member_details()['fullName']
    board_id, cards_list = get_all_cards(board_name)
    card_details = get_card_details(cards_list, card_name)
    list_data = get_list_id_based_on_name(board_id, list_name)  # get rejected list id
    if (list_data['id'] == card_details['list_id']):
        comment_card(card_details['id'], list_name, member_name, True)
    else:
        move_card(card_details['id'], list_data['id'])
        comment_card(card_details['id'], list_name, member_name, False)


def assignment_2(board_name, list_name, team_mates):
    """
    :param board_name: Trello board name
    :param list_name: List names in the board
    :param team_mates: Team mates whose card is to be created
    :return:
    """
    board_id = check_board_exists(board_name)
    if not board_id:
        board_id = create_board(board_name)

    list_mapper = check_list_exists(board_id)
    if not list_mapper:
        list_mapper = create_lists(board_id, list_name)

    card_exist = check_card_exists(board_id, team_mates)
    if not card_exist:
        create_cards(team_mates, list_mapper)

    move_all_card(list_mapper, board_id)



def main():
    for list_name in MOVE_TO_LIST_ORDER:
        assignment_part_1(BOARD_NAME, LOGGED_USER_CARD_NAME, list_name)
    assignment_part_2(BOARD_NAME, REJECTED_CARD_NAME, REJECTED_LIST_NAME)
    assignment_2(CUSTOM_BOARD_NAME, CUSTOM_LIST_NAMES, TEAM_MATES)


if __name__ == '__main__':
    main()
