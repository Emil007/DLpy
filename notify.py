import configparser
from pushover import Client
from pushbullet import Pushbullet

def send_notification(message):
    config = configparser.ConfigParser()
    config.read('notify.ini')

    # Send notifications via Pushover
    pushover_sections = [section for section in config.sections() if section.startswith('Pushover')]
    for section in pushover_sections:
        pushover_config = config[section]
        user_key = pushover_config['user_key']
        api_token = pushover_config['api_token']
        client = Client(user_key, api_token=api_token)
        client.send_message(message)

    # Send notifications via Pushbullet
    pushbullet_sections = [section for section in config.sections() if section.startswith('Pushbullet')]
    for section in pushbullet_sections:
        pushbullet_config = config[section]
        access_token = pushbullet_config['access_token']
        pb = Pushbullet(access_token)
        push = pb.push_note("New Death", message)
