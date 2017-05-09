from __future__ import print_function
from __future__ import unicode_literals
from janis import Janis
from rtmbot.core import Plugin, Job
from slackclient import SlackClient

JANIS_API_KEY = ""
JANIS_CLIENT_KEY = ""
janis = Janis(JANIS_API_KEY,JANIS_CLIENT_KEY,'slack')


class janisListener():
    def __init__(self, plugin):
        def onChatResponse(self, args):
            print('on_chat_response_response', args)
            channel = args["channel"]
            text = args["text"]
            plugin.outputs.append([channel, text])
        
        janis.on('chat_response', onChatResponse)
        
        def onChannelUpdate(self, args):
            print('on_channel_update', args)
        
        janis.on('channel_update', onChannelUpdate)
        janis.start()



class janisPlugin(Plugin):
    
    def process_message(self, data):

        hopInResponse = janis.hopIn(data)
        # If your bot is paused, stop it from replying
        if hopInResponse.get('paused'):
           return "Success"
        
        def sendIt(channel, text):
            self.outputs.append([channel, text])
            janis.hopOut({'channel':channel, 'text':text})
        
        channel = data['channel']
        text = data['text']
        
        if (text == 'hi' or text == 'hello'):
            sendIt(channel, 'Hello there.')
        elif (text == "help" or text == "operator"):
            # send a janis alert to your slack channel
            # that the user could use assistance
            janis.assistanceRequested(data);
            # let the user know that they are being routed to a human
            sendIt(channel, 'Hang tight. Let me see what I can do.')

        # otherwise log an unknown intent with janis
        else:
            # capture conversational 'dead-ends'.
            janis.logUnknownIntent(data)
            # let the user know that the bot does not understand
            sendIt(channel, 'Huh?')
                
    def register_jobs(self):
        janisListener(self)
