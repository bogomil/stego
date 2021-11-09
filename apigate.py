from flask import Flask, request, jsonify
from PIL import Image
from stegano import lsb
import os


app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({'status': "SUCCESS", 'message': "A basic steganography API. We accept only POST. Read more here: http://talkweb.eu/openweb/3122/"})


@app.route("/steg", methods=["POST","GET"])
def process_image():
    if request.method == 'POST':

        file = request.files['image']
        try:
            img = Image.open(file.stream)
            msg ="sucess"
            mmsg = lsb.reveal(img)
        except:
            msg = "error"
            mmsg = "Something went wrong. Maybe you are not sending a picture"
    else:
            msg = "info"
            mmsg = "A basic steganography API. We accept only POST. Read more here: http://talkweb.eu/openweb/3122/"

    return jsonify({'status': msg, 'message': mmsg})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
