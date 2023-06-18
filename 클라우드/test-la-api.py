import json
import requests
import boto3
import os

def lambda_handler(event, context):
    # currencylayer.com API 키 설정
    access_key = os.environ['ACCESS_KEY']
    url = f"http://apilayer.net/api/live?access_key={access_key}&currencies=USD,EUR,KRW,JPY&format=1"

    # currencylayer.com에서 환율 정보 가져오기
    response = requests.get(url)
    livequote = response.json()
    quotes = livequote.get("quotes")

     # 변수 quotes에 id 추가
    id_counter = 1
    result = []
    for key, value in quotes.items():
        pair = {
            "id": str(id_counter),
            "key": key,
            "value": value
        }
        result.append(pair)
        id_counter += 1

    # S3에 JSON 파일 저장
    s3 = boto3.client('s3')
    bucket_name = 'testbk-api-7'
    file_name = 'quotes.json'

    json_data = json.dumps(result)
    s3.put_object(Body=json_data, Bucket=bucket_name, Key=file_name)

    return {
        'statusCode': 200,
        'body': 'Quotes saved successfully to S3.'
    }
