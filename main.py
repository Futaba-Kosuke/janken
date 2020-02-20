from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, VideoSendMessage, StickerSendMessage, AudioSendMessage
)
import os
import random

app = Flask(__name__)

#環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def hands_to_int(user_hand):
    if user_hand == 'グー':
        return 0
    elif user_hand == 'チョキ':
        return 1
    elif user_hand == 'パー':
        return 2
    else:
        return -1

def select_bot_hand():
    return random.randint(0, 2)

def judge(user_hand, bot_hand):
    judge_num = (user_hand - bot_hand) % 3
    result = ''

    if bot_hand == 0:
        result += 'グー！\n'
    elif bot_hand == 1:
        result += 'チョキ！\n'
    elif bot_hand == 2:
        result += 'パー！\n'
    else:
        result += '？？？\n'

    if judge_num == 0:
        result += 'あいこ！'
    elif judge_num == 1:
        result += '貴方の負け！'
    elif judge_num == 2:
        result += '貴方の勝ち！'
    else:
        result += 'ERROR'

    return result

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = hands_to_int(event.message.text)
    # message = str(select_bot_hand())
    message = judge(hands_to_int(event.message.text), select_bot_hand())
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
