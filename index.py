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
	ImageCarouselColumn
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
	if (event.message.text == '/help'):
		reply_message = TemplateSendMessage(
			alt_text='Message not supported',
			template=ButtonsTemplate(
				title='Helper',
				text='Please select action',
				actions=[
					MessageTemplateAction(
						label='Cari lirik lagu',
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

	elif (event.message.text[0] == '/lirik'):
		if (len(event.message.text.split("-"))<2):
			reply_message = TextSendMessage(text='Ketik /lirik-(judul)-(artis), contoh : /lirik-raisa-mantan terindah')
		else :
			reply_message = TextSendMessage(text=lirik_api.getLyricsByTrackArtist(event.message.text.split("-")[1], event.message.text.split("-")[2]))
	
	#nurul----
	elif (event.message.text[0] == '/lagu'):
		if (len(event.message.text)<1):
			reply_message = TextSendMessage(text='Ketik /lagu-(judul), contoh : /lagu-mantan terindah')
		else :
			reply_message = TemplateSendMessage(
			alt_text='Pilih judul dengan artis yang sesuai',
			template=ImageCarouselTemplate(
			columns=[
				(ImageCarouselColumn(
					image_url='https://via.placeholder.com/800x800', action=MessageTemplateAction(
						label= result[i].get("track").get("track_name") + ' - ' + result[i].get("track").get("artist_name"),
						text= '1'+ result[i].get("track").get("track_name") + '-' + result[i].get("track").get("artist_name"),

					)
				))
				for i in range(10):
			]
		)
	)

	elif (event.message.text[0] == '/artis'):
		if (len(event.message.text)<2):
			reply_message = TextSendMessage(text='Ketik /artis-(nama), contoh : /artis-raisa')
		else :
			reply_message = TextSendMessage(text=lirik_api.getLyricsByTrackArtist(event.message.text.split("-")[1], event.message.text.split("-")[2]))
	
	elif (event.message.text[0] == '/sublirik'):
		if (len(event.message.text)<2):
			reply_message = TextSendMessage(text='Ketik /sublirik-(potonganlagu), contoh : /sublirik-ketika ku mendengar bahwa')
		else :
			reply_message = TextSendMessage(text=lirik_api.getLyricsByTrackArtist(event.message.text.split("-")[1], event.message.text.split("-")[2]))

	else:
		reply_message = TextSendMessage(text='Ketik /help untuk bantuan')

	line_bot_api.reply_message(
	event.reply_token,
	reply_message
)

if __name__ == "__main__":
	app.run()

