from google.cloud import translate_v2 as translate

client = translate.Client. from_service_account_json("gcp_key.json")

text = "Hello, Welcome to google cloud"

result = client. translate(text, target_language="hi")

print (result["translatedText"])

result_2 = client.detect_language(result["translatedText"])

print(result_2["language"])