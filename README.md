Halibot
-------

Introducing *Halibot!* The worlds most astounding saltwater xmpp bot! Its diet primarily consists
of modules that it finds in the directory termed `modules`, and is highly prized among the xmpp
community for its ease of use, ease of module implementation, and ease of digestion.


Configuration
-------------

Halibot expects in the same directory as it is run, to be a JSON-formatted file called `config.json`.
Below is a list of top-level keys and their significance.
Module config options are documented somewhere else probably.

- `admins` : Array of jid's that should be allowed to run admin commands.
- `jid` : User for the bot to connect with.
- `muc` : Array of JSON objects with a `nick` and `room` keys. (See sample config)

Sample Configuration

```
{
    "admins": [
        "somemoderator@xmpp.server.net"
    ],
    "jid": "username@xmpp.server.net/resource",
    "modules": [
        "Config",
        "Help",
        "Admin",
        "Cat",
        "Ddg",
        "Toys",
        "Xkcd",
        "Quotes",
        "Greeting",
        "Cleverbot",
        "Dorp",
        "Irc"
    ],
    "muc": [
        {
            "nick": "Hal",
            "room": "room@conference.xmpp.server.net"
        }
    ]
}

```


Modules
-------

(todo)
