import requests
import threading
from socketIO_client import SocketIO

class Janis:
    def __init__(self, api_key, client_key, platform, *access_token, **kwargs):
        """
            @required:
                api_key
                client_key
                platform
            @optional:
                access_token
                kwargs
        """
        self.headers = {'apikey':api_key,'clientkey':client_key,'platform':platform}
        if access_token:
            self.headers['token'] = access_token[0]
            self.token = access_token[0]
        if kwargs.get('serverRoot'):
            self.serverRoot = kwargs.get('serverRoot')
        else:
            self.serverRoot = 'https://wordhopapi.herokuapp.com'
        if kwargs.get('socketServer'):
            self.socketServer = kwargs.get('socketServer')
        else:
            self.socketServer = 'https://wordhop-socket-server.herokuapp.com'
        if kwargs.get('path'):
            self.path = kwargs.get('path')
        else:
            self.path = '/api/v1/'
        if kwargs.get('useWebhook'):
            self.useWebhook = kwargs.get('useWebhook')
        else:
            self.useWebhook = false
        if kwargs.get('janisAppId'):
            self.janisAppId = kwargs.get('janisAppId')
        else:
            self.janisAppId = 1242623579085955

        self.apiUrl = self.serverRoot + self.path
        self.platform = platform
        self.clientkey = client_key

        self.start()


    def hopIn(self, x):
        response = requests.post(self.apiUrl + "in",headers=self.headers, json=x)
        result = response.json()
        return result

    def hopOut(self, x):
        response = requests.post(self.apiUrl + "out",headers=self.headers, json=x)
        result = response.json()
        return result
    
    def logUnknownIntent(self, x):
        response = requests.post(self.apiUrl + "unknown",headers=self.headers, json=x)
        return response
    def assistanceRequested(self, x):
        response = requests.post(self.apiUrl + "human",headers=self.headers, json=x)
        return response
    def passThreadControl(self, x):
        message = x['message']
        recipientID = x['recipient']['id']
        appId = message['app_id']
        if x['message'].get('is_echo') and (appId == self.janisAppId or appId is None):
            # If an agent responds via the Messenger Inbox, then `appId` will be null.
            # If an agent responds from Janis on Slack, the `appId` will be 1242623579085955.
            # In both cases, we should pause your bot by giving the thread control to Janis.
            # Janis will pass control back to your app again after 10 minutes of inactivity.
            # If you want to manually pass back control, use the slash command `/resume`
            # in the Janis transcript channel, or press "Done" in the Page Inbox on the thread.
            
            # See: https://developers.facebook.com/docs/messenger-platform/handover-protocol#app_roles
            # This app should be the Primary Receiver. Janis should be a Secondary Receiver.
            # Every time an echo from either Janis or the Page Inbox is received,
            # this app passes control over to Janis so the humans are the only ones who can respond.
            j = {"recipient": {"id": recipientID}, "target_app_id": self.janisAppId, "metadata": "passing thread"}
            uri = "https://graph.facebook.com/v2.6/me/pass_thread_control?access_token=" + self.token
            response = requests.post(uri, json=j)
            return response

    callbacks = None
        
    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}
            
            if event_name not in self.callbacks:
                self.callbacks.setdefault(event_name,[callback])
        else:
            a = self.callbacks.setdefault(event_name,[callback])
            a.append(callback)
        
    def trigger(self, event_name, args):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self, args)

    def start(self):
        def setupSocketClient():
            if self.useWebhook:
                return
            
            def on_socket_set_response(*args):
                socket_id = args[0]
                x = {'socket_id': socket_id, 'clientkey': self.clientkey}
                r = requests.post(self.apiUrl + "update_bot_socket_id",headers=self.headers, json=x)
            
            def on_chat_response_response(*args):
                channel = args[0]["channel"]
                text = args[0]["text"]
                ts = args[0]["ts"]
                ts = args[0]["ts"]
                slack_user = args[0]["slack_user"]
                team = args[0]["team"]
                if self.platform == 'messenger':
                    messageData = {'metadata':{"ts": ts , "slack_user": slack_user , "team":  team }, 'recipient': {'id': channel},'message': {'text': text}}
                else:
                    messageData = {'metadata':{"ts": ts , "slack_user": slack_user , "team":  team }, 'channel': channel, 'text': text}
                self.hopOut(messageData)
                self.trigger('chat_response', args[0])
        
            def on_channel_update_response(*args):
                self.trigger('channel_update', args[0])
            
            with SocketIO(self.socketServer) as socketIO:
                socketIO.on('chat response', on_chat_response_response)
                socketIO.on('channel update', on_channel_update_response)
                socketIO.on('socket_id_set', on_socket_set_response)
                socketIO.wait()
            
        t = threading.Thread(target=setupSocketClient, args = ())
        t.daemon = True
        t.start()
