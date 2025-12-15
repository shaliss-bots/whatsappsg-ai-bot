import os
import re
from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()

from flask import Flask, request, Response
from helper.openai_api import Conversation
from twilio.twiml.messaging_response import MessagingResponse

Conversations = {}

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "program is all well and running"


@app.route("/twilio/receiveMessage", methods=["POST"])
def receiveMessage():
    resp = MessagingResponse()
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

        reply = conv.prompt_response(message)
        resp.message(reply)

    except Exception as e:

        import traceback
    traceback.print_exc()
    resp.message("Something went wrong")

    return Response(str(resp), mimetype="application/xml")
