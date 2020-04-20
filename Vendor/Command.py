from Vendor.Client import client, config
from Vendor.Logger import Logger

from datetime import timedelta


class Command:
    # def __init__(self):

    async def init__(self):
        for key, value in self.myAttributes.items():
            try:
                self.attributes[key]
                setattr(self, key, self.attributes[key])
            except Exception:
                # If Attribute is required to be entered by user
                if value == '__req':
                    # Log Error
                    await self.logError(
                        f'Attribute `{key}` is required for command: `{self.command}`',
                        -1
                    )
                else:
                    # Setting `self.key` and attributes['key'] to value
                    self.attributes[key] = value
                    setattr(self, key, value)
        # Logging The Command With it's Attributes
        attrs = ''.join(f"  {key} : {value}\n" for key,
                        value in self.attributes.items())
        logger = Logger(
            f"Sent `{self.command}` Command in `{self.event.chat_id}`\n"
            f"Event: `{self.event.id}`\n"
            f"Attributes:\n"
            f"```"
            f"{'{'}\n"
            f"{attrs}"
            f"{'}'}\n"
            f"```"
        )
        if self.attributes['log']:
            await logger.log(True, False)

    async def sendMessageToChatProperty(self, message, link_preview=False, reply_to=None):
        await client.send_message(
            self.toChat,
            message,
            link_preview=link_preview,
            reply_to=reply_to
        )

    async def logError(self, message, level):
        level = "Error" if level == -1 else "Warning" if level == 0 else "Info"
        await client.send_message(
            'me',
            f"{level}: {message}\nThrown in command: `{self.command}`",
            schedule=timedelta(seconds=10 if level == 'Error' else 0)
        )
        if level == "Warning":
            await client.send_message(
                int(config['GENERAL']['LOG_CHANNEL']),
                f"Execution Completed With a Warning\nEvent: `{getattr(self, 'event').id}`",
            )
        if level == "Error":
            raise Exception('Request Denied Due To an Error')
