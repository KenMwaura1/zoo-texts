import requests
from app.settings import TWITCH_SETTINGS, TWILIO_SETTINGS
from twilio.rest import Client

# This is one of the route where Twitch expose data,
# They have many more: https://dev.twitch.tv/docs
endpoint = "https://api.twitch.tv/helix/streams?"
client_id = TWITCH_SETTINGS["client_id"]
# print(client_id)

# In order to authenticate we need to pass our api key through header
headers = {"Client-ID": client_id}

# In order to get a response we need to pass parameters
params = {"game_id": "33214"}

# It is now time to make the actual request
response = requests.get(endpoint, params=params, headers=headers)
# print(response.json())

json_response = response.json()

# We get only Streams
streams = json_response.get('data', [])
# print(streams)

# Create a lambda function to get only live streams
is_live = lambda stream: stream.get('type') == 'live'
streams_active = list(filter(is_live, streams))

# Atleast one stream active
atleast_one_stream_active = any(streams_active)
print(atleast_one_stream_active)

live_user = []


def convert(streams_a):
    live_ls = []
    for stream in streams_a:
        user_name = stream['user_name']
        title = stream['title']
        viewer_count = stream['viewer_count']
        live_list = [user_name, viewer_count]
        live_ls.append(live_list)
    global live_user
    for live in live_ls:
        live_user.append(live)
    print(live_user)
    print('-' * 10, 'live users')
    return live_ls


print(convert(streams_active))
print('--' * 20, 'global live users')
print(live_user)

account_sid = TWILIO_SETTINGS['ACCOUNT_SID']

auth_token = TWILIO_SETTINGS['AUTH_TOKEN']
twilio_client = Client(account_sid, auth_token)
trial_number = '+12162598374'
real_number = '+254750233428'
#muchiri = '+254743226448'
'''
twilio_client.messages.create(
    body=str(live_user), from_=trial_number, to=real_number)
'''
last_messages_sent = twilio_client.messages.list(limit=2)
if last_messages_sent:
    last_message_id = last_messages_sent[0].sid
    last_message_data = twilio_client.messages(last_message_id).fetch()
    last_message_content = last_message_data.body
    online_notified = "LIVE" in last_message_content
    offline_notified = not online_notified
else:
    online_notified, offline_notified = False, False

if atleast_one_stream_active and not online_notified:
    twilio_client.messages.create(body=str(live_user) + '' ' are LIVE playing Fornite !!!', from_=trial_number, to=real_number)
if not atleast_one_stream_active and not offline_notified:
    twilio_client.messages.create(body='OFFLINE !!!', from_=trial_number, to=real_number)
print(twilio_client.messages(last_message_data.body))