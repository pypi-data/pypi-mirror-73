# Package: dishevel
# Version: 0.0.2

#useful json style error object {bool: ok:, int: error_code, str: description}

import json
import re
import urllib.request
import urllib.parse

# Check if any list of words are in dict.
def listInDict(seq, hash):
    for e in seq:
        if e in hash:
            return e

# Get JSON as pyData from a web request. That is a python data structure.
# If there is no json it returns {hasJson:False}
def query(path, apiPath, params=None):
	jsonType = "application/json"
	extras = {
		"hasJson": False,
		"hasError": False # Indicates whether json is an error report.
	}
	reqString = path + urllib.parse.quote(apiPath)
	if params:
		reqString += "?" + urllib.parse.urlencode(params)
	try:
		htres = urllib.request.urlopen(reqString)
		contentType = htres.getheader("content-type", "")
		
		if contentType.startswith(jsonType):
			extras["hasJson"] = True
			extras["json"] = json.load(htres)
			return extras
		else:
			extras['text'] = htres.read()
			return extras
	except urllib.error.HTTPError as exception:
		contentType = exception.getheader("content-type", "")
		
		if contentType.startswith(jsonType):
			extras["hasJson"] = True
			extras["hasError"] = True
			extras["json"] = json.load(exception)
		return extras

class Bot:
	def __init__(self, botKey):
		self.botKey = botKey
		self.commands = []
		self.helpString = ""
		self.lastError = ""
		self.botQueryUri = "https://api.telegram.org/bot"+botKey
		self.fileHandler = None

		user = self.getMe()
		if user:
			self.name = user['first_name']
			self.botName = user['username']

		self.on("^/help", self.help)
		self.on("^/online", self.online)
		
	# The heart of the framework.
	def start(self):
		print("Started %s." % self.botName)

		updates = self.getUpdates({'allowed_updates': 'message', 'timeout': 100})
		update_id = -1
		
		while True:
			if updates:
				for update in updates:
					if "message" in update:
						extras = {}
						chatId = update['message']['chat']['id']
						senderId = update['message']['from']['id']
						sentBy = update['message']['from']['first_name']
						if "reply_to_message" in update['message']:
							extras['replyMsgId'] = update['message']['reply_to_message']['message_id']
							if "text" in update['message']['reply_to_message']:
								extras['replyMsg'] = update['message']['reply_to_message']['text']
							extras['replyMsgSenderId'] = update['message']['reply_to_message']['from']['id']
							extras['replyMsgChatId'] = update['message']['reply_to_message']['chat']['id']
						if "text" in update['message']:
							message = update['message']['text']
							extras.update({
								"chatId": chatId,
								"sender": sentBy,
								"senderId": senderId
							})
							# debug who sent the message
							print(sentBy, message)
							self.run(message, extras)
						
						# All media is handled by one method, runFileHandler().
						result = listInDict(['audio', 'video', 'document'], update['message'])
						if result:
							print(result.capitalize(), "found")
							fileId = update['message'][result]['file_id']
							extras = {
								"fileType": update['message'][result]['mime_type'],
								"mediaType":  result
							}
							if result == "audio":
								extras['track'] = update['message'][result]['performer'] + " - " + update['message'][result]['title']
							self.runFileHandler(fileId, extras)
							
					update_id = update['update_id']

			updates = self.getUpdates({
				'allowed_updates': 'message',
				'timeout': 100,
				'offset': update_id+1
			})
	
	def run(self, message, extras):
		for triggerData in self.commands:
			pattern = triggerData[0]
			command = triggerData[1]
			if pattern.search(message):
				if message.startswith("/"):
					if message.find(" ") != -1:
						commandStr, message = message.split(" ", 1)
						commandStr = commandStr[1:]
					else:
						commandStr = message
						message = ""
					extras['commandStr'] = commandStr
				command(message, extras)

	def runFileHandler(self, fileId, fileType):
		if self.fileHandler:
			self.fileHandler(fileId, fileType)

	def on(self, pattern, method):
		if pattern == "fileReceived":
			self.fileHandler = method
			return
		self.commands.append([re.compile(pattern), method])

	def getMe(self):
		pyData = query(self.botQueryUri, "/getMe")
		if pyData["hasJson"] & pyData["json"]["ok"]:
			return pyData["json"]["result"]

	def addHelpString(self, text):
		self.helpString += text + "\n"

	# self event handlers
	def help(self, message, extras):
		if self.helpString == "":
			self.sendMessage(extras["chatId"], "No help set")
		else:
			self.sendMessage(extras['chatId'], self.helpString)

	def online(self, message, extras):
		self.sendMessage(extras['chatId'], "I'm online!")
	# end

	def getUpdates(self, params=None):
		pyData = query(self.botQueryUri, "/getUpdates", params)
		if pyData["hasJson"] & pyData["json"]["ok"]:
			return pyData["json"]["result"]

	def getLastError(self):
		return self.lastError

	def sendMessage(self, to, message):
		pyData = query(self.botQueryUri, "/sendMessage", {'chat_id': to, 'text': message})
		if pyData["hasJson"] & pyData["json"]["ok"]:
			return pyData["json"]["result"]

	# Returns a Uri to a temporary file.
	# Do not share this link to a public chat.
	def getFile(self, fileId):
		pyData = query(self.botQueryUri, "/getFile", {'file_id': fileId})
		if pyData["hasJson"] & pyData["json"]["ok"]:
			fileObject = pyData["json"]["result"]
			return "https://api.telegram.org/file/bot" + self.botKey + "/" + fileObject['file_path']

	# Returns True on success.
	# Returns False on same message pinned.
	def pinChatMessage(self, to, messageId, disableNotify=False):
		pyData = query(self.botQueryUri, "/pinChatMessage", {'chat_id': to, 'message_id': messageId, 'disable_notification': disableNotify})
		if "hasJson" in pyData:
			if pyData['json']['ok']:
				if pyData['json']['result']:
					return True
				else:
					return False

	# Returns True on success.
	# Returns False if no message is pinned.
	def unpinChatMessage(self, to):
		pyData = query(self.botQueryUri, "/unpinChatMessage", {'chat_id': to})
		if "hasJson" in pyData:
			if pyData['json']['ok']:
				if pyData['json']['result']:
					return True
				else:
					return False
