#!/usr/bin/env python
"""
A basic script used to consume the Path of Exile public stash tab api and find items based on a search parameter.
"""
import re
import requests
__name__ = '__main__'


def main():
    url = 'http://www.pathofexile.com/api/public-stash-tabs'
    head = {'Content-type': 'application/json', 'Accept-Encoding': 'gzip'}
    next_change_id = get_next_change_id(head)
    search_param = input('Please enter an item name: ').strip().upper()

    parse_river(url, head, next_change_id, search_param)


def get_next_change_id(head):
    """
    Consumed the poe.ninja api for the latest next_change_id

    :return: The next_change_id
    """
    url = 'http://api.poe.ninja/api/Data/GetStats'
    result = requests.get(url, headers=head).json()
    return result['nextChangeId']


def parse_river(url, head, next_change_id, search_param):
    """
    Parses the public stash tab api river and searches for any items whose name contains the search_param

    :param url: Path of Exile public stash tab api url
    :param head: dictionary containing request headers
    :param next_change_id: the id of the api page being requested
    :param search_param: a search parameter used to limit the displayed items
    """
    while next_change_id != '0-0-0-0-0':
        result = requests.get(url + '?id=' + next_change_id, headers=head).json()
        next_change_id = result['next_change_id']
        for stash in result['stashes']:
            for item in stash['items']:
                if search_param in item['name'].upper():
                    print(get_whisper_message(item, stash))
        print('')
    print('Reached live.')


def get_whisper_message(item, stash):
    """
    Generates a trade whisper message for the found item

    :param item: dictionary containing information on the found item
    :param stash: dictionary containing information on the stash where the item was found
    :return: trade whisper message
    """
    character_name = stash['lastCharacterName']
    item_name = re.sub('<<.*?>>', '', item['name'])
    try:
        price = ' listed for ' + item['note'].replace('~b/o ', '')
    except KeyError:
        price = ''
    league = item['league']
    tab_name = stash['stash']
    left_pos = str(item['x'])
    top_pos = str(item['y'])
    return '@' + character_name + ' Hi, I would like to buy your ' + item_name + price + ' in ' + league + \
           ' (stash tab "' + tab_name + '"; position: left ' + left_pos + ', top ' + top_pos + ')'

if __name__ == '__main__':
    main()
