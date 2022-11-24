from flask import Flask
from flask import request
from flask import Response
from freelancer import Freelancer
from utils import parse_message,tel_send_message


    

app        = Flask(__name__)
freelancer = Freelancer()


@app.route('/', methods=['GET', 'POST'])
def index():
    # Check request type
    if request.method == 'POST':
        # Restore message data
        msg = request.get_json()
        chat_id,txt = parse_message(msg)

        if txt == "id":
            tel_send_message(chat_id,f'your id is {chat_id}')

        return "Accepted"
        

    if request.method == 'GET':
        start = False
        start = request.args.get('start')
        if start == "True":
            tel_send_message(75248049,"======= START =======")
            projects = freelancer.fetch_projects()
            for p in projects:
                msg_maked = freelancer.make_message(p)
                tel_send_message(75248049,msg_maked)
        
        return "GET method recived"

 
if __name__ == '__main__':
   app.run(debug=True)
