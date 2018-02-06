#!/usr/bin/env python3


#export SLACK_BOT_TOKEN=Bot User OAuth Access Token

import os
import time
import re
#import json #used for debug printing
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


def main():
    if slack_client.rtm_connect():
        print('RepeaterBot has gone online...')
        while True:
            print(msg_echo)
            msg_echo = slack_client.rtm_read()
            for update in msg_echo:
                print('Update found...')
                if 'type' in update and update['type'] == 'message':
                    slack_client.rtm_send_message(update['channel'], update['text'])
            time.sleep(1)
    else:
        print("Connection Failed...")

if __name__ == '__main__':
    main()
