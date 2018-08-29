from flask import Flask, request, abort
from bs4 import BeautifulSoup
import wikipedia
import goslate
from gtts import gTTS
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
line_bot_api = LineBotApi('rQExLm1oTVReucXgIHa6uo1KQta5jCK7nluqcmhiKTecHcMppL9WCFvnawJ+suZVfJ+gGK/sFwWR99MUcdvo+0C4qVNEKWqHg0t40ogdYYBpiFf8fLDuvnNzZ+gpR4fjvIMsGMl146TOPSVe6rjzgwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('439f983b3872dcb6e04a41caa2260171')
#===========[ NOTE SAVER ]=======================
notes = {}

mimic = {
    "target":{}
}

helpmessage = """----------- Normal order -----------
/id
/bio
/name
/pic
/idline [ Offline ]
/contact

----------- Special Order -----------
/shorturl [ URL ]
/check [ ID URL ]
/news ( Country )
/snews [ message ]
/yt [ message ]
/wiki [ message ]"""
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
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Hello /help To see all orders',quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label="Click here to view all orders.", text="/help"))])))
	
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
        result = "Search"
        for anu in data["videos"]:
            no += 1
            result += "\n{}. {}\n{}".format(str(no),str(anu["title"]),str(anu["webpage"]))
        result += "\nall{}".format(str(len(data["videos"])))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if "/news" in text:
        try:
            separate = text.split(" ")
            country = text.replace(separate[0] + " ","")
            if(separate == None):country == "th"
            user_agent = {'User-agent': 'Mozilla/5.0'}
            url = requests.get("https://newsapi.org/v2/top-headlines?country={}&apiKey=763b6fc67a594a4e9e0f9d29303f83dd".format(country))
            data = url.json()
            result="New Releases"
            for anu in data["articles"]:
                if len(result) > 500:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
                else:
                    result+="\n" + anu["title"] + "\n"+anu["url"]+"\n"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
        except Exception as Error:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=Error))
    if "/snews" in text:
        separate = text.split(" ")
        searchx = text.replace(separate[0] + " ","")
        search = searchx
        gs = goslate.Goslate()
        search = gs.translate(searchx,'en')
        r = requests.get("http://www.google.co.th/search?q="+search+"&tbm=nws")
        content = r.text
        news_summaries = []
        soup = BeautifulSoup(content, "html.parser")
        st_divs = soup.findAll("div", {"class": "st"})
        g_divs = soup.findAll("div", {"class": "g"})
        trs="News about " + searchx
        news_d = []
        for g_div in g_divs: 
            news_d.append(g_div.text)
        for st_div in st_divs:
            news_summaries.append(st_div.text)
        for i in news_summaries:
            for x in news_d:
                try:
                    if len(trs) > 600:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=trs))
                    else:
                        gs = goslate.Goslate()
                        x = gs.translate(x,'en')
                        trs+="\n\n"+x+"\nRead more at"
                except Exception as error:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=trs))
    if text == "/bye":
        if(event.source.user_id == "U2c7d1341178eed8c93c23e914cbcb6a0"):
            confirm_template_message = TemplateSendMessage(
                alt_text='God message',
	    		template=ConfirmTemplate(
                    text='Will remove the bot? Are you sure?',
                    actions=[
                        PostbackAction(
                            label='sure',
                            text='goodbye',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='Not',
                            text='...'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, confirm_template_message)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="This user is not allowed."))
    if "/ti/g/" in text:
        link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
        links = link_re.findall(text)
        n_links = []
        for l in links:
            if l not in n_links:
                n_links.append(l)
        for ticket_id in n_links:
            group = line_bot_api.findGroupByTicket(ticket_id)
            line_bot_api.acceptGroupInvitationByTicket(group.id,ticket_id)
    if text == '/contact':
        buttons_template_message = TemplateSendMessage(
            alt_text='God message',
            template=ButtonsTemplate(
                thumbnail_image_url='https://gamingroom.co/wp-content/uploads/2017/11/CyCYOArUoAA2T6d.jpg',
                title='Contact',
                text='contact',
                actions=[
                    PostbackAction(
                        label='Line',
                        text='http://line.me/ti/p/~1535915621_',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label="Facebook",
                        text='https://www.facebook.com/DPunisher'
                    ),
                    URIAction(
                        label='Contact',
                        uri='http://line.me/ti/p/~1535915621_'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='http://images4.fanpop.com/image/photos/15800000/Animes-anime-cuties-15887436-1400-875.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://line.me/ti/p/~esci_', label='@')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='PASUNx', weight='bold', size='xl'),
                    # review
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Bangkok, Thailand',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="00:00 - 23:59",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='contact', uri="https://line.me/ti/p/~esci_")
                    )
                ]
            ),
        )
        #message = FlexSendMessage(alt_text="God message", contents=bubble)
        #line_bot_api.reply_message(
        #    event.reply_token,
        #    buttons_template_message
        #)
    if '/wiki ' in text:
        try:
            wiki = text.replace("/wiki ","")
            wikipedia.set_lang("en")
            pesan="Wikipedia About"
            pesan+=wikipedia.page(wiki).title
            pesan+="\n\n"
            pesan+=wikipedia.summary(wiki, sentences=1)
            pesan+="\n\nRead more\n"
            pesan+=wikipedia.page(wiki).url
            titlex = wikipedia.page(wiki).title
            textx = wikipedia.summary(wiki, sentences=1)
            urlx = wikipedia.page(wiki).url
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pesan))
        except:
            try:
                pesan="Over limit message! Please click the link below to read more.\n"
                pesan+=wikipedia.page(wiki).url
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=pesan))
            except Exception as e:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(e)))
    if text == "/kick":
        line_bot_api.kickoutFromGroup(0, event.source.group_id, "Udaa0a2f396dd41e4398b106d903d92fd")
    if text == "/2kick":
        line_bot_api.kickoutFromGroup(event.source.group_id, "u541bbaba15d68f3a652106a0de5a3e94")
    if text == "/3kick":
        line_bot_api.kickoutFromGroup(0, event.source.group_id, "u541bbaba15d68f3a652106a0de5a3e94")
    if text == "/4kick":
        line_bot_api.kickoutFromGroup(event.source.group_id, "Udaa0a2f396dd41e4398b106d903d92fd")
		
    if text == '/gid':
        profile = line_bot_api.get_profile(event.source.user_id)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.display_name))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.group_id))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.picture_url))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=profile.status_message))
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
        if(event.source.user_id == "U2c7d1341178eed8c93c23e914cbcb6a0"):
            if isinstance(event.source, SourceGroup):
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text='Outgoing...'))
                    line_bot_api.leave_group(event.source.group_id)
            elif isinstance(event.source, SourceRoom):
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text='Outgoing...'))
                line_bot_api.leave_room(event.source.room_id)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="The bot can not leave chat. 1:1 have"))
    
    elif "/idline " in event.message.text:
        skss = event.message.text.replace('/idline ', '')
        sasa = "http://line.me/R/ti/p/~" + skss
        text_message = TextSendMessage(text=sasa)
        line_bot_api.reply_message(event.reply_token, text_message)
    elif '/check' in text:
        originURLx = text.split(" ")
        originURL = text.replace(originURLx[0] + " ","")
        result = requests.get("http://shorturlbyzefyrinusx.000webhostapp.com/api/check.php?id=" + originURL + "&type=api").text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    elif '/shorturl' in text:
        originURLx = text.split(" ")
        originURL = text.replace(originURLx[0] + " ","")
        result = requests.get("http://shorturlbyzefyrinusx.000webhostapp.com/api/urlshorten.php?url=" + originURL).text
        buttons_template_message = TemplateSendMessage(
            alt_text='God message',
            template=ButtonsTemplate(
                thumbnail_image_url='https://gamingroom.co/wp-content/uploads/2017/11/CyCYOArUoAA2T6d.jpg',
                title='RESULT',
                text=result,
                actions=[
                    PostbackAction(
                        label='information URL',
                        text='/check ' + result,
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label="URL",
                        text=result
                    ),
                    URIAction(
                        label='turns on URL',
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
