from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_PASSWORD = getenv("SENDER_PASSWORD")  
RECEIVER_EMAIL = getenv("RECEIVER_EMAIL")

server = Flask(__name__)
CORS(server)

@server.route('/', methods=['GET'])
def default():
    return jsonify({ "status" : "good" }), 200

@server.route('/sendmessage', methods=['POST'])
def addData():
    data = dict(request.get_json())
    try : 
        body = data['message'] + "\n\n" + "From: " + data['name'] + "\n" + "Email: " + data['email']
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = data["subject"]
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
            
            server.quit()
            return jsonify({ "status" : "good" }), 200

        except Exception as e:
            return jsonify({ "status" : "bad"}), 500
    except Exception as e:
        return jsonify({ "status" : "bad" }), 500

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)  