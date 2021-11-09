from flask import Flask, request, jsonify
from PIL import Image
from stegano import lsb
import os


app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def process_image():
    if request.method == 'POST':

        file = request.files['image']
        try:
            img = Image.open(file.stream)
            msg ="sucess"
            mmsg = lsb.reveal(img)
        except:
            msg = "error"
            mmsg = "Stego here: Something went wrong. Maybe you are not feeding me with pictures."
    else:
            msg = "info"
            mmsg = "Stego here: I eat only POST requests. Read more here: https://github.com/bogomil/stego "

    return jsonify({'status': msg, 'message': mmsg})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
