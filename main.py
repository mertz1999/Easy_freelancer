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

        # parsing data
        chat_id,txt = parse_message(msg)
        if txt == "fetch":
            # Get projects from freelancer and send it on telegram
            projects = freelancer.fetch_projects()
            for p in projects:
                msg_maked = freelancer.make_message(p)
                tel_send_message(chat_id,msg_maked)

        else:
            tel_send_message(chat_id,'Not iplemented!')
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)
