import requests, json
import boto3

s3 = boto3.client('s3')
image_url = s3.generate_presigned_url('get_object',
                         Params={'Bucket': 'dreandes',
                                'Key':'articleWordCloud/new/wordcloud.png'})

def send_msg(slack_webhook, block, channel="#dss", username="뉴스봇"):
    payload = {"channel": channel, 
               "username": username, 
               "text": msg, 
               "icon_emoji": ":ghost:",
               "blocks": block
              }
    requests.post(slack_webhook, json.dumps(payload))
    
slack_webhook = ""

block = [{"type": "image",
          "title": {
              "type": "plain_text","text": "Today's WordCloud","emoji": True
          },
          "image_url": image_url,
          "alt_text": "marg"}]


msg = "Today's WordCloud"

send_msg(slack_webhook, block)
