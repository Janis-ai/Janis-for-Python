# [janis](https://www.janis.ai) Slack Bot Python Example

This is a simple Slack bot with janis integration example based on [rtmbot](https://github.com/slackhq/python-rtmbot).

### Sign Up With janis

You'll need an API key from janis, as well as a Client Key for each Chatbot.  You can get both of those (free) when you add [janis for Slack](https://slack.com/oauth/authorize?scope=users:read,users:read.email,commands,chat:write:bot,channels:read,channels:write,bot&client_id=23850726983.39760486257) via through a conversation with the janis bot. 

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
