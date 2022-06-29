'''
Written by Thomas Munzer (tmunzer@juniper.net)
Github repository: https://github.com/tmunzer/Mist_library/
'''

#######################################################################################################################################
#######################################################################################################################################
############################################# IMPORTS
#######################################################################################################################################
import requests
import random

from requests.api import get
from mist_smtp.mist_smtp import Mist_SMTP
from datetime import datetime
import os
from dotenv import load_dotenv
import getopt
import sys
#######################################################################################################################################
#######################################################################################################################################
############################################# CONF LOAD


#######################################################################################################################################
#### SMTP CONFIG
def _load_smtp(verbose):
    smtp_config = {
        "enabled": eval(os.environ.get("MIST_SMTP_ENABLED", default=False)),
        "host": os.environ.get("MIST_SMTP_HOST", default=None),
        "port": os.environ.get("MIST_SMTP_PORT", default=587),
        "use_ssl": eval(os.environ.get("MIST_SMTP_SSL", default=True)),
        "username": os.environ.get("MIST_SMTP_USER", default=None),
        "password": os.environ.get("MIST_SMTP_PASSWORD", default=None),
        "from_name": os.environ.get("MIST_SMTP_FROM_NAME", default="Wi-Fi Access"),
        "from_email": os.environ.get("MIST_SMTP_FROM_EMAIL", default=None),
        "logo_url": os.environ.get("MIST_SMTP_LOGO_URL", default="https://cdn.mist.com/wp-content/uploads/logo.png"),
        "enable_qrcode": eval(os.environ.get("MIST_SMTP_QRCODE", default=True))
    }    
    if (smtp_config["enabled"]):
        mist_smtp = Mist_SMTP(smtp_config)
    else:
        mist_smtp = None

    if verbose:
        print("".ljust(80, "-"))
        print(" SMTP CONFIG ".center(80))
        print("")    
        print("enabled       : {0}".format(smtp_config["enabled"]))
        print("host          : {0}".format(smtp_config["host"]))
        print("port          : {0}".format(smtp_config["port"]))
        print("use_ssl       : {0}".format(smtp_config["use_ssl"]))
        print("username      : {0}".format(smtp_config["username"]))
        print("from_name     : {0}".format(smtp_config["from_name"]))
        print("from_email    : {0}".format(smtp_config["from_email"]))
        print("logo_url      : {0}".format(smtp_config["logo_url"]))
        print("enable_qrcode : {0}".format(smtp_config["enable_qrcode"]))
        print("")

    return mist_smtp

#############################################
#### Mist CONFIG

def _load_mist(verbose):
    mist_config = {
        "host": os.environ.get("MIST_HOST", default=None),
        "api_token": os.environ.get("MIST_API_TOKEN", default=None),
        "scope": os.environ.get("MIST_SCOPE", default=None),
        "scope_id": os.environ.get("MIST_SCOPE_ID", default=None),
        "wlan_id": os.environ.get("MIST_WLAN_ID", default=None)
    }
    if not mist_config["host"]: 
        print("ERROR: Missing the MIST HOST")
        sys.exit(1)
    if not mist_config["api_token"]: 
        print("ERROR: Missing the API TOKEN")
        sys.exit(1)
    if not mist_config["scope"]: 
        print("ERROR: Missing the SCOPE")
        sys.exit(1)
    if not mist_config["scope_id"]: 
        print("ERROR: Missing the scope_id")
        sys.exit(1)
    if not mist_config["wlan_id"]: 
        print("ERROR: Missing the wlan_id")
        sys.exit(1)

    if verbose:
        print("".ljust(80, "-"))
        print(" MIST CONFIG ".center(80))
        print("")
        print("host    : {0}".format(mist_config["host"]))
        print("scope    : {0}".format(mist_config["scope"]))
        print("scope_id : {0}".format(mist_config["scope_id"]))
        print("wlan_id  : {0}".format(mist_config["wlan_id"]))
        print("")

    return mist_config

#############################################
#### PSK CONFIG

def _load_psk(verbose):
    psk_config = {
        "length": int(os.environ.get("MIST_PSK_LENGTH", default=12)),
        "allowed_chars": os.environ.get("MIST_PSK_ALLOWED_CHARS", default="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"),
        "recipients": os.environ.get("MIST_PSK_RECIPIENTS","").split(",")
    }    

    if verbose:
        print("".ljust(80, "-"))
        print(" PSK CONFIG ".center(80))
        print("")
        print("length        : {0}".format(psk_config["length"]))
        print("allowed chars : {0}".format(psk_config["allowed_chars"]))
        print("recipients    : {0}".format(psk_config["recipients"]))
        print("")
    
    return psk_config

#######################################################################################################################################
#######################################################################################################################################
############################################# FUNCTIONS
#######################################################################################################################################

