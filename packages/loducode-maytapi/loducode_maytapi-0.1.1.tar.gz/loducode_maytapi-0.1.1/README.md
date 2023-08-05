# Library non Official for maytapi PYTHON

Library for send messages for whatsapp

## functionalities

- **Send message**
    - send_text("573166187553","hello world 😄")
- **Send multimedia**
    - send_multimedia("573166187553","hello world 😄","http://oyepepe.com/static/dashboard/assets/images/logo.png")
    - send_multimedia("573166187553","","http://oyepepe.com/static/dashboard/assets/images/logo.png")  
- **Send contact**
    - send_contact("573166187553",'573166187553')
- **Send location**
    - send_location("573166187553","Hello","12.654","-72.776")
    - send_location("573166187553","","12.654","-72.776")
- **Send link**
    - send_link("573166187553","Text","https://google.com")
    - send_link("573166187553","","https://google.com")
- **Set config**
    - set_config("https://f2d55e5eceae.ngrok.io/chatbot/recibir-mensage/",True)

### Required ENV

- ID_PHONE
- PRODUCT_ID
- TOKEN