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


ACCESS_TOKEN = '<ACCESS_TOKEN>'
VERIFY_TOKEN = '<VERIFY_TOKEN>'
JANIS_API_KEY = '<JANIS_API_KEY>'
JANIS_CLIENT_KEY = '<JANIS_CLIENT_KEY>'
bot = Bot(ACCESS_TOKEN)
janis = Janis(JANIS_API_KEY,JANIS_CLIENT_KEY,'messenger', ACCESS_TOKEN, useWebhook=True)

@app.route("/", methods=['GET', 'POST'])

def hello():
    
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        
        for event in output['entry']:
            if event.get('messaging'):
                messaging = event['messaging']
                for messageData in messaging:
                    j = json.dumps(messageData)
                    
                    if messageData.get('message'):
                        
                        recipient_id = messageData['sender']['id']
                        if messageData['message'].get('is_echo'):
                            # See: https://developers.facebook.com/docs/messenger-platform/handover-protocol#app_roles
                            # This app should be the Primary Receiver. Janis should be a Secondary Receiver.
                            # Every time an echo from either Janis or the Page Inbox is received,
                            # this app passes control over to Janis so the humans are the only ones who can respond.
                            # Janis will pass control back to this app again after 10 minutes of inactivity.
                            # If you want to manually pass back control, use the slash command `/resume`
                            # in the Janis transcript channel, or press "Done" in the Page Inbox on the thread.
                            janis.passThreadControl(messageData)
                            return "Success"
                        if messageData['message'].get('text'):
                            message = messageData['message']['text']
                            if message == 'hi':
                                response = bot.send_text_message(recipient_id, 'Hello there!')
                            elif message == 'help':
                                # let the user know that they are being routed to a human
                                response = bot.send_text_message(recipient_id, 'Hang tight. Let me see what I can do.')
                                # send a janis alert to your slack channel
                                # that the user could use assistance
                                janis.assistanceRequested(messageData)
                            else:
                                # let the user know that the bot does not understand
                                response = bot.send_text_message(recipient_id, 'Huh?')
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

