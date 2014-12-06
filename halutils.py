def getSensibleName(msg):
	if msg["type"] in ("normal", "chat"):
		return msg["from"].split("@")[0]
	elif msg["type"] in ("groupchat"):
		return msg["from"].split("/")[1]

def splitArgStr(msg):
	body = msg['body'].split(" ", 1)

	return (body[0], body[1]) if len(body) == 2 else (body[0], "")

def splitArgList(msg):
	body = msg['body'].split(" ")

	return (body[0], body[1:]) if len(body) > 1 else (body[0], [])
