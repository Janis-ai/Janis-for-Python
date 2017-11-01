# [Janis](https://www.janis.ai) Slack Bot Python Example

This is a simple Slack bot with Janis integrated.  The example is based on [rtmbot](https://github.com/slackhq/python-rtmbot).

### Sign Up With janis

You'll need an API key from Janis and a Client Key for your Chatbot.  You can get both of those (free) when you add [Janis for Slack](https://www.janis.ai) and start a conversation with Janis in Slack.

### Connecting Your Bot to Slack

To connect a bot to Slack, [get a Bot API token from the Slack integrations page](https://my.slack.com/services/new/bot).

### Installation

```bash
$ pip install -r requirements.txt
```

### Usage

Open [rtmbot.conf](./rtmbot.conf) and add your `SLACK_TOKEN`. 
Then open [janisConnector.py](./plugins/janisConnector.py) and modify `JANIS_API_KEY` and `JANIS_CLIENT_KEY` to match your own.

Run the following command to get your bot online:

```bash
$ rtmbot
```
