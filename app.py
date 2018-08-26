from flask import Flask, request, abort
from bs4 import BeautifulSoup
import wikipedia
import goslate
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

helpmessage = """----------- คำสั่งปกติ -----------
/id
/bio
/name
/pic
/idline [id line]
----------- คำสั่งพิเศษ -----------
/shorturl [URL]
/news (text)
/yt [text]
/wiki [text]"""
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
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='สวัสดี พิพม์ /help เพื่อดูคำสั่งทั้งหมด',quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label="กดที่นี่เพื่อดูคำสั่งทั้งหมด", text="/help"))])))
	
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ LEAVE GROUP OR ROOM ]==========[ ARSYBAI ]======================
    if "/yt" in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
        data = url.json()
        no = 0
        result = "╔══〘 Youtube Search 〙"
        for anu in data["videos"]:
            no += 1
            result += "\n╠ {}. {}\n║Link: {}".format(str(no),str(anu["title"]),str(anu["webpage"]))
        result += "\n╚══〘 Total {} Result 〙".format(str(len(data["videos"])))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    """if text == "/news":
        try:
            user_agent = {'User-agent': 'Mozilla/5.0'}
            url = requests.get("https://newsapi.org/v2/top-headlines?country=th&apiKey=763b6fc67a594a4e9e0f9d29303f83dd")
            data = url.json()
            result="ข่าวเกี่ยวกับ " + search
            for anu in data["articles"]:
                if len(result) > 500:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
                else:
                    result+="\n\n" + anu["title"] + "\n"+anu["url"]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
        except Exception as Error:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=Error))"""
    if "/news" in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        r = requests.get("http://www.google.co.th/search?q="+search+"&tbm=nws")
        content = r.text
        news_summaries = []
        soup = BeautifulSoup(content, "html.parser")
        st_divs = soup.findAll("div", {"class": "st"})
        trs="ข่าวเกี่ยวกับ " + search
        for st_div in st_divs:
            news_summaries.append(st_div.text)
        for i in news_summaries:
            try:
                if len(trs) > 500:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=trs))
                else:
                    gs = goslate.Goslate()
                    x = gs.translate(i,'th')
                    trs+="\n\n"+x+"\nอ่านเพิ่มเติมได้ที่"
            except Exception as error:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=trs))
    if text == "/bye":
        if(event.source.user_id == "Udaa0a2f396dd41e4398b106d903d92fd"):
            confirm_template_message = TemplateSendMessage(
                alt_text='God message',
	    		template=ConfirmTemplate(
                    text='จะลบบอทออก? คุณแน่ใจหรือ?',
                    actions=[
                        PostbackAction(
                            label='แน่ใจ',
                            text='goodbye',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='ไม่',
                            text='...'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, confirm_template_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ผู้ใช้นี้ไม่ได้รับอนุญาตให้"))
    if '/wiki ' in text:
        try:
            wiki = text.replace("/wiki ","")
            wikipedia.set_lang("th")
            pesan="หัวข้อ "
            pesan+=wikipedia.page(wiki).title
            pesan+="\n\n"
            pesan+=wikipedia.summary(wiki, sentences=1)
            pesan+="\n\nอ่านเพิ่มเติม\n"
            pesan+=wikipedia.page(wiki).url
            titlex = wikipedia.page(wiki).title
            textx = wikipedia.summary(wiki, sentences=1)
            urlx = wikipedia.page(wiki).url
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pesan))
        except:
            try:
                pesan="เกินขีด จำกัด ข้อความ! โปรดคลิกลิงก์ข้างล่างเพื่ออ่านเพิ่มเติม\n"
                pesan+=wikipedia.page(wiki).url
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pesan))
            except Exception as e:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(e)))
    if text == '/id':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == '/bio':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == '/pic':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == '/name':
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
    if text == 'goodbye':
        if(event.source.user_id == "Udaa0a2f396dd41e4398b106d903d92fd"):
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
    
    elif "/idline " in event.message.text:
        skss = event.message.text.replace('/idline ', '')
        sasa = "http://line.me/R/ti/p/~" + skss
        text_message = TextSendMessage(text=sasa)
        line_bot_api.reply_message(event.reply_token, text_message)
	
    elif '/shorturl' in text:
        originURLx = text.split(" ")
        originURL = text.replace(originURLx[0] + " ","")
        result = requests.get("http://pasun.cf/api/urlshorten.php?url=" + originURL + "&type=api").text
        buttons_template_message = TemplateSendMessage(
            alt_text='God message',
            template=ButtonsTemplate(
                thumbnail_image_url='https://gamingroom.co/wp-content/uploads/2017/11/CyCYOArUoAA2T6d.jpg',
                title='RESULT',
                text=result,
                actions=[
                    PostbackAction(
                        label='ข้อมูล URL',
                        text='/check ' + result,
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label="URL",
                        text=result
                    ),
                    MessageAction(
                        label="URL",
                        text=result
                    ),
                    URIAction(
                        label='เปิด URL',
                        uri=result
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
		
    elif '/help' in text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=helpmessage))
		
    elif '/test' in text:
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='God message',
                actions=[
                    PostbackAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
	











#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
