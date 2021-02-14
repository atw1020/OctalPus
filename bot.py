"""

Author: Arthur Wesley

"""

import discord

import utils
import constants


def create_bot():
    """

    creates a bot

    :return: instantiated bot
    """

    client = discord.Client()

    @client.event
    async def on_ready():
        """

        initialization method

        :return:
        """

        # get the emoji channel
        emote_react_channel = client.get_channel(constants.reaction_emotes_channel_id)

        # clear the channel
        history = [item async for item in emote_react_channel.history()]
        await emote_react_channel.delete_messages(history)

        # send the base message
        message = await emote_react_channel.send(constants.react_message)

        # react to the message with all color reactions
        emote_dict = utils.mk_color_to_emote_dict(client.emojis)

        # go through all of the colors and react to the message with them
        for color in constants.color_roles:
            # add the reaction
            await message.add_reaction(emote_dict[color])

    @client.event
    async def on_message(message):
        """

        message response

        :param message:
        :return:
        """

        # check to see if the message is in #game-codes
        if message.channel.id == constants.game_codes_channel_id:
            if not utils.string_has_code(message.content) and not message.author.bot:

                # send a warning message
                await message.channel.send(constants.game_codes_warning.format(user=message.author.mention))

        # Mod Specific Commands
        if message.content == ".channel":

            # respond with a message with the channel ID
            await message.channel.send("this channel's ID is " + str(message.channel.id))

    @client.event
    async def on_reaction_add(reaction, user):
        """

        respond to a user adding a reaction

        :param reaction: emote that was reacted with
        :param user:
        :return:
        """

        print(user, "reacted with", reaction.emoji.name)

        if type(reaction.emoji) != str:
            emote_name = reaction.emoji.name
        else:
            emote_name = reaction.emoji

        if utils.is_react_message(reaction.message) and not user.bot:

            if utils.is_react_message(reaction.message):

                # check to see if the emote is a role
                if emote_name in constants.color_roles:

                    # remove all of the other reactions to this message this user has
                    reactions = reaction.message.reactions

                    # go through all the reactions
                    for _reaction in reactions:

                        if _reaction is not reaction:
                            # if this isn't the new reaction, remove it
                            await _reaction.remove(user)

                    # get the server this happened on
                    guild = reaction.message.guild

                    # create a roles dictionary for the roles on that server
                    roles_dict = utils.mk_color_to_role_dict(guild.roles)

                    # remove the user's color based roles
                    await utils.remove_color_roles(user)

                    # add the role for this emote
                    await user.add_roles(roles_dict[emote_name])

                else:
                    # if it's not a color reaction, remove the message

                    await reaction.remove(user)

    @client.event
    async def on_raw_reaction_remove(payload):
        """

        respond to an emote being removed

        :param payload: reaction event payload
        :return: None
        """

        # get the guild and user
        guild = client.get_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)

        await utils.remove_color_roles(user)

    return client


def run_bot(bot):
    """

    runs a bot

    :param bot: bot to run with the token
    :return:
    """

    # get the token from token.txt
    token = utils.get_token()

    bot.run(token)


def main():
    """

    main method

    :return:
    """

    bot = create_bot()
    run_bot(bot)


if __name__ == "__main__":
    main()
