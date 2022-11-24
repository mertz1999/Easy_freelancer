import requests

TOKEN      = "5956637545:AAGFOmqKDTCm7KUr_2CCifGn_LL-cZF4fUk"

# Get msg and id
def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    return chat_id,txt

# Send telegram message
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 