# [Janis](https://www.janis.ai) Messenger Chatbot Python Example

This is a simple Messenger Chatbot with a [Janis](https://www.janis.ai) integration. 
This integration example is based on [Facebook's example](https://github.com/fbsamples/messenger-platform-samples) and assumes you are coding and hosting your own Chatbot.  If you want to experiment with a hosted Chatbot example, you can remix our [Glitch](https://glitch.com/edit/#!/blaze-temper) project. 


### Sign Up With janis

You'll need an API key from Janis and a Client Key for your Chatbot.  You can get both of those (free) when you add [Janis for Slack](https://www.janis.ai) and start a conversation with Janis in Slack.

### Register for an Access Token with Facebook

You'll need to setup a [Facebook App](https://developers.facebook.com/apps/), Facebook Page, get the Page Access Token and link the App to the Page before you can start to use the Janis Send/Receive service.
[This quickstart guide should help](https://developers.facebook.com/docs/messenger-platform/quickstart).
NOTE: In the Webhooks section of your Facebook Messenger app, in addition to adding a Callback URL and creating a Verify Token, make sure the following events are selected: messages, messaging_postbacks, message_echoes, standby, messaging_handovers. 

### Set App Roles

Once you have completed the steps above and completed the Janis installation, go to the Facebook page where you added your bot with Janis integrated. Click "Settings" for the page, than select Messenger Platform. Set your app to be the "Primary Receiver". Set Janis as the "Secondary Receiver". For more information about app roles, see: [Facebook App Roles](https://developers.facebook.com/docs/messenger-platform/handover-protocol#app_roles).

### Janis Installation

```bash
$ pip install -r requirements.txt
```

### Usage

Open [JANIS_messenger_bot.py](./JANIS_messenger_bot.py) and modify `JANIS_API_KEY`, `JANIS_CLIENT_KEY`, `ACCESS_TOKEN` and `VERIFY_TOKEN` to match your own.

Run the following command to get your bot online:

```bash
$ python janis_messenger_bot.py
```
