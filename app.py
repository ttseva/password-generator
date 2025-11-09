from flask import Flask, request, jsonify
import telebot
import random
import string
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

settings = {
    "default_length": 12,
    "include_digits": True,
    "include_specials": True
}


##################################################

def generate_password(length=None, include_digits=None, include_specials=None):
    length = length or settings["default_length"]
    if include_digits is None:
        include_digits = settings["include_digits"]
    if include_specials is None:
        include_specials = settings["include_specials"]

    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    if include_specials:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?/"

    return ''.join(random.choice(chars) for _ in range(length))


##################################################

##### получить настройки
@app.route("/settings", methods=["GET"])
def get_settings():
    return jsonify(settings)


##### изменить настройки
@app.route("/settings", methods=["PUT"])
def update_settings():
    data = request.json
    if "default_length" in data:
        settings["default_length"] = int(data["default_length"])
    if "include_digits" in data:
        settings["include_digits"] = bool(data["include_digits"])
    if "include_specials" in data:
        settings["include_specials"] = bool(data["include_specials"])
    return jsonify({"status": "ok", "settings": settings})


##################################################

##### сгенерировать парлль
@app.route("/password", methods=["POST"])
def password():
    data = request.json or {}
    length = data.get("length")
    include_digits = data.get("include_digits")
    include_specials = data.get("include_specials")
    pwd = generate_password(length, include_digits, include_specials)
    return jsonify({"password": pwd})


##### отправить парлль

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    chat_id = data.get("chat_id")
    text = data.get("text")

    if not chat_id or not text:
        return jsonify({"error": "chat_id и text обязательны"}), 400

    bot.send_message(chat_id, text, parse_mode="HTML")
    return jsonify({"status": "ok", "sent_text": text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
