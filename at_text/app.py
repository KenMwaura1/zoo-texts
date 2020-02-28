import os
from flask import Flask, render_template, request
import africastalking
import pandas as pd
import json
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
africastalking.initialize(prod_name, prod_apikey)
sms = africastalking.SMS


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        sms_message = request.form['smsMessage']
        phone_number = request.form['phoneNumber']

        print(sms_message)

        phone_number1 = ['+254719702373']
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


@app.route("/login")
def sg():
    return render_template("signin.html")


@app.route("/base")
def bd():
    return render_template("base.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
