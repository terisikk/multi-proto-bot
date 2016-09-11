
def new_user(name):
    return {"name": name}

def new_ircuser(nickname, username=None, ircname=None):
    user = new_user(username or nickname)
    user["ircname"] = ircname or nickname
    user["nickname"] = nickname
    return user