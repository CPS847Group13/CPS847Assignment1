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

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return matches.group(2).strip() if matches else None

def main():
    if slack_client.rtm_connect():
        print('RepeaterBot has gone online...')
        while True:
            msg_echo = slack_client.rtm_read()
            print(msg_echo)
            for update in msg_echo:
                print('Update found...')
                if 'type' in update and update['type'] == 'message':
                    #slack_client.rtm_send_message(update['channel'], update['text'])
                    message = parse_direct_mention(update["text"])
                    slack_client.rtm_send_message(update["channel"], message)
            time.sleep(1)
    else:
        print("Connection Failed...")

if __name__ == '__main__':
    main()
