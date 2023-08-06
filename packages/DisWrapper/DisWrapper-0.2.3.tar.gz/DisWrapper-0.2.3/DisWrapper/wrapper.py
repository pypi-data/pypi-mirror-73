from websocket import create_connection
import requests, json, threading, select, multiprocessing, time, os
from datetime import datetime

class User:
    def __init__(self, user_id, username, avatar, discriminator, public_flags, nick=None):
        self.user_id = user_id
        self.username = username
        self.nick = nick
        self.avatar = avatar
        self.discriminator = discriminator
        self.public_flags = public_flags


class Message:
    def __init__(self, message_id, message_type, content, channel_id, author, attachments, emebds, 
                mentions, mention_roles, pinned, mention_everyone, tts, timestamp, edited_timestamp, flags):
        self.message_id = message_id
        self.type = message_type
        self.content = content
        self.channel_id = channel_id
        self.author = author
        self.attachments = attachments
        self.embeds = emebds
        self.mentions = mentions
        self.mention_roles = mention_roles
        self.pinned = pinned
        self.tts = tts
        self.timestamp = timestamp
        self.edited_timestamp = edited_timestamp
        self.flags = flags


class DisWrapper:
    def __init__(self):
        self.requester = requests.Session()
        self.request_logging = False

        self.ws_gateway_query_params = '/?encoding=json&v=6'
        self.ws = None
        self.ws_send_queue = multiprocessing.Queue()

    def sendReq(self, method, url, data=None, headers={}, params=None):
        res = self.requester.request(method, url, headers=headers, json=data, params=params)
        if self.request_logging: print(f"[{method}] {url} - {res.status_code}: {res.text}")
        return res

    def auth(self, email, password):
        header = {
            "content-type": "application/json"
        }
        payload = {"email": email, "password": password}
        url = "https://discord.com/api/v6/auth/login"

        req = self.sendReq("POST", url, payload, header).text
        json_request = json.loads(req)

        self.theme = json_request["user_settings"]["theme"]
        self.locale = json_request["user_settings"]["locale"]
        self.token = json_request["token"]
        return self.token


    def sendMessage(self, channel_id, message):
        headers = {
            "Authorization": self.token,
            "content-type": "application/json"
        }
        payload = {"content": message}
        url=f"https://discordapp.com/api/channels/{channel_id}/messages"

        req = self.sendReq("POST", url, payload, headers)
        self.last_message_request = req
        self.last_message_reponse = json.loads(req.text)

        return json.loads(req.text)
    

    def readMessage(self, num_messages, channel_id):
        messages = []

        headers = {
            "Authorization": self.token
        }
        url=f"https://discordapp.com/api/v6/channels/{channel_id}/messages?limit={num_messages}"

        req = self.sendReq("GET", url, headers=headers)
        request_json = json.loads(req.text)

        for message in request_json:
            new_author = User(message["author"]["id"], message["author"]["username"], message["author"]["avatar"], 
                                message["author"]["discriminator"], message["author"]["public_flags"])

            new_message = Message(message["id"], message["type"], message["content"], message["channel_id"], new_author, 
                                  message["attachments"], message["embeds"], message["mentions"], message["mention_roles"],
                                  message["pinned"], message["mention_everyone"], message["tts"], message["timestamp"],
                                  message["edited_timestamp"], message["flags"])
            messages.append(new_message)
        
        messages.reverse()
        
        return messages


    def typing(self, channel_id):
        headers = {
            "Authorization": self.token
        }
        url=f"https://discord.com/api/v6/channels/{channel_id}/typing"
        req = self.sendReq("POST", url, headers=headers)
        return

    
    def createInvite(self, max_age, max_uses, channel_id):
        headers = {
            "Authorization": self.token
        }
        payload = {
            "max_age":max_age,
            "max_uses":max_uses
        }
        url=f"https://discord.com/api/v6/channels/{channel_id}/invites"

        req = self.sendReq("POST", url, payload, headers)


    def setStatus(self, status):
        headers = {"Authorization": self.token}
        payload = {"custom_status":{"text":status}}
        url = "https://discord.com/api/v6/users/@me/settings"

        req = self.sendReq("PATCH", url, payload, headers)


    def setNick(self, server_id, user_id, nickname):
        headers = {"Authorization": self.token}
        payload = {"nick": nickname}
        url = f"https://discordapp.com/api/v6/guilds/{server_id}/members/{user_id}"

        req = self.sendReq("PATCH", url, payload, headers)

        if req.status_code == 200:
            return True
        return False

    
    def getGuildUserInfo(self, server_id, user_id):
        headers = {"Authorization": self.token}
        url = f"https://discordapp.com/api/v6/guilds/{server_id}/members/{user_id}"

        req = self.sendReq("GET", url, headers=headers)
        req_json = json.loads(req.text)

        new_user = User(req_json["user"]["id"], req_json["user"]["username"], req_json["user"]["avatar"], 
                        req_json["user"]["discriminator"], req_json["user"]["public_flags"], req_json["nick"])
        
        return new_user
    
    def getUserInfo(self, user_id):
        headers = {"Authorization": self.token}
        url = f"https://discordapp.com/api/v6/users/{user_id}"

        req = self.sendReq("GET", url, headers=headers)
        req_json = json.loads(req.text)

        new_user = User(req_json["id"], req_json["username"], req_json["avatar"], 
                        req_json["discriminator"], req_json["public_flags"])
        return new_user

    def get_websocket_gateway(self):
        req = self.sendReq("GET", "https://discordapp.com/api/v6/auth/login")
