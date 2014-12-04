def getSensibleName(msg):
	if msg["type"] in ("normal", "chat"):
		return msg["from"].split("@")[0]
	elif msg["type"] in ("groupchat"):
		return msg["from"].split("/")[1]


