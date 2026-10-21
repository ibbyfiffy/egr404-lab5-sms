"""OPTIONAL lab5 SMS bot reference. Merge with your current sms_bot.py after review.

Requires: flask twilio openai python-dotenv requests werkzeug.
Uses SQLite to persist subscriber opt-in status. Twilio's Messaging Service may
handle STOP/START automatically; verify and coordinate with that behavior.
"""
import os
import sqlite3
from pathlib import Path
from flask import Flask, request, Response
from dotenv import load_dotenv
from openai import OpenAI
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from werkzeug.middleware.proxy_fix import ProxyFix
from spotify_client import search_tracks

load_dotenv()
app = Flask(__name__)
# Use exactly one trusted ngrok proxy for X-Forwarded-Proto, not arbitrary headers.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
client = OpenAI()
DB_PATH = Path(__file__).with_name("subscribers.sqlite3")
BRAND = "lab5"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS subscribers (phone TEXT PRIMARY KEY, opted_in INTEGER NOT NULL)")


def opted_in(phone):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT opted_in FROM subscribers WHERE phone = ?", (phone,)).fetchone()
    return bool(row and row[0])


def set_opt_in(phone, is_opted_in):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO subscribers (phone, opted_in) VALUES (?, ?) "
                     "ON CONFLICT(phone) DO UPDATE SET opted_in=excluded.opted_in",
                     (phone, int(is_opted_in)))


def interpret_mood(message):
    result = client.responses.create(
        model="gpt-4.1-mini",
        instructions=("Interpret the user's mood or activity as a Spotify track "
                      "search query. Reply with only 2-5 short genre/mood words."),
        input=message,
    )
    return result.output_text.strip()


def sms_reply(message):
    twiml = MessagingResponse()
    twiml.message(message)
    return Response(str(twiml), mimetype="text/xml")


@app.route("/sms", methods=["POST"])
def sms():
    signature = request.headers.get("X-Twilio-Signature", "")
    if not validator.validate(request.url, request.form, signature):
        return "Invalid Twilio signature", 403

    sender = request.form.get("From", "").strip()
    body = request.form.get("Body", "").strip()
    if not sender:
        return "Missing sender", 400
    command = body.upper()
    if command in ("STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"):
        set_opt_in(sender, False)
        # Twilio's Advanced Opt-Out may suppress your TwiML response here.
        return sms_reply(f"{BRAND}: You are unsubscribed. Reply START to opt in again.")
    if command in ("START", "UNSTOP"):
        set_opt_in(sender, True)
        return sms_reply(
            f"{BRAND}: You're subscribed to on-demand Spotify suggestions. "
            "Message frequency varies. Msg & data rates may apply. "
            "Reply HELP for help or STOP to unsubscribe."
        )
    if command == "HELP":
        return sms_reply(
            f"{BRAND}: Text how you're feeling for Spotify suggestions. "
            "Reply STOP to opt out or START to join. "
            "Support: ibrahim.tahoun@uri.edu"
        )
    if not opted_in(sender):
        return sms_reply(f"{BRAND}: To receive recommendations, review our website and reply START to opt in. Reply HELP for help.")
    if not body:
        return sms_reply(f"{BRAND}: Tell me your mood or activity to get song suggestions.")
    try:
        query = interpret_mood(body)
        tracks = search_tracks(query, limit=3)
        if not tracks:
            return sms_reply(f"{BRAND}: No matching tracks found. Try describing another mood. Reply STOP to opt out.")
        lines = [f"{BRAND}: Songs for {query}:"]
        for song in tracks:
            lines.append(f"{song['name']} — {song['artist']}\n{song['url']}")
        lines.append("Reply STOP to opt out or HELP for help.")
        return sms_reply("\n\n".join(lines))
    except Exception:
        app.logger.exception("Recommendation failed")
        return sms_reply(f"{BRAND}: Sorry, the music service is unavailable. Please try again later.")


if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
