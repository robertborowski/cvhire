import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
# ID of the channel you want to send the message to
channel_id = "C02028H1ZK9"

try:
  # Call the chat.postMessage method using the WebClient
  result = client.chat_postMessage(
    channel=channel_id, 
    text="Hello world"
  )
  print(result)

except SlackApiError as e:
  logger.error(f"Error posting message: {e}")