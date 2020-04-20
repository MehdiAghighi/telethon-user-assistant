import sys
from classes import classes
from Vendor.Client import client, config
from Vendor.Logger import Logger
import importlib


class Parse:
    def __init__(self, command, event):
        self.command = command
        self.event = event
        self.attributes = {
            "del": "y",
            "log": "y"
        }
        self.module = None
        self.logMessage = None
        # self.commandObject = None

    async def parseCommand(self):
        # Split attributes into array
        options = self.command.split(' -')
        # Getting Command from attributes
        self.command = options[0][2:].lower()
        # Removing command from attributes
        options.pop(0)
        # Importing The Command Class
        try:
            self.module = importlib.import_module(
                'commands.' + classes[self.command])
        except Exception as err:
            raise Exception(f'`{self.command}` is not defined as a command')
            pass
        # adding each option to self.attributes
        for option in options:
            optionKeyValuePair = option.split('=')
            self.attributes[optionKeyValuePair[0]] = optionKeyValuePair[1]
        # Making An Instance Of Command class
        self.commandObject = getattr(
            self.module,
            classes[self.command])(self.event, self.attributes, self.command)
        # self.commandObject = self.commandObject(self.event, self.attributes)

    async def executeCommand(self):
        # Parsing Global Attributes
        await self.parseAttributes()
        # Deleting Command Message If `del` attribute is true
        if self.attributes['del'] == True:
            await client.delete_messages(self.event.chat_id, self.event.id)
        # Execute The Command
        executionStatus = await self.commandObject.execute()
        if executionStatus:
            await client.send_message(
                int(config['GENERAL']['LOG_CHANNEL']),
                f"Execution Succeded\nEvent: `{getattr(self, 'event').id}`",
            )
        else:
            await client.send_message(
                int(config['GENERAL']['LOG_CHANNEL']),
                f"Execution Status Is Unknown\nEvent: `{getattr(self, 'event').id}`",
            )

    async def parseAttributes(self):
        await self.parseDelAttribute()
        await self.parseLogAttribute()

    async def parseDelAttribute(self):
        if self.attributes['del'] == "y":
            self.attributes['del'] = True
        else:
            self.attributes['del'] = False

    async def parseLogAttribute(self):
        if self.attributes['log'] == "y":
            self.attributes['log'] = True
        else:
            self.attributes['log'] = False
