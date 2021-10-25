import argparse
import logging
import os
import urllib

import boto3
import requests
from botocore.config import Config
from botocore.exceptions import ClientError

conf = {
    'TOKEN': '1857443773:AAGOtuPhdjOmH3byx7LyOv9fX_cZptdmTy8'
}

emojis = {
    'Назад': '\U0001F519',  # '\U00002B05',
    'Отзыв': '\U0001F4DD',
    'Напитки': '\U0001F379',
    'Кофе': '\U00002615',
    'Меню': '\U0001F4D7',
    'Десерты': '\U0001F370',
    'Закуски': '\U0001F374'
}

admins = {
    'Daniil': 347739791
}

AWS_S3_CREDS = {
        "aws_secret_access_key":'HjE6hfY7hG7A+bs+tqaZC/yLvsXz7lCOilhDRgU1',
    "aws_access_key_id":'AKIA3IXPI3A3LIZGYBTP',
    "region_name":'eu-central-1'
}
url = boto3.client('s3',
                   region_name='eu-central-1',
                   aws_access_key_id='AKIA3IXPI3A3A6PXQXOH',
                   aws_secret_access_key='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').generate_presigned_url(Params={'Bucket': 'coffee-dishes-db',
                                                        'Key': 'dishes.dump'},
                                                    ClientMethod='put_object')
print(url)

def main(ROLE_ARN=None):
  sts_client = boto3.client('sts')
  assume_role_response = sts_client.assume_role(
      RoleArn=os.environ.get(ROLE_ARN),
      RoleSessionName="collaborator-session"
  )
  credentials = assume_role_response['Credentials']
  url_credentials = {}
  url_credentials['sessionId'] = credentials.get('AccessKeyId')
  url_credentials['sessionKey'] = credentials.get('SecretAccessKey')
  url_credentials['sessionToken'] = credentials.get('SessionToken')
  json_string_with_temp_credentials = json.dumps(url_credentials)
  print(f"json string {json_string_with_temp_credentials}")

  request_parameters = f"?Action=getSigninToken&Session={urllib.parse.quote(json_string_with_temp_credentials)}"
  request_url = "https://signin.aws.amazon.com/federation" + request_parameters
  r = requests.get(request_url)
  signin_token = json.loads(r.text)
  request_parameters = "?Action=login" 
  request_parameters += "&Issuer=Example.org" 
  request_parameters += "&Destination=" + urllib.parse.quote("https://us-west-2.console.aws.amazon.com/cloudshell")
  request_parameters += "&SigninToken=" + signin_token["SigninToken"]
  request_url = "https://signin.aws.amazon.com/federation" + request_parameters

  # Send final URL to stdout
  print (request_url)

if __name__ == "__main__":
  main()

