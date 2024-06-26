import os
import json
import openai
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

openai.api_key = OPENAI_API_KEY


@csrf_exempt
def slack_events(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Slack URL verification challenge
        if 'challenge' in data:
            return JsonResponse({'challenge': data['challenge']})

        # Handle message events
        if 'event' in data:
            event = data['event']
            if event['type'] == 'message' and 'bot_id' not in event:
                user_message = event['text']
                channel_id = event['channel']

                # Generate response using OpenAI API
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=user_message,
                    max_tokens=150
                )
                bot_message = response.choices[0].text.strip()

                # Send the response back to Slack
                send_message(channel_id, bot_message)

        return JsonResponse({'status': 'ok'})


def send_message(channel, text):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }
    data = {
        'channel': channel,
        'text': text
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        print(f"Failed to send message: {response.text}")
