# Released under the MIT License. See LICENSE for details.


from datetime import datetime

import _babase
import setting
from playersData import pdata
from serverData import serverdata

import bascenev1 as bs
from .handlers import check_permissions
from .handlers import clientid_to_accountid

settings = setting.get_settings_data()


def command_type(command):
    """
    Checks The Command Type

    Parameters:
        command : str

    Returns:
        any
    """
    if command in NormalCommands.Commands or command in NormalCommands.CommandAliases:
        return "Normal"

    if command in Management.Commands or command in Management.CommandAliases:
        return "Manage"

    if command in Fun.Commands or command in Fun.CommandAliases:
        return "Fun"

    if command in Cheats.Commands or command in Cheats.CommandAliases:
        return "Cheats"


def execute(msg, clientid):
    """
    Command Execution

    Parameters:
        msg : str
        clientid : int

    Returns:
        any
    """
    command = msg.lower().split(" ")[0].split("/")[1]
    arguments = msg.lower().split(" ")[1:]
    accountid = clientid_to_accountid(clientid)
    print("checking command type")
    print(command_type(command))
    if command_type(command) == "Normal":
        NormalCommands.ExcelCommand(command, arguments, clientid, accountid)

    elif command_type(command) == "Manage":
        if check_permissions(accountid, command):
            Management.ExcelCommand(command, arguments, clientid, accountid)
            bs.broadcastmessage("Executed", transient=True, clients=[clientid])
        else:
            bs.broadcastmessage("access denied", transient=True,
                                clients=[clientid])

    elif command_type(command) == "Fun":
        if check_permissions(accountid, command):
            Fun.ExcelCommand(command, arguments, clientid, accountid)
            bs.broadcastmessage("Executed", transient=True, clients=[clientid])
        else:
            bs.broadcastmessage("access denied", transient=True,
                                clients=[clientid])

    elif command_type(command) == "Cheats":
        if check_permissions(accountid, command):
            Cheats.ExcelCommand(command, arguments, clientid, accountid)
            bs.broadcastmessage("Executed", transient=True, clients=[clientid])
        else:
            bs.broadcastmessage("access denied", transient=True,
                                clients=[clientid])
    now = datetime.now()
    if accountid in pdata.get_blacklist()[
        "muted-ids"] and now < datetime.strptime(
        pdata.get_blacklist()["muted-ids"][accountid]["till"],
        "%Y-%m-%d %H:%M:%S"):
        bs.broadcastmessage("You are on mute", transient=True,
                            clients=[clientid])
        return None
    if serverdata.muted:
        return None
    if settings["ChatCommands"]["BrodcastCommand"]:
        return msg
    return None


def QuickAccess(msg, client_id):
    from bascenev1lib.actor import popuptext
    if msg.startswith(","):
        name = ""
        teamid = 0
        for i in bs.get_foreground_host_session().sessionplayers:
            if i.inputdevice.client_id == client_id:
                teamid = i.sessionteam.id
                name = i.getname(True)

        for i in bs.get_foreground_host_session().sessionplayers:
            if hasattr(i,
                       'sessionteam') and i.sessionteam and teamid == i.sessionteam.id and i.inputdevice.client_id != client_id:
                bs.broadcastmessage(name + ":" + msg[1:],
                                    clients=[i.inputdevice.client_id],
                                    color=(0.3, 0.6, 0.3), transient=True)

        return None
    elif msg.startswith("."):
        msg = msg[1:]
        msgAr = msg.split(" ")
        if len(msg) > 25 or int(len(msg) / 5) > len(msgAr):
            bs.broadcastmessage("msg/word length too long",
                                clients=[client_id], transient=True)
            return None
        msgAr.insert(int(len(msgAr) / 2), "\n")
        for player in _babase.get_foreground_host_activity().players:
            if player.sessionplayer.inputdevice.client_id == client_id and player.actor.exists() and hasattr(
                player.actor.node, "position"):
                pos = player.actor.node.position
                with bs.get_foreground_host_activity().context:
                    popuptext.PopupText(
                        " ".join(msgAr),
                        (pos[0], pos[1] + 1, pos[2])).autoretain()
                return None
        return None