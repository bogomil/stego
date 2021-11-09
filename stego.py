from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from stegano import lsb
import requests
import os


app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def process_image():
    if request.method == 'POST':

        sfile = request.json['fstego']
        r = requests.head(sfile)

        #if the headers shows the content is an image. More work needed here, this could be bypassed
        if r.headers['Content-Type'].startswith("image/"):

            response = requests.get(sfile)
            sinvestigte = lsb.reveal(BytesIO(response.content))

            #if there is a hidden message, send an alert
            if sinvestigte != None:
                msg = "alert"
                mmsg = "Stego: Roar -> Secret message found."

            #if there is not a hidden message, declare the picture safe
            else:
                msg = "safe"
                mmsg = "Stego: Roar -> the picture is Safe."

        #If the image os not a picture, send an error message
        else:
            msg = "error"
            mmsg = "Stego: You make my cry. Maybe you are not feeding me pictures."


    #if not a POST request
    else:
            msg = "info"
            mmsg = "Stego: Hm, I eat only POST Requests. Read more here: https://github.com/bogomil/stego"

    return jsonify({'status': msg, 'message': mmsg})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
