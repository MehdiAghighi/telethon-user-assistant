# Telethon User Assistant

telethon user assistant is somthing like a simple command line interface for telegram clients written in telethon

## Commands
in this project a command is exactly same with ones you write in cmd and starts with `!!`, like this:
```
!!id -to=me -bt=y -link=n -log=y -del=n
```
### Id 
id is a built-in command to get the numeric `chat_id` or `user_id` of a chat or user and then as you see there are some attributes:

`to`: this means where the id should be sent: values for this attribute can be `me`(saved messages),`here`(in the chat),`ch`(a channel that you should give the id)
and it also can be a user, group, channel, megagroup numeric id or username.

`bt`: if the backthicks should be used before and after the id to make it nicer

`link`: if the name of user or chat should be linked to it

`log`: if the command should be logged

`del`: if the command message itself should be deleted

## How To make a command
now which you now how do commands work in this project maybe you wanna build some commands that gets some attributes on your own.

to make a command you should create a file under `Commands` Directory for example, we are going to build `!!id` command again together so we will create a file under `commands/Id.py` directory
next you should create a class (every name you want)

then go to `classes.py` file and add the command text and class name in it for example we want the `!!id` command to call `Id` class so we should do like this:
```
classes = {
    "id": "Id",
}
```
notice that the key is command text and the value is name of the class that should be called

### Your Command class should inherit from `Command` class in Vendor Folder
```python
from Vendor.Command import Command

class Id(Command):
```

and also you can import `client` from `Vendor.client`

you should have the `__init__` method in your class.
your `__init__` should look like this
```python
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
```
`self.myAttributes` should have all command attributes in it with their default value for example here `link` attribute's default in `n`
your class should have all values in `myAttributes` as a property for example if we have a `to` property in `myAttributes` the class should have a `self.to` property which the `to` attribute's value goes in that

so now we have all values for `to`, `link` and `bt` in our class that are accessible via `self`

you can have all your own class props too for example here we have a `self.toChat` that is not a command attribute

## Command Execution
after all of this you should have some logic for your command in our example we need to get user's id and send it to `to` attribute`

you can define your login in `execute` method in your class for example we have this:
```python
# Calling The parent init__ method
async def execute(self):
        # Calling The parent init__ method
        await self.init__()
        # Event Object
        event = self.event
        # Parsing All Attributes
        await self.parseAttributes()
        # The Chat That Message Should Go to (Get It from toChatId which is set in parseToAttribute)
        self.toChat = await client.get_entity(self.to)
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
      
```

### Important: you should call `self.init__` at top of every execution method

you may ask where is `self.sendMessageToChatProperty` method is coming from? this method is defined in the parent `Command` class and if you have `to` attribute in your command it will send the message you give to it.

`execute` method should return True in case of success and False if something failed.

you can also have some attribute parsing Logic if you want for example watch this:
```python
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
```

and you can call them at the top of your `execute` method
```python
await self.parseToAttribute()
await self.parseLinkAttribute()
await self.parseBtAttribute()
```

you may ask yourself, "so what about `del` and `log` attributes?" 
those attributes are global and defined in `Vendor/Parse.py` file. i am not gonna explain how they work because they are a part of code that there is no need to change them for you. if you want to have some more global attributes you can look at the codes.


# Author
[Mehdi Aghighi](https://t.me/mehdi_n8)

# Inspiration
[Telethon](https://github.com/LonamiWebs/Telethon)
