"""
This bot listens to port 5016 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
from janis import Janis
import json

app = Flask(__name__)


ACCESS_TOKEN = ''
VERIFY_TOKEN = ''
JANIS_API_KEY = ''
JANIS_CLIENT_KEY = ''
bot = Bot(ACCESS_TOKEN)
janis = Janis(JANIS_API_KEY,JANIS_CLIENT_KEY,'messenger', ACCESS_TOKEN)

def onChatResponse(self, args):
    try:
        print('janis chat_response args:' + str(args))
        channel = args["channel"]
        text = args["text"]
        bot.send_text_message(channel, text)
    except Exception as e:
        print(e, sys.exc_info())

janis.on('chat_response', onChatResponse)


def onChannelUpdate(self, args):
    try:
        print('janis channel_update args:' + str(args))
    except Exception as e:
        print(e, sys.exc_info())
    
janis.on('channel_update', onChannelUpdate)


@app.route("/", methods=['GET', 'POST'])


def hello():
    def sendIt(channel, text):
        response = bot.send_text_message(channel, text)
        messageData = {'recipient': {'id': channel},'message': {'text': text}}
        janis.hopOut(messageData)

    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        print(output)
        
        for event in output['entry']:
            messaging = event['messaging']
            for messageData in messaging:
                j = json.dumps(messageData)
                hopInResponse = janis.hopIn(messageData)
                
                if messageData.get('message'):
                    # If your bot is paused, stop it from replying
                    if hopInResponse.get('paused'):
                        return "Success"
                    recipient_id = messageData['sender']['id']
                    if messageData['message'].get('text'):
                        message = messageData['message']['text']
                        if message == 'hi':
                            sendIt(recipient_id, 'Hello there.')
                        elif message == 'help':
                            # let the user know that they are being routed to a human
                            sendIt(recipient_id, 'Hang tight. Let me see what I can do.')
                            # send a janis alert to your slack channel
                            # that the user could use assistance
                            janis.assistanceRequested(messageData)
                        else:
                            # let the user know that the bot does not understand
                            sendIt(recipient_id, 'Huh?')
                            # capture conversational dead-ends.
                            janis.logUnknownIntent(messageData)
                                
                    if messageData['message'].get('attachment'):
                        bot.send_attachment_url(recipient_id, messageData['message']['attachment']['type'],
                                                messageData['message']['attachment']['payload']['url'])
                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=5016, debug=True)

