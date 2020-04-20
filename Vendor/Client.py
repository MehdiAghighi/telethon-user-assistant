from telethon import TelegramClient, events, types, functions, sync
import socks
import configparser
import logging
from os import path, getcwd

# Set the location of the script
script_dir = path.abspath(path.join(path.dirname(__file__), '..'))

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Loading Environment varriables
config = configparser.ConfigParser()
config.read(path.join(script_dir, "config.ini"))


client = TelegramClient(
    path.join(script_dir, "Assist"),
    config['ACCOUNT']['API_ID'],
    config['ACCOUNT']['API_HASH'],
    proxy=(socks.SOCKS5, '127.0.0.1',
           8383) if config['GENERAL']['USE_PROXY'] == "TRUE" else False
)
