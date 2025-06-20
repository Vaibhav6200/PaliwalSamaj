# from google.cloud import translate_v2 as translate
# client = translate.Client. from_service_account_json("gcp_key.json")
# text = "Hello, Welcome to google cloud"
# result = client.translate(text, target_language="hi")
# print (result["translatedText"])
# result_2 = client.detect_language(result["translatedText"])
# print(result_2["language"])


# from google.transliteration import transliterate_text
#
# text = "Hello, Welcome to google cloud"
# result = transliterate_text(text, lang_code='hi')
#
#
# text = "Hello, Welcome to google cloud"
#
# # Perform transliteration (not translation)
# transliterated = transliterate_text(text, lang_code='hi')
#
# # Print result
# print(f"Original Text: {text}")
# print(f"Transliterated (Hindi Script): {transliterated}")