def _generate_psk(psk_config):
    print("Generating new PSK ".ljust(79, "."), end="", flush=True)
    try:
        psk = ''.join(random.choice(psk_config["allowed_chars"]) for i in range(psk_config["length"]))        
        print("\033[92m\u2714\033[0m")
        return  psk
    except:
        print('\033[31m\u2716\033[0m')
        sys.exit(255)

def _update_psk(mist_config, psk):
    headers = {
        "Authorization": "Token {0}".format(mist_config["api_token"])
    }
    url = "https://{0}/api/v1/{1}s/{2}/wlans/{3}".format(mist_config["host"], mist_config["scope"], mist_config["scope_id"], mist_config["wlan_id"])
    try:
        print("Retrieving current WLAN configuration ".ljust(79, "."), end="", flush=True)
        wlan = requests.get(url, headers=headers)   
        if (wlan.status_code != 200):
            raise
        auth = wlan.json().get("auth")  
        ssid = wlan.json().get("ssid")
        print("\033[92m\u2714\033[0m")        
    except:
        print('\033[31m\u2716\033[0m')
        if wlan.json():
            print(wlan.json())
    try: 
        print("Updating WLAN PSK configuration ".ljust(79, "."), end="", flush=True)
        auth["psk"]=psk
        wlan = requests.put(url, headers=headers, json={"auth": auth})
        if (wlan.status_code == 200):
            print("\033[92m\u2714\033[0m") 
            print("Validating the configuration change ".ljust(79, "."), end="", flush=True)
            auth = wlan.json().get("auth")  
            if auth.get("psk") == psk:
                print("\033[92m\u2714\033[0m")  
                return ssid
            else:
                raise
        else: 
            raise
    except:
        print('\033[31m\u2716\033[0m')
        return False

def _chck_only():
        _load_smtp(True)
        _load_mist(True)
        _load_psk(True)

def _run(check):
        mist_smtp =_load_smtp(check)
        mist_config= _load_mist(check)
        psk_config = _load_psk(check)
        print("".ljust(80,"-"))
        print("New Turn - {0}".format(datetime.now().ctime()).center(80))
        psk = _generate_psk(psk_config)
        ssid = _update_psk(mist_config, psk)
        if ssid and mist_smtp:
            mist_smtp.send_psk(psk,ssid, psk_config["recipients"] )


def usage():
    print("""
---
Usage:
-c, --check         Check the configuration file only and display the values 
                    (passowrds and tokens are not shown)

-e, --env=file      Configuration file location. By default the script
                    is looking for a ".env" file in the script root folder

-a, --all           Check the configuration file (-c) and run the script

---
Configuration file example:
MIST_SMTP_ENABLED = True
MIST_SMTP_HOST = "smtp.myserver.com"
MIST_SMTP_PORT = 587
MIST_SMTP_SSL = True
MIST_SMTP_USER = "my.user"
MIST_SMTP_PASSWORD = "xxxxxxxxxxxxxxxx"
MIST_SMTP_FROM_NAME = "Wi-Fi Access"
MIST_SMTP_FROM_EMAIL = "my.user@myserver.com"
MIST_SMTP_LOGO_URL = "https://cdn.mist.com/wp-content/uploads/logo.png"
MIST_SMTP_QRCODE = True

MIST_HOST = "api.mist.com"
MIST_API_TOKEN = "xxxxxxxxxxxxxxxxx"
MIST_SCOPE = "org" # site or org
MIST_SCOPE_ID = "xxxxxxxxxxxxxx" # site_id or org_id depending on the scope
MIST_WLAN_ID = "xxxxxxxxxxxxxx"

MIST_PSK_LENGTH = "12"
MIST_PSK_ALLOWED_CHARS = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"

MIST_PSK_RECIPIENTS = user.1@myserver.com,user.2@myserver.com
    """)

def main():    
    print("""

Python Script to rotate Mist PSK.
Written by Thomas Munzer (tmunzer@juniper.net)
Github: https://github.com/tmunzer/mist_psk_rotate

""")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ce:ah", ["check", "env=", "all", "help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    check = False
    check_only = False
    env_file = None
    for o, a in opts:
        if o in ["-h", "--help"]:
            usage()
            sys.exit()
        elif o in ["-c", "--check"]:
            check_only=True
        elif o in ["-a", "--all"]:
            check=True
        elif o in ["-e", "--env"]:
            env_file = a
        else:
            assert False, "unhandled option"
  
    if env_file:
        load_dotenv(dotend_path=env_file)
    else:
        load_dotenv()

    if check_only:
        _chck_only()
    else: 
        _run(check)

#######################################################################################################################################
#######################################################################################################################################
############################################# ENTRYPOINT
#######################################################################################################################################
if __name__=="__main__":
        main()

