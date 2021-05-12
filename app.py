# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# package
import re
from datetime import datetime 

# customer module
#import mongodb
import corwler

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('your_api_key')
# 必須放上自己的Channel Secret
handler = WebhookHandler('your_token')

#line_bot_api.push_message('Uc11e2f0ebc9a2ca445c73f8c698f88f2', TextSendMessage(text='您好！我是南山萬事通，很高興認識你～我可以幫助你得到南山人壽相關資訊喔！'))

# 監聽所有來自 /callback 的 Post Request
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

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    當收到使用者訊息的時候
    '''
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    message = event.message.text

    
    if re.search('Hi|hello|你好|ha', message, re.IGNORECASE):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = event.message.text + ', ' + name)) #加上人名
        
        return 0 

    # 傳送圖片
    elif event.message.text == '圖片':
        message = ImageSendMessage(
            original_content_url='https://i.imgur.com/Q8CgRpX.jpg',
            preview_image_url='https://i.imgur.com/Q8CgRpX.jpg'
        )

    # 傳送位置
    elif event.message.text == '地點':
        message = LocationSendMessage(
            title='公司所在位置',
            address='南山金融中心',
            latitude=25.031794,
            longitude=121.561091
        )
    # 傳送貼圖
    elif event.message.text == '貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

    elif re.search('聯合報|udn', event.message.text, re.IGNORECASE):
        dic = corwler.udn_news()
        columns = []
        for i in range(0,5):
            carousel = CarouselColumn(
                        thumbnail_image_url = dic[i]['img'],
                        title = dic[i]['title'],
                        text = dic[i]['summary'],
                        actions=[
                            URITemplateAction(
                                label = '點我看新聞',
                                uri = dic[i]['link']
                              )
                            ]
                        )
            columns.append(carousel)
        
        remessage = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(columns=columns)
                    )
        
        
        line_bot_api.reply_message(event.reply_token, remessage)
        return 0 
    
    elif re.search('中央社|cna', event.message.text, re.IGNORECASE):
        dic = corwler.cna()
        columns = []
        for i in range(0,5):
            carousel = CarouselColumn(
                        thumbnail_image_url = 'https://i.imgur.com/vkqbLnz.png',
                        title = dic[i]['title'],
                        text = dic[i]['summary'],
                        actions=[
                            URITemplateAction(
                                label = '點我看新聞',
                                uri = dic[i]['link']
                              )
                            ]
                        )
            columns.append(carousel)
        
        remessage = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(columns=columns)
                    )
        
        
        line_bot_api.reply_message(event.reply_token, remessage)
        return 0 
        
    elif re.search('Dcard|dcard', event.message.text, re.IGNORECASE):
        text = corwler.Dcard()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))
        return 0 
    
    elif re.search('news|新聞', event.message.text, re.IGNORECASE):
        text = corwler.nanshan_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))
        return 0 
    
    elif re.search('天氣|氣象|weather', event.message.text, re.IGNORECASE):
        radar_url = corwler.weather()
        message = ImageSendMessage(
            original_content_url= radar_url,
            preview_image_url=radar_url
            )
        line_bot_api.push_message(uid, message)
        return 0 
   
#    if re.search('商品|product', event.message.text, re.IGNORECASE):
#        text = '商品資訊如下：' + '\n' + 'https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/8'
#        line_bot_api.reply_message(
#            event.reply_token,
#            TextSendMessage(text=text))
#        return 0 
    
    elif re.search('商品|product', event.message.text, re.IGNORECASE):
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/Q8CgRpX.jpg',
                title='商品分類',
                text='Please select',
                actions=[
                    URITemplateAction(
                        label='壽險保障',
                        uri='https://www.nanshanlife.com.tw/NanshanWeb/product/10'
                    ),
                    URITemplateAction(
                        label='保險理財',
                        uri='https://www.nanshanlife.com.tw/NanshanWeb/product/17'
                    ),
                    URITemplateAction(
                        label='醫療保障',
                        uri='https://www.nanshanlife.com.tw/NanshanWeb/product/24'
                    ),
#                    URITemplateAction(
#                        label='旅行險專區',
#                        uri='https://www.nanshanlife.com.tw/promotion/travel/index.htm'
#                    ),      
                    URITemplateAction(
                        label='投資型商品專區',
                        uri='http://ilp.nanshanlife.com.tw/'
                    )                             
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, message)
        return 0 
    
    elif re.search('常見問題|QA|qa', event.message.text, re.IGNORECASE):
#        text = 'https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/347'
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/TIP68IM.png',
                        title='理賠服務',
                        text='申請方式、作業流程、給付方式',
                        actions=[
                            URITemplateAction(
                                label='申請方式',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/104'
                            ),
                            URITemplateAction(
                                label='作業流程',
                                uri='https://www.nanshanlife.com.tw/PublicWeb/Service/file/AM/process.pdf'
                            ),
                            URITemplateAction(
                                label='給付方式',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/108'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/U2ghV3H.png',
                        title='保單服務',
                        text='契約變更、保單借款、終止契約',
                        actions=[
                            URITemplateAction(
                                label='契約變更',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/85'
                            ),
                            URITemplateAction(
                                label='保單借款',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/90'
                            ),
                            URITemplateAction(
                                label='終止契約',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/97'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/GQjUNi0.png',
                        title='繳費服務',
                        text='金融機構轉帳、信用卡轉帳、自行繳費',
                        actions=[
                            URITemplateAction(
                                label='金融機構轉帳',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/99'
                            ),
                            URITemplateAction(
                                label='信用卡轉帳',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/100'
                            ),
                            URITemplateAction(
                                label='自行繳費',
                                uri='https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/101'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        return 0 
    
    elif re.search('服務據點', event.message.text, re.IGNORECASE):
        text = '客服中心:0800-020-060' + '\n' + '\n' + 'https://www.nanshanlife.com.tw/NanshanWeb/static-sidebar/73'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))
        return 0 
    
    elif re.search('保單查詢', event.message.text, re.IGNORECASE):
        text = '請先登入會員才能進行相關後續動作喔～⬇︎' + '\n' + 'https://www.nanshanlife.com.tw/CESIDP/sso/AllInOne.action?spId=CP&utm_source=internal&utm_medium=link_insured&utm_campaign=Officalsite_floatlogin&utm_content=Officalsite_floatlogin'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))
        return 0 
    else:
        message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text))
    return 0 
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
