from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('mIbLskZ5WICInTfM8omKsuBf0T9gPmd4CnExNyZYF9A3gRWHis83SiJeuJdP/ORXco3ECH13n4WqdPfWBuQXdfPBsqeNoFf0O8y6pvzq0orNgxBiBc38Apv7SQolAP5WQz0AsLJcEGoZC3YZQMTJPAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5e0bb8077fbec9c4a14217ebeb653371')
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Welcome'))
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ LEAVE GROUP OR ROOM ]==========[ ARSYBAI ]======================
    if text == "/test":
        member_ids_res = line_bot_api.get_group_member_ids(event.source.group_id)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=member_ids_res.member_ids))
    if text == '/bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='กำลังออกกลุ่ม...'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='กำลังออกกลุ่ม...'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="บอทไม่สามารถออกแชท 1:1 ได้"))

    elif 'gambar' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        r = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(search))
        data = r.text
        data = json.loads(data)

        if data["result"] != []:
            items = data["result"]
            path = random.choice(items)
            a = items.index(path)
            b = len(items)

        image_message = ImageSendMessage(
            original_content_url=path,
            preview_image_url=path
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )
    
    elif '/shorturl' in text:
        originURLx = text.split(" ")
        originURL = text.replace(originURLx[0] + " ","")
        result = requests.get("http://pasun.cf/api/urlshorten.php?url=" + originURL + "&type=api").text
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=843),
            selected=False,
            name="URL SHORTENR",
            chat_bar_text=result,
            areas=[RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                action=URIAction(label='Contact', uri='https://line.me/ti/p/~esci_'))]
        )
		line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))












#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
