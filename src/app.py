import os
import re
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, Response
from helper.openai_api import Conversation

from helper.twilio_api import send_message

Conversations = {}

app = Flask(__name__)


@app.route("/" , methods=["GET"])
def home():
    return "program is all well and running"


@app.route("/twilio/receiveMessage", methods=["POST"])
def receiveMessage():
    try:
        message = request.form["Body"]
        sender_id = request.form["From"]  # whatsapp:+919685168546

        conversation_id = re.sub(r"\w+", "", sender_id, 0, re.IGNORECASE)

        conv = Conversations.get(conversation_id)

        if conv is None:
            conv = Conversation(
                api_key=os.getenv("OPENAI_API_KEY"), conversation_id=conversation_id
            )
            Conversations[conversation_id] = conv

        response = conv.prompt_response(message)

        # Twilio sandbox sender number

        sender_number = "whatsapp:+14155238886"  # Twilio sandbox

        # Send reply back to user

        twiml = f"<Response><Message>{response}</Message></Response>"
        return Response(twiml, mimetype="application/xml")

    except Exception as e:

        import traceback
    traceback.print_exc()
    return Response("<Response></Response>", mimetype="application/xml")


def send_message(sender_number, sender_id, response):
    twiml = f"<Response><Message>{response}</Message></Response>"
    return Response(twiml, mimetype="application/xml")
