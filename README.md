# [Janis](https://www.Janis.ai) - Message Management
## For Chatbots built with Python

Janis helps teams train and monitor bots and fix problems fast.  [Build a bot in Python](./examples/) and integrate Janis with just a few lines of code to ensure delightful conversational experiences in every messaging channel.

* Train
Collaborate on what users say and your responses in a dedicated training channel. Experience exactly what your users will experience when they message you.

* Monitor
Janis alerts you in Slack when your bot needs your help. Use our smart alerts, or create your own alerts to bring humans in the loop.

* Fix Problems Fast
Take over for your bot and chat live to retain your users, while training your AI to learn from the conversation. Hand control back to your bot when you're done.

To learn more about Janis' capabilities, visit [Janis.ai](https://www.janis.ai)

### What you need to get started:
* [Add Janis to your Slack team](https://www.janis.ai)
* [A Chatbot built in Python](./examples/)

##### Operational Dependencies:
1.  You'll need an API key and a Client Key for your Chatbot.  You can get both of those (free) when you add Janis to Slack. 
2.  If you're building a Messenger Chatbot, you'll need to setup a Facebook App, Facebook Page, get the Page Access Token from Facebook and link the Facebook App to the Facebook Page for Janis to work. This is standard for any Chatbot you build for Messenger.
3.  Janis can help you train your AI from Slack.  Currently Dialogflow, formerly known as API.AI (http://www.api.ai) is supported.

Note: This module has been tested with Messenger, Slack, Skype, and Microsoft Webchat. Please see our [examples](./examples/).

### Installation

```bash
$ pip install janis
```


### Usage

```python
from janis import janis
apiKey = xxxxxxxxxxxxxxxxxxxxxx # <= key provided by janis for Slack
clientKey = xxxxxxxxxxxxxxxxxxxxxx # <= key provided by janis for Slack
botPlatform = 'messenger'; # <= possible values: 'messenger', 'slack'
token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx # <= only required for Messenger bots.

janis = janis(apiKey, clientKey, botPlatform, token)
```
##### Incoming Message Schema:
Throughout this documentation, you will see references to `incomingMessage`. Depending on whether you have a Messenger or Slack bot, the schema will be different. The value of `incomingMessage` should be equal to the message you receive directly from either the Messenger webhook response, or from the Slack RTM event response.

```python
# Example of a Slack Incoming Message
{
    "type": "message",
    "channel": "D024BE91L",
    "user": "U2147483697",
    "text": "Hello world",
    "ts": "1355517523.000005"
}

# Example of a Messenger Incoming Message
{
  "sender":{
    "id":"USER_ID"
  },
  "recipient":{
    "id":"PAGE_ID"
  },
  "timestamp":1458692752478,
  "message":{
    "mid":"mid.1457764197618:41d102a3e1ae206a38",
    "seq":73,
    "text":"hello, world!",
    "quick_reply": {
      "payload": "DEVELOPER_DEFINED_PAYLOAD"
    }
  }
}  
```

##### Outgoing Message Schema:
Throughout this documentation, you will see references to `outgoingMessage`. Depending on whether you have a Messenger or Slack bot, the schema, as defined by each platform, will be different. Every time you track an outgoing message, the schema requirements match the respective platform.

```python
# Example of Slack Outgoing Message
{
    "channel": "C024BE91L",
    "text": "Hello world"
}

# Exmaple of Messenger Outgoing Message
{
  "recipient":{
    "id":"USER_ID"
  },
  "message":{
    "text":"hello, world!"
  }
}
```

##### Tracking received messages:

When your bot receives an incoming message, you'll need to log the data with janis by calling to `janis.hopIn`. 
__Note__: janis can pause your bot so that it doesn't auto response while a human has taken over. The server response from your `hopIn` request will pass the `paused` state. Use that to stop your bot from responding to an incoming message. Here is an example:

```python
hopInResponse = janis.hopIn(incomingMessage)
# If your bot is paused, stop it from replying
if hopInResponse.get('paused'):
    return "Success"
    ...
```

##### Tracking sent messages:

Each time your bot sends a message, make sure to log that with janis by calling to `janis.hopOut`. Here is an example of a function that we're calling `sendIt` that tracks an outgoing message and at the same time, has the bot say the message:
```python
def sendIt(channel, text):
    # schema matches Messenger
    outgoingMessage = {'recipient': {'id': channel},'message': {'text': text}}
    janis.hopOut(outgoingMessage)
    bot.send_text_message(channel, text) # <= example of bot sending reply
    ...
```

##### Log Unknown Intents:

Find the spot in your code your bot processes incoming messages it does not understand. Within that block of code, call to `janis.logUnkownIntent` to capture these conversational ‘dead-ends’. Here's an example:

```python
# let the user know that the bot does not understand
sendIt(recipient_id, 'Huh?')
# capture conversational dead-ends.
janis.logUnknownIntent(incomingMessage) 
```
##### Dial 0 to Speak With a Live Human Being:

janis can trigger alerts to suggest when a human should take over for your Chatbot. To enable this, create an intent such as when a customer explicitly requests live assistance, and then include the following lines of code where your bot listens for this intent:

```python
# match an intent to talk to a real human
if text == 'help':
    # let the user know that they are being routed to a human
    sendIt(recipient_id, 'Hang tight. Let me see what I can do.')
    # send a janis alert to your slack channel
    # that the user could use assistance
    janis.assistanceRequested(incomingMessage);
```

##### Human Take Over:

To enable the ability to have a human take over your bot, add the code below to subscribe to the 'chat response' event. Alternatively, if you'd prefer to use a webhook to receive the payload, please get in touch with us at support@janis.ai and we can enable that for you.

```python
# Handle forwarding the messages sent by a human through your bot
def onChatResponse(self, args):
    channel = args["channel"]
    text = args["text"]
    bot.send_text_message(channel, text) # <= example of bot sending message
    
janis.on('chat_response', onChatResponse)
```

Go back to Slack and wait for alerts. That's it! 
[Be sure to check out our examples.](./examples/)


### Looking for something we don't yet support?  
* [Join our mailing list and we'll notifiy you](https://www.janis.ai)
* [Contact Support](mailto:support@janis.ai)
