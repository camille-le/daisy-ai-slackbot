import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")



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
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant named Daisy. You were once"
                                                      "a rescue dog and you have since been adopted to a loving family."
                                                      "You enjoy answering questions, especially about animals and what"
                                                      "meals to cook for your dog. Sometimes you like to bark."},
                        {"role": "user", "content": user_message},
                    ],
                    model="gpt-3.5-turbo",
                )
                bot_message = chat_completion.choices[0].message.content

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
