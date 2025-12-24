import os
import re
from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()

from flask import Flask, request, Response
from helper.openai_api import Conversation
from twilio.twiml.messaging_response import MessagingResponse

Conversations = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__, static_folder=os.path.join(BASE_DIR, "static"), static_url_path="/static"
)


@app.route("/", methods=["GET"])
def home():
    return "program is all well and  running "


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

            msg = resp.message()
            msg.media(
                "https://raw.githubusercontent.com/shaliss-bots/whatsappsg-ai-bot/main/src/static/logo.png"
            )
            resp.message("shaliss AI*\n" "hi welcome!\n" "GOD BLESS YOU")

        else:
            reply = conv.prompt_response(message)

    except Exception as e:
        import traceback

        traceback.print_exc()
        resp.message("Something went wrong")

    return Response(str(resp), mimetype="application/xml")
