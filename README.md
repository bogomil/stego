# Stego
Hello. I am Stego. I am a steganography dinosaur who helps you discover concrete threats on the internet.

Feed me your pictures, and I will detect a secret message or a malicious code in it.

I eat only POST and my mount is open in here: https://stegoapi.herokuapp.com/

Roar,

Your Stego


# A bit about the problem
Steganography is the practice of sending data in a concealed format so the very fact of sending the data is disguised. The word steganography is a combination of the Greek words στεγανός (steganos), meaning “covered, concealed, or protected”, and γράφειν (graphein) meaning “writing”.

Adversaries may use steganography techniques to prevent the detection of hidden information. Attackers can use steganographic techniques to hide data in digital media such as images, audio tracks, video clips, or text files.

There are (at least)  three main reasons for using steganography from bad actors:

- It helps them conceal not just the data itself but the fact that data is being uploaded and downloaded;
- It helps bypass DPI systems, which is relevant for corporate systems;
- The use of steganography may help bypass security checks by anti-APT products, as the latter cannot process all image files (corporate networks contain too many of them, and the analysis algorithms are relatively expensive)

*Source: Kaspersky*

## Resources
- See a good list of steganography attacks from the Mitre website: https://attack.mitre.org/techniques/T1027/003/


# Stego Use-Cases

- Create a browser plugin to check if the page you visit contains images with something in it.
- Check if someone is exposing trade secrets in the pictures posted on your website.
- Create a check before uploading an unknown image to your blog.
- Check if the pictures you are uploading from your brand new camera have a built-in malicious message. Exploiting camera software is not a big deal.


# Stego API Documentation
----
### Base Url
https://stegoapi.herokuapp.com/

## 1. Checks a *single image* for a hidden image (default)

* **Route**

 /

* **Method:**

`POST`


 * **Request format:**

`JSON`

*  **Request Params**

`rstego=[valid image url]`


* **Json Request format**

`{'rstego': [valid image url]}`

* **Response:**

 | Status  | Message | Description |
 | ------------- | ------------- |-----|
 | error  | Stego: You make my cry. Maybe you are not feeding me with a valid URL  | Returned when the image url is not valid.
 | info  | Stego: Hm, I eat only POST Requests  | Returned when you try to feed Stego with wrong requests.
 |safe|Stego: Roar -> the picture is Safe| Returned if the picture is analized and found safe.
 |alert|Stego: Roar -> Secret message found.| Returned when the picture is analized and a message has been found inside.


* **Sample Call: Python**

```python
import requests
url = 'https://stegoapi.herokuapp.com/'
#this one contains a hidden message
#s_url= "https://talkweb.eu/wp-content/uploads/2021/01/secret.png"
s_url = "https://1gr.cz/o/newspaper/images/vyber-mfd-3.png"
stego_obj = {'rstego': s_url}
r = requests.post(url, json = stego_obj)
print(r.content)
```

## 2. Checks a URL for hidden image content
*Under development: See the response section for the limitation*

* **Route**

 /url

* **Method:**

`POST`


 * **Request format:**

`JSON`

*  **Request Params**

`rstego=[valid url]`


* **Json Request format**

`{'rstego': [valid url]}`

* **Response:**

 Currently returns a json response with all the images discovered in that URL.


* **Sample Call: Python**

```python
import requests
#note the new route /url
url = 'https://stegoapi.herokuapp.com/url'
s_url = "https://talkweb.eu/c/lean-agile/"
stego_obj = {'rstego': s_url}
r = requests.post(url, json = stego_obj)
print(r.content)
```
