# daisy-ai-slackbot

AI Chatbot Application to use in a Slack workspace

### Installation
Set up your Slack developer account and a Slack workspace.
Create a new application within the Slack developer website.
After that's setup, go ahead and clone this repo.

Set up `.env` file in the project and set the API keys:
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
OPENAI_API_KEY=your-openai-api-key
```
After updating this, you can set up a virtual environment, activate it
and install the requirements.
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

To test the Slack integration, install `ngrok`, including signing up for the 
service and going through the authorization flow. You'll get back a URL which
you can setup in `Event Subscriptions`. You'll also need to modify `ALLOWED_HOSTS`
```bash
# Install NGROK
brew install ngrok
ngrok http 8000

# Do work to update event subscriptions

# Do work to update the scopes for the Slackbot and event subscriptions

# Modify ALLOWED_HOSTS

# Open your Slack channel and message the bot
```

Finally, to deploy it in Heroku
 

### Errors That May Come Up / QA
> You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.

Run `python manage.py migrate` to apply migrations.

What is Ngrok? 
> It enables developers to expose a local development server to the Internet with minimal effort. The software makes your locally-hosted web server (like computer, laptop, rasbery PI) appear to be hosted on a subdomain of ngrok.com, meaning that no public IP or domain name on the local machine is needed.
