from Vendor.Client import client
from Vendor.Command import Command
import sys


class Id(Command):
    def __init__(self, event, attributes, command):
        # User Given Attributes
        self.attributes = attributes
        # All Command Attributes
        self.myAttributes = {
            # you should the default value or `__req` string for user required attributes
            "to": "ch",
            "link": "y",
            "bt": "n"
        }
        # Event property
        self.event = event
        # Command property
        self.command = command
        # All Attributes Properties
        self.to = None
        self.link = None
        self.bt = None
        # Your Own Properties
        self.toChatId = None
        self.toChat = None

    async def parseAttributes(self):
        # Parsing Attributes one by one
        await self.parseToAttribute()
        await self.parseLinkAttribute()
        await self.parseBtAttribute()

    async def execute(self):
        # Calling The parent init__ method
        await self.init__()
        # Event Object
        event = self.event
        # Parsing All Attributes
        await self.parseAttributes()
        # The Chat That Message Should Go to (Get It from toChatId which is set in parseToAttribute)
        self.toChat = await client.get_entity(self.toChatId)
        # Get The Chat That Message is sent in
        chat = await event.get_chat()
        # Get The last message from the chat
        try:
            async for message in client.iter_messages(chat, limit=1):
                last_message = message
        except:
            await self.logError(f"Can't get the lass message of this chat", 0)
            pass
        # If Message Is Sent In Private Group
        if event.is_private:
            # Send ID of person to 'toChatId' Property
            await self.sendMessageToProperty(
                chat.first_name,
                chat.id,
            )
            return True
        # If The message if in channel,group,supergroup
        if event.is_group or event.is_channel:
            # if message is replyed to another message
            if event.is_reply:
                # get the message that command is replyed to
                replyed_to = await event.get_reply_message()
                # get the replyed person entity
                replyed_user = await client.get_entity(replyed_to.from_id)
                # Send ID of replyed person to 'toChatId' Property
                await self.sendMessageToProperty(
                    replyed_user.first_name,
                    replyed_user.id,
                )
                return True
            else:
                # Send ID for of chat to 'toChatId' Property
                await self.sendMessageToProperty(
                    chat.title,
                    chat.id,
                    c_type=1,
                    last_message_id=last_message.id
                )
                return True
        return False

    # Sending message to `toChatId` property
    async def sendMessageToProperty(self, name, chat_id, c_type=0, last_message_id=None):
        # if there is a last_message_id ( means that message is in the group )
        if c_type == 1:
            if last_message_id != None:
                await self.sendMessageToChatProperty(
                    f"{f'[{name}](https://t.me/c/{str(chat_id)}/{str(last_message_id)})' if self.link else f'{name}'} : {'`' if self.bt else ''}{str(chat_id)}{'`' if self.bt else ''}")
            else:
                await self.sendMessageToChatProperty(
                    f"{name} : {'`' if self.bt else ''}{str(chat_id)}{'`' if self.bt else ''}")
        # if sending id of a user
        else:
            await self.sendMessageToChatProperty(
                f"{f'[{name}](tg://user?id={str(chat_id)})' if self.link else f'{name}'} : {'`' if self.bt else ''}{str(chat_id)}{'`' if self.bt else ''}")

    async def parseToAttribute(self):
        toAttribute = self.to
        # If the 'to' attribute is here send it to event.chat_id
        if toAttribute == 'here':
            self.toChatId = self.event.chat_id
            return
        # If the 'to' attribute is ch send it to channel
        if toAttribute == 'ch':
            self.toChatId = 1372737953
            return
        # If the 'to' attribute is me send it to saved messages
        if toAttribute == 'me':
            self.toChatId = "me"
            return

        # If The 'to' attirbute is none of the predefined values
        try:
            # Get entity with string toAttribute (Can be Chat Id)
            self.toChat = await client.get_input_entity(int('-100' + toAttribute))
            self.toChatId = int('-100' + toAttribute)
            return
        except:
            pass
        try:
            # Get entity with string toAttribute (Can be Chat Id)
            self.toChat = await client.get_input_entity(int(toAttribute))
            self.toChatId = int(toAttribute)
            return
        except:
            pass
        try:
            # Get entity with string toAttribute (Can be Username)
            self.toChat = await client.get_input_entity(toAttribute)
            self.toChatId = toAttribute
            return
        except:
            await self.logError(
                f"Valid Values For `to` Property is a Chat id, username, `here`, `me` or `ch`",
                -1
            )

    async def parseLinkAttribute(self):
        if self.link.lower() == "y":
            self.link = True
        else:
            self.link = False

    async def parseBtAttribute(self):
        if self.bt.lower() == "y":
            self.bt = True
        else:
            self.bt = False
