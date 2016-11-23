import bot.protocols.IRC.client as irc
import bot.protocols.mumble.client as mumble
import asyncio
from bot.plugins.food import plugin as food


def main():
    # load configurations
    # load connections
    # connect to them

    #irc_conn = irc.IrcClient("JanisBot4")
    #irc_coro = loop.create_connection(lambda: irc_conn.protocol, "open.ircnet.net", 6667)

    mumble_client = mumble.MumbleClient("Janisbot4", "mumina1")
    foodplugin = food.FoodPlugin()
    mumble_client.register_event_listener(foodplugin)

    mumble_client.start("terisikk.dy.fi", 64738)
    

    #loop.run_until_complete(irc_coro)

    mumble_client.join_channel("Paskaneekeri")

    loop.run_forever()

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    main()
