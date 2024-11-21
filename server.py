from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from twilio.rest import Client

load_dotenv()

accountSID = getenv('TWILIO_ACCOUNT_SID')
auccAuth = getenv('TWILIO_AUTH_TOKEN')
number = getenv('TWILIO_PHONE_NO')

server = Flask(__name__)
CORS(server)
client = Client(accountSID, auccAuth)
server.debug = True

@server.route('/', methods=['POST'])
def addData():
    data = dict(request.get_json())
    try : 
        client.messages.create(
        body= f"\nName : {data['name']}\nEmail : {data['email']}\nSubject : {data['subject']}\nMessage : {data['message']}",
        from_= number,
        to = "+918459058302"
        )
        return jsonify({ "status" : "good" }), 200
    except :
        return jsonify({ "status" : "bad" }), 200

if __name__ == "__main__":
    server.run()    