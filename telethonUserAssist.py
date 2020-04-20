from Vendor.Client import client
from Vendor.Client import config

from telethon import TelegramClient, events, types, functions, sync
from datetime import timedelta

import socks
import asyncio

import sys


from Vendor.Parse import Parse


async def raiseError(err, level=-1):
    level = "Error" if level == -1 else "Warning" if level == 0 else "Info"
    if level == "Error":
        await client.send_message(
            'me',
            f"{level}: {err}",
            schedule=timedelta(seconds=10)
        )
    else:
        await client.send_message(
            'me',
            f"{level}: {err}",
        )


async def main():

    # @events.register(events.NewMessage(func=lambda event: event.message.from_id == 777000))
    # async def messageFromTelegram(event):
    #     if 'Login code:' in event.raw_text:
    #         # await client.forward_messages(473546383, int(event.message.id))
    #         await event.forward_to("Mehdi_N8")

    @events.register(events.NewMessage(outgoing=True))
    async def newCommand(event):
        if event.raw_text.startswith('!!'):
            commandOut = Parse(event.raw_text, event)
            try:
                await commandOut.parseCommand()
                await commandOut.executeCommand()
            except Exception as err:
                await raiseError(err)
                await client.send_message(
                    int(config['GENERAL']['LOG_CHANNEL']),
                    f"Execution Failed With An Error\nEvent: `{event.id}`",
                )
                return

    await client.start()
    await client.get_dialogs()
    client.add_event_handler(newCommand)


# client.add_event_handler(newCommand)
# client.start()
# client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()


# @events.register(events.NewMessage(outgoing=True, func=lambda event: event.raw_text.startswith('!!')))
# async def newMessageSent(event):
#     await client.delete_messages(event.chat_id, event.id)
#     command = event.raw_text[2:]
#     user = await event.get_chat()
#     if command == 'id':
#         if event.is_private:
#             await client.send_message(1372737953, "[" + user.first_name + "]" + "(" + "https://t.me/" + user.username + ")" + " : " + "`" + str(user.id) + "`", link_preview=False)
#             return
#         if event.is_reply:
#             replyed_message = await event.get_reply_message()
#             replyed_user = await client.get_entity(replyed_message.from_id)
#             await client.send_message(1372737953, "[" + replyed_user.first_name + "]" + "(" + "https://t.me/" + replyed_user.username + ")" + " : " + "`" + str(replyed_user.id) + "`", link_preview=False)
#             return
#         if event.is_channel:
#             print(user.stringify())
#             await client.send_message(1372737953, user.title + " : " + "`" + str(user.id) + "`", link_preview=False)
#             return
#         if event.is_group:
#             await client.send_message(1372737953, user.title + " : " + "`" + str(user.id) + "`", link_preview=False)
#             return


# @events.register(events.MessageRead(func=lambda e: e.is_private))
# async def messageRead(event):
#     user = await event.get_chat()
#     message = await client.get_messages(user, ids=event.max_id)
#     await client.send_message(1372737953, "[" + user.username.capitalize() + "]" + "(" + "https://t.me/" + user.username + ")" + " Has Read My Message " + "👇", link_preview=False)
#     await message.forward_to(1372737953)


# @events.register(events.NewMessage())
# async def newMessage(event):
#     print(await event.get_chat())

# client.start()
# client.add_event_handler(newMessageSent)
# client.add_event_handler(messageRead)
# # client.add_event_handler(newMessage)
# client.run_until_disconnected()
