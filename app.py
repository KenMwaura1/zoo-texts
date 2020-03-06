import os
from flask import Flask, render_template, request
import africastalking
import pandas as pd
import json
import requests
import pendulum
from pandas.io.json import json_normalize
from text_class import Text
# from datetime import date
from settings import Session, Base, engine
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

prod_name = os.getenv("PROD_NAME")
prod_apikey = os.getenv("PROD_APIKEY")
# africastalking.initialize(username, apikey)
africastalking.initialize(str(prod_name), str(prod_apikey))
sms = africastalking.SMS
print(prod_apikey, prod_name)

# This is one of the route where Twitch expose data,
# They have many more: https://dev.twitch.tv/docs
endpoint = "https://api.twitch.tv/helix/streams?"
client_id = os.getenv("TWITCH_Client_ID")
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


def is_live(stream): return stream.get('type') == 'live'


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


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        sms_message = request.form['smsMessage']
        phone_number = request.form['phoneNumber']

        print(sms_message)

        phone_number1 = os.getenv("phone_number1")
        phone_number = [phone_number]
        print(phone_number)

        response = sms.send(sms_message, phone_number)
        data = json.dumps(response)
        # n = json.loads(response)
        print(response)
        # print(data)
        # print(n)

        nj = json_normalize(response)
        # print(nj)
        '''
        for row in nj.itertuples():
            print(row.Index,row._1[''],'\n')
            print(row._2)
        '''
        for index, row in nj.iterrows():
            print('Message', '=>', row['SMSMessageData.Message'])
            print('Recipients', '=>', row['SMSMessageData.Recipients'])
            m = row['SMSMessageData.Message']

            for r in row['SMSMessageData.Recipients']:
                print(r['statusCode'], '=>', r['status'],
                      'cost :', '=>', r['cost'])
                stc = r['statusCode']
                st = r['status']
                costs = r['cost']
                numbers = r['number']
                messageids = r['messageId']
                print(m, stc, st, costs, numbers, messageids, sep='\n')

                Base.metadata.create_all(engine)

                # create new session
                session = Session()

                text1 = Text(m, stc, numbers, costs, st,
                             messageids, pendulum.now())

                session.add(text1)
                session.commit()
                session.close()

    return render_template('index.html')


@app.route("/home", methods=["GET", "POST"])
def home():
    live = convert(streams_active)
    print('-' * 10, 'home')
    print(live)
    return render_template("home.html")


@app.route("/login")
def sg():
    return render_template("signin.html")


@app.route("/base")
def bd():
    return render_template("base.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
