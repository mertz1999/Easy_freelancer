import requests
from flask import Flask
from flask import request
from datetime import datetime
from flask import Response
from freelancer import Freelancer
from utils import parse_message,tel_send_message

app        = Flask(__name__)
freelancer = Freelancer(username= "hihellosalam2022@gmail.com", password="@Rezatz1378")


@app.route('/', methods=['GET', 'POST'])
def index():
    # Check request type
    if request.method == 'POST':
        # Restore message data
        msg = request.get_json()
        chat_id,txt = parse_message(msg)

        # Get id of telegram Chat
        if txt == "id":
            tel_send_message(chat_id,f'your id is {chat_id}')
        
        # Get bid from user
        if (txt[0:10].lower() == 'freelancer'):
            prop_file = open('proposals/temp','w')
            prop_file.write(txt)
            prop_file.close()

            url, amount, period = freelancer.parse_bid()
            if freelancer.send_bid(url=url, priod=period, amount=amount): 
                tel_send_message(chat_id,"Bid is one site!")
            else:
                tel_send_message(chat_id,"Problem to send bid!")

        return "Accepted"
        

    if request.method == 'GET':
        start = False
        start = request.args.get('start')
        if start == "True":
            print(datetime.now())
            projects = freelancer.fetch_projects()
            for p in projects:
                msg_maked = freelancer.make_message(p)
                tel_send_message(75248049,msg_maked)
        
        return "GET method recived"

 
if __name__ == '__main__':
   app.run(debug=True)
