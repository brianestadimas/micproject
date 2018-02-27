from flask import Flask, request, abort
from dotenv import load_dotenv, find_dotenv
from wit import Wit
import os
import musixmatchAPI as lirik_api

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
	MessageEvent,
	TextMessage,
	TextSendMessage,
	ButtonsTemplate,
	TemplateSendMessage,
	PostbackTemplateAction,
	MessageTemplateAction,
	URITemplateAction,
	ImageCarouselTemplate,
	ImageCarouselColumn,
	CarouselTemplate,
	CarouselColumn
)

app = Flask(__name__)
load_dotenv(find_dotenv())

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

##WITAI BOT##
client = Wit(os.environ.get('WIT_ACCESS_TOKEN'))

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: {}'.format(body))

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if ('/help' in event.message.text):
		reply_message = TemplateSendMessage(
			alt_text='Message not supported',
			template=ButtonsTemplate(
				title='Helper',
				text='Please select action',
				actions=[
					MessageTemplateAction(
						label='/lirik',
						text='/lirik'
					),
					MessageTemplateAction(
						label='Cari lirik berdasarkan judul',
						text='/lagu'
					),
					MessageTemplateAction(
						label='Cari lirik berdasarkan artis',
						text='/artis'
					),
					MessageTemplateAction(
						label='Cari lirik berdasarkan penggalan lirik',
						text='/sublirik'
					),
					URITemplateAction(
						label='Go to website',
						uri='http://example.com/'
					)
				]
			)
		)

	############## FORMAT UDAH DIRAPIHIN DIMAS #################	

	elif ('/lirik' in event.message.text):
		if (len(event.message.text.split("-"))<3):
			reply_message = TextSendMessage(text='Ketik /lirik-(judul)-(artis), contoh : /lirik-raisa-mantan terindah')
		else :
			reply_message = TextSendMessage(text=lirik_api.getLyricsByTrackArtist(event.message.text.split("-")[1], event.message.text.split("-")[2]))
			

	elif ('/lagu' in event.message.text):
		if (len(event.message.text.split("-"))<2):
			reply_message = TextSendMessage(text='Ketik /lagu-(judul), contoh : /lagu-mantan terindah')
		else :
			result = lirik_api.getTracksWithTrack(event.message.text.split("-")[1])
			reply_message = TemplateSendMessage(
    			alt_text='Pilih artis dan judul yang sesuai',
    			template=CarouselTemplate(
        			columns=[
            			CarouselColumn(
                			title=result[i].get("track").get("artist_name"),
                			text=result[i].get("track").get("artist_name")+"-"+result[i].get("track").get("track_name"),
                			actions=[
                    			MessageTemplateAction(
	                        		label="Pilih Ini",
    	                    		text=lirik_api.getLyricsByTrackArtist(result[i].get("track").get("artist_name"),result[i].get("track").get("track_name"))
        	            		)
            	    		]
            			)
            			for i in range(len(result)%10)
        			]
    			)
			)
	elif ('/artis' in event.message.text):
		if (len(event.message.text.split("-"))<2):
			reply_message = TextSendMessage(text='Ketik /artis-(nama), contoh : /artis-raisa')
		else :
			reply_message = TextSendMessage(text=lirik_api.getLyricsByTrackArtist(event.message.text.split("-")[1], event.message.text.split("-")[2]))
	
	elif ('/sublirik' in event.message.text):
		if (len(event.message.text.split("-"))<2):
			reply_message = TextSendMessage(text='Ketik /sublirik-(potonganlagu), contoh : /sublirik-ketika ku mendengar bahwa')
		else :
			#ini
			result = lirik_api.getTracksWithSubLyrics(event.message.text.split("-")[1])
			reply_message = TemplateSendMessage(
    			alt_text='Pilih artis dan judul yang sesuai',
    			template=CarouselTemplate(
        			columns=[
            			CarouselColumn(
                			title=result[i].get("track").get("artist_name"),
                			text=result[i].get("track").get("artist_name")+"-"+result[i].get("track").get("track_name"),
                			actions=[
                    			MessageTemplateAction(
	                        		label="Pilih Ini",
    	                    		text="/lirik-"+result[i].get("track").get("artist_name")+"-"+result[i].get("track").get("track_name")
        	            		)
            	    		]
            			)
            			for i in range(len(result)%10)
        			]
    			)
			)

	else:
		reply_message = TextSendMessage(text='Ketik /help untuk bantuan')

	line_bot_api.reply_message(
	event.reply_token,
	reply_message
)

if __name__ == "__main__":
	app.run()
