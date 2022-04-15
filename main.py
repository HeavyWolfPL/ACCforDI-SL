import re
from datetime import datetime
from requests import get, post, exceptions

print("╔══════════════════════════════════════════════════════╗")
print("║                       SL-DICC                        ║")
print("║ Dynamic IP Config Changer for SCP: Secret Laboratory ║")
print("║                                                      ║")
print("║ This is not an official tool from Northwood Studios! ║")
print("║      Northwood is not responsible for any damage     ║")
print("╠══════════════════════════════════════════════════════╣")
print("║        https://github.com/HeavyWolfPL/SL-DICC        ║")
print("╚══════════════════════════════════════════════════════╝")

# Examples:
# Linux - "/home/scpsl/.config/SCP Secret Laboratory/config/7777"
# Windows - "C:\Users\wafel\AppData\Roaming\SCP Secret Laboratory\config\7777"
# You must not use %appdata% in the path.
path = "/home/scpsl/.config/SCP Secret Laboratory/config/7777"

# This is a Discord Webhook URL. Webhook will be sent when an error in encountered and optionally on successful config change.
# Set it to "" if you don't want to use it at all.
webhook_url = ""
webhook_on_success =  True
webhook_on_no_change = False

def configValidator():
    valid = True
    if webhook_url != "":
        if re.search("discord.com\/api\/webhooks\/([^\/]+)\/([^\/]+)", webhook_url) == None:
            print("Webhook URL is invalid.")
            valid = False
        if webhook_on_success not in [True, False]:
            print("Boolean value for webhook_on_success is invalid.")
            valid = False
        if webhook_on_no_change not in [True, False]:
            print("Boolean value for webhook_on_no_change is invalid.")
            valid = False
        
    if not valid: # tell me there's a better way of doing this shit
        exit()
configValidator()

def getIP():
    ip = get('https://api.ipify.org').content.decode('utf8')
    print('Public adress according to API: {}'.format(ip))

    ipRegex = re.search("^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$", ip)
    if not ipRegex:
        print("IPv4 not detected. Make sure you're connected to the internet and nothing is blocking the connection. \nYou may only have a IPv6 or the API can't detect it. \nIf you have any questions, contact me on discord (Wafel#8871) or make a github issue.")
    return ip

def updateConfig(ip):
    try:
        with open(f"{path}/config_gameplay.txt", "r+") as file:
            content = file.read().split("\n")
            ip_index = [i for i, item in enumerate(content) if re.search('server_ip:', item)] # Look for multiple server_ip lines
            if len(ip_index) > 1:
                return [False, "You have 2 server_ip values in your config, remove one of them."]
            
            ip_index = [i for i, item in enumerate(content) if re.search('server_ip: ((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$', item)] # Look for the full line
            if len(ip_index) == 0:
                ip_index = [i for i, item in enumerate(content) if re.search('server_ip: auto$', item)]  # Look for server_ip set to auto
                if len(ip_index) == 0:
                    return [False, "No server_ip values found. Please check if your config file includes a 'server_ip:' line with IPv4/auto value. \n\nExamples: \n'server_ip: 1.13.78.123'\n'server_ip: auto'"]
            
            old_ip = content[ip_index[0]].split(" ")[1]
            print("Currently set value: {}".format(old_ip))
            if old_ip == ip:
                return ["NoChanges", "IP is already set to the current value."]
            file.seek(0)
            file.truncate(0)
            content[ip_index[0]] = f"server_ip: {ip}"
            file.write("\n".join(content))
            return [True, ip, old_ip]

    except FileNotFoundError:
        return [False, "Config file not found. Make sure you have a proper config path set!"]
    except PermissionError:
        return [False, "Config file is not writable. Make sure you have permissions to run the file!"]

def sendWebhook(success, params):
    if success == True:
        if not webhook_on_success:
            return
        color = 0x00FF00
        title = "IP Updated!"
    elif success == "NoChanges":
        if not webhook_on_no_change:
            return
        color = 0x00AAFF
        title = "IP is already set to the current value."
    else:
        color = 0xFF0000
        title = "IP Update Failed!"

    data = {
        "embeds": [{
            "description" : params,
            "color": color,
            "author": {
                "name": "SL-DICC | {}".format(title),
                "url": "https://github.com/HeavyWolfPL/SL-DICC"
            },
            "footer": {
                "text": "SL-DICC by Wafel#8871",
                "icon_url": "https://i.imgur.com/g3a3tLo.png"
            },
            "timestamp": datetime.now().isoformat()
        }]
    }
    webhook = post(webhook_url, json = data)
    try:
        webhook.raise_for_status()
    except exceptions.HTTPError as err:
        print("\nSomething went wrong while sending a webhook. Error: \n---------------- \n{} \n---------------- \n\nIf this is a mistake, contact me on discord (Wafel#8871) or make a github issue.".format(err))

ip = getIP()
result = updateConfig(ip)

if result[0] == False:
    sendWebhook(False, "**Something went wrong.** \n```{}```".format(result[1]))
    print("\nSomething went wrong. Error: \n---------------- \n{} \n---------------- \n\nIf this is a mistake, contact me on discord (Wafel#8871) or make a github issue.".format(result[1]))

elif result[0] == "NoChanges":
    sendWebhook("NoChanges", "No changes made. Proper IP is already set in the config.")
    print("\nNo changes made. Proper IP is already set in the config.")

else:
    sendWebhook(True, "IP changed from `{old}` to `{new}`".format(old=result[2], new=result[1]))
    print("\nSuccessfully updated config file! Server IP set to: {}.".format(result[1]))