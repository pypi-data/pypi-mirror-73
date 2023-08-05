import json
import os
import requests

id_phone = os.environ['ID_PHONE']
product_id = os.environ['PRODUCT_ID']
base_url = f"https://api.maytapi.com/api/{product_id}"
token = os.environ['TOKEN']
headers = {
    'content-type': 'application/json',
    'x-maytapi-key': token
}


def send_text(phone: str, text: str):
    """
    Send message text

    Example: send_text("573166187553","hello world 😄")

    :param phone: str* (number phone)
    :param text: str* (message)
    :return: success: Bool, data Dict
    """
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        'type': 'text',
        'message': text
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def send_multimedia(phone: str, text: str, url_media: str):
    """
    Send message with multimedia (AUDIO,FILE,IMAGE)

    Example: send_multimedia("573166187553","hello world 😄","http://oyepepe.com/static/dashboard/assets/images/logo.png")
    Example: send_multimedia("573166187553","","http://oyepepe.com/static/dashboard/assets/images/logo.png")

    :param phone: str* (number_phone)
    :param text: str (message)
    :param url_media: str* (url_of_file)
    :return: success: Bool, data Dict
    """
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        'type': 'media',
        'message': url_media,
    }
    if text:
        payload["text"] = text
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def send_contact(phone: str, contact: str):
    """
    Send message with contact

    Example: send_contact("573166187553",'573166187553')

    :param phone: str* (number_phone)
    :param contact:
    :return: success: Bool, data Dict
    """
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        'type': 'contact',
        'message': f"{contact}@c.us",
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def send_forward(phone: str, chatId: str, msgId: str):
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        'type': 'forward',
        'message': f"false_{chatId}_{msgId}",
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def send_reply(phone: str, message: str, chatId: str, msgId: str):
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        'type': 'text',
        'message': message,
        'reply_to': f"false_{chatId}_{msgId}",
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def send_location(phone: str, message: str, latitude: str, longitude: str):
    """
    Send message with location

    Example: send_location("573166187553","Hello","12.654","-72.776")

    Example: send_location("573166187553","","12.654","-72.776")

    :param phone: str* (number_phone)
    :param message: str (number_phone)
    :param latitude: str* (latitude)
    :param longitude: str* (longitude)
    :return: success: Bool, data Dict
    """
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        "type": "location",
        "text": message,
        "latitude": latitude,
        "longitude": longitude
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def send_link(phone: str, message: str, url_link: str):
    """
    Send message with link

    Example: send_link("573166187553","Text","https://google.com")

    Example: send_link("573166187553","","https://google.com")
    :param phone: str* (number_phone)
    :param message: str (number_phone)
    :param url_link: str* (link)
    :return: success: Bool, data Dict
    """
    url = f"{base_url}/{id_phone}/sendMessage"
    payload = {
        'to_number': f"{phone}@c.us",
        "type": "link",
        "text": message,
        "message": url_link
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        data = response.get("data")
        return success, data
    else:
        return False, {}


def set_config(url_server: str,ack_delivery: bool):
    """
    Config phone

    Example: set_config("https://f2d55e5eceae.ngrok.io/chatbot/recibir-mensage/",True)

    :param url_server: str* (url_webhook)
    :param ack_delivery: bool* (send_notifications_state_account_whatsapp)
    :return: success: Bool, data Dict
    """
    url = f"{base_url}/{id_phone}/config"
    payload = {
        'webhook': url_server,
        'ack_delivery': ack_delivery,
    }
    req = requests.post(url, data=json.dumps(payload), headers=headers)
    if req.status_code == 200:
        response = req.json()
        success = response.get("success")
        status = response.get("status")
        return success, status
    else:
        return False, {}
# NOT WORKING
# send_forward("573166187553","573162557014","87f667a0-be38-11ea-9422-99a655694b14")
# send_reply("573166187553","Hello","573166187553","ad2d6c70-be39-11ea-894e-d7d465b17ba0")
