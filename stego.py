#Stego is a steganography API to help you discover mailicious code hidden in media files
#This is a POC. Expect it not to work as you expect. Coding standards are low. There is a lot to refactor.
#Done as a hackaton effort at PureStorage

from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from stegano import lsb
import requests
import os
import re
from bs4 import BeautifulSoup


def stg_construct_json(status, sresponse, source = "", message = "", type = 1):
    # Construct the JSON responce we send back to the customer. No standard at the moment
    if type == 1:
        return jsonify({'status': status, 'response': sresponse, 'imgurl':source, 'message':message})
    else:
        return jsonify({'status': status, 'response': sresponse} )


app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def process_image():
    if request.method == 'POST':

        rstego = request.json['rstego']
        r = requests.head(rstego)

        #if the headers shows the content is an image. More work needed here, this could be bypassed
        if r.headers['Content-Type'].startswith("image/"):

            response = requests.get(rstego)
            sinvestigte = lsb.reveal(BytesIO(response.content))

            #if there is a hidden message, send an alert
            if sinvestigte != None:
                msg = "alert"
                mmsg = "Stego: Roar -> Secret message found."
                smessage = sinvestigte


            #if there is not a hidden message, declare the picture safe
            else:
                msg = "safe"
                mmsg = "Stego: Roar -> the picture is Safe."
                smessage = ""


        #If the image os not a picture, send an error message
        else:
            msg = "error"
            mmsg = "Stego: You make my cry. Maybe you are not feeding me pictures."
            smessage = ""


    #if not a POST request. Mayb efind an elegant solution
    else:
            msg = "info"
            mmsg = "Stego: Hm, I eat only POST Requests. Read more here: https://github.com/bogomil/stego"
            smessage = ""
            rstego = ""

    return stg_construct_json(msg, mmsg, rstego, smessage)

# send a url and the API will scan all the images in that URL and [not implemented] check them for malicious content.
@app.route("/url", methods=["POST","GET"])
def process_url():
    if request.method == 'POST':
        rstego = request.json['rstego']
        r = requests.head(rstego)


        if r.headers['Content-Type'].startswith("text/"):

            #read urls
            s_resp = ""
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
            response = requests.get(rstego,headers=headers)

            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            urls = [img['src'] for img in img_tags]


            for url in urls:
                filename = re.search(r'/([\w_-]+[.](jpg|gif|png|jpeg|jfif))$', url)
                if not filename:
                     #need an status here
                     continue
                if 'http' not in url:
                        # sometimes an image source can be relative
                        # if it is provide the base url which also happens
                        # to be the site variable atm.
                        url = '{}{}'.format(rstego, url)

                msg = "info"

                    #todo get the urls coming from the loop and run them one by one. Now return json array only.
                s_resp += "{"+ url +"}"
                #aapend json ther
            return stg_construct_json(msg, s_resp,"","",2)
            #end read Urls


        #If the content type is not HTML  send an error message
        else:
            msg = "error"
            mmsg = "Stego: You make my cry. Maybe you are not feeding me with a valid URL."

    else:
            msg = "info"
            mmsg = "Stego: Hm, I eat only POST Requests. Read more here: https://github.com/bogomil/stego"
            url = ""

    return stg_construct_json(msg, mmsg, url)

#For Heroku this must be like that.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
