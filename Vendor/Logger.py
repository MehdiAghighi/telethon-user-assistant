from Vendor.Client import client, config
from datetime import timedelta
# from Vendor.Client import config


class Logger:
    def __init__(self, message):
        self.message = message

    async def log(self, telegram, note):
        if telegram:
            try:
                await self.logToTelegram()
            except Exception as err:
                await self.logError(
                    f"Log to telegram channel failed", -1)
                await self.logError(f"{err}", -1)

        if note:
            # TODO: Ability For Logging To txt File
            return

    async def logToTelegram(self):
        await client.send_message(
            int(config['GENERAL']['LOG_CHANNEL']),
            f"{self.message}")

    async def logError(self, message, level):
        level = "Error" if level == -1 else "Warning" if level == 0 else "Info"
        await client.send_message(
            'me',
            f"{level} : {message}\nThrown in Action: `Logging`",
            schedule=timedelta(seconds=10 if level == 'Error' else 0)
        )
        if level == "Error":
            raise Exception('Request Denied Due To an Error')
