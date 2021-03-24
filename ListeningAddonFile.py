import os
import re
import sqlite3
import requests
import string
import datetime


def find_files(filename, search_path):
    """
    Search for the path like : 'D:Blizzard\World of Warcraft\_retail_\WTF\Config.wtf'
    :param filename:
    :param search_path:
    :return list_file:
    """

    list_file = []

    # Wlaking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            list_file.append(os.path.join(root, filename))
    return list_file


def refine_files(list_file):
    """
    Change URL path from 'D:Blizzard\World of Warcraft\_retail_\WTF\Config.wtf' to 'D:Blizzard\World of Warcraft\_retail_\WTF\'
    :param list_file:
    :return file:
    """
    file = str
    for element in list_file:
        index = list_file.index(element)
        file = element.replace('Config.wtf', '')
        list_file[index] = file
    return file


def search_folder_path(path):
    """
    Add Account to path and search for the account folder. Current path is 'D:Blizzard\World of Warcraft\_retail_\WTF\Account\[ID ACCOUNT]'
    :param path:
    :return path:
    """
    folder_list = os.listdir(path + 'Account\\')
    for folder in folder_list:
        if 'SavedVariables' not in folder:
            path = path + 'Account\\' + folder + '\\'
            return path


def search_realmlist(PATH):
    """
    Search for realm list
    :param PATH:
    :return list of all realm folder:
    """
    folder_list = os.listdir(PATH)

    return [
        folder
        for folder in folder_list
        if not re.search("[.]\w+", folder) and 'SavedVariables' not in folder
    ]


def search_character(realm_list, PATH):
    """
    Search for character name's of all realm list
    :param PATH:
    :param realm_list:
    :return list of all realm folder and charac list:
    """
    dict_char = {}
    for realm in realm_list:
        char_list = os.listdir(PATH + realm)
        dict_char[realm] = char_list
    return dict_char, realm_list


def save_path(path_to_account):
    """
    Write the current path into a file for the next time
    :param path_to_account:
    """
    with open("config.txt", 'w+') as write_in_file:
        write_in_file.write(path_to_account)


def sending_keys():
    """
    Send keys to discord
    """
    cur.execute("SELECT * FROM mythic_key")
    content = cur.fetchall()
    cur.close()

    data = {
        "embeds": [
            {
                "title": "Global keys",
                "fields": [
                    {
                        "name": 'Personnages',
                        "value": '\n'.join(
                            i[0] + " - " + i[1] for i in content
                        ),
                        "inline": 'true',
                    },
                    {
                        "name": 'Donjon',
                        "value": '\n'.join(i[2] for i in content),
                        "inline": 'true',
                    },
                    {
                        "name": 'Level',
                        "value": '\n'.join(f"+{i[3]}" for i in content),
                        "inline": 'true',
                    },
                ],
                "color": 7741329,
                "timestamp": str(datetime.datetime.now()),
            }
        ],
        "username": "Esclave Purotin",
    }

    url = 'PASTE YOUR WEBHOOK URL HERE'
    requests.post(url, json=data, headers={"Content-Type": "application/json"})


def search_addon_file(dict_char, path_to_account):
    """
    Insert or update new data into database and call sending_keys() if data changed
    :param dict_char:
    :param path_to_account:
    """
    global cur
    changed = 0
    for realm in dict_char:
        for char in dict_char[realm]:
            if 'SavedVariables' in os.listdir(
                    f"{path_to_account + realm}\\{char}") and "Mythic_Keystone_Tracker.lua" in os.listdir(
                    f"{path_to_account + realm}\\{char}\\SavedVariables"):

                # Read the lua file : list object
                with open(f"{path_to_account + realm}\\{char}\\SavedVariables\\Mythic_Keystone_Tracker.lua", 'r',
                          encoding='utf8') as read_lua:
                    keystone = read_lua.read()

                keystone = keystone.split('\n')
                dungeon = keystone[1].split('"')
                level = keystone[2].split(' ')

                conn = sqlite3.connect(r'.\wow_mythic_keys.db')
                cur = conn.cursor()
                cur.execute(
                    "SELECT * FROM mythic_key")
                is_exist = cur.fetchall()
                cur.close()

                is_name_present = 0
                is_dungeon_present = 0
                for name in is_exist:
                    if char == name[0] and realm == name[1]:
                        is_name_present = 1
                        if dungeon[1] in name[2] and str(level[2]) in str(name[3]):
                            is_dungeon_present = 1

                conn = sqlite3.connect(r'.\wow_mythic_keys.db')
                cur = conn.cursor()

                if 'name = nil' not in dungeon:
                    if is_name_present == 1:
                        if is_dungeon_present != 1:
                            cur.execute(
                                'UPDATE mythic_key SET dungeon_name = ?, dungeon_level = ? WHERE charac_name = ? ',
                                (dungeon[1], level[2], char))
                            changed = 1

                    else:

                        cur.execute(
                            'INSERT INTO mythic_key VALUES (?, ?, ?, ?)', (char, realm, dungeon[1], level[2]))
                        changed = 1

                    conn.commit()
                    cur.close()

    if changed == 1:
        sending_keys()


try:
    with open("config.txt", 'r') as read_file:
        path_to_account = read_file.read()
    realm_list = search_realmlist(path_to_account)
    dict_char, realm_list = search_character(realm_list, path_to_account)

    search_addon_file(dict_char, path_to_account)

except:
    for letter in string.ascii_uppercase:
        wow_folder_path = find_files('Config.wtf', f'{letter}:')
        if wow_folder_path:
            wow_folder_path_refined = refine_files(wow_folder_path)
            path_to_account = search_folder_path(wow_folder_path_refined)
            save_path(path_to_account)
            realm_list = search_realmlist(path_to_account)
            dict_char, realm_list = search_character(realm_list, path_to_account)
            search_addon_file(dict_char, path_to_account)