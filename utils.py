"""

Author: Arthur Wesley

"""

import string

import constants
from english_words import english_words_set


async def remove_color_roles(user):
    """

    removes all color based roles from a user

    :param user: the user to remove the roles from
    :return: None
    """

    # get the color color_roles
    color_roles = get_color_roles(user.roles)

    # remove all of the users old color roles
    for role in color_roles:
        await user.remove_roles(role)


def get_token():
    """

    get the discord bot token

    :return: discord bot token
    """

    with open("token.txt") as file:
        return file.read().strip()


def string_has_code(message):
    """

    check to see if a given string is a code

    :param message: string to look for game codes in
    :return: Boolean: does the string contain a code
    """

    # start by converting the message to lowercase
    message = message.lower()

    # replace the delimiters with spaces
    for punctuation in string.punctuation:
        message = message.replace(punctuation, " ")

    words = message.split(" ")

    # go through all of the words
    for word in words:

        # check to see if the word's length is 6 and not an english word
        if len(word) == 6 and word not in english_words_set:
            return True

    # return the result
    return False


def get_color_roles(roles):
    """

    generate a list of all the users with color color_roles

    :param roles: color_roles a user has
    :return: a list of all the color color_roles they possess
    """

    to_remove = []

    for role in roles:

        if role.name not in constants.color_roles:
            to_remove.append(role)

    for role in to_remove:
        roles.remove(role)

    return roles


def mk_color_to_role_dict(roles):
    """

    makes a Dictionary that maps from names of roles to roles (colors in our case)

    :param roles: roles to create a dictionary for
    :return: dictionary that maps from role names to roles
    """

    return {role.name: role for role in roles}


def mk_color_to_emote_dict(emotes):
    """

    makes a dictionary that maps from names

    :param emotes: list of the server's emotes
    :return: dictionary that maps from emote names to emotes
    """

    return {emote.name: emote for emote in emotes}


def is_react_message(message):
    """

    determines if a given message object is the role reactions message

    :param message: message to check
    :return: boolean: is the message as expected
    """

    return message.author.bot and message.channel.id == constants.reaction_emotes_channel_id


if __name__ == "__main__":
    print(string_has_code("this is a;test!APLGZF"))
    print("better" in english_words_set)
