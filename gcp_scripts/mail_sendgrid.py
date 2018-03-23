import requests

url = "https://api.sendgrid.com/v3/mail/send"

payload = '{"personalizations":[{"to":[{"email":"test@gmail.com","name":"John Doe"}],"subject":"Hello, World!"}],"from":{"email":"test@gmail.com","name":"Sam Smith"},"reply_to":{"email":"test@gmail.com","name":"Sam Smith"},"subject":"Hello, World!","content":[{"type":"text/html","value":"test"}]}'


headers = {
    'authorization': "Bearer <api key> ",
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)

