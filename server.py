from flask import Flask, request
import time
import threading
import pexpect
import os
import sys
from constants import server_secret, server_port, devices

# added this to start server in cron
# since paths aren't absolute
os.chdir("/home/pi/GoveeAPI")

# Adding a keeaplive thread so that commands fail less
def keepalive_loop():
    while True:
        time.sleep(30.0)
        os.system("python3 tool.py --keepalive on")

# Create key of devices so you can test for membership
device_keys = list(devices.keys())
device_keys.append("all")

app = Flask(__name__)

#devices
@app.route('/device_list', methods=["GET"])
def device_list():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        return devices
    else:
        return "Empty request"
#device on
@app.route('/device/<dev>/on', methods=["GET"])
def dev_on(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        command_str = f"python3 tool.py --device {dev} --mode on"
        os.system(command_str)
        return "done"
    else:
        return "Empty request"
#device off
@app.route('/device/<dev>/off', methods=["GET"])
def dev_off(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        command_str = f"python3 tool.py --device {dev} --mode off"
        os.system(command_str)
        return "done"
    else:
        return "Empty request"
#brightness
@app.route('/device/<dev>/brightness/<bright>', methods=["GET"])
def bright(dev, bright):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --brightness " + bright)
        return "done"
    else:
        return "Empty request"

#########################################################################################################################################################
@app.route('/alarm', methods=["POST", "GET"])
def alarm():
    if request.method == "POST":
        rdict = request.form.to_dict()
        if "alarm" in rdict.keys():
            alarm = request.form["alarm"].replace(" at ", "").replace(" : ", ":").replace(" . ", ".").replace(" .", ".")
            correct_ampm_alarm = alarm.replace("a.m.", "AM").replace("p.m.", "PM")
            is_day_before = (time.strftime("%p") == "PM")
            time_str = correct_ampm_alarm + " tomorrow" if is_day_before else correct_ampm_alarm
            command_str = f"at {time_str} -f ./start_bright_increase.sh"
            print(command_str)
            os.system(command_str)
            return "done"
        else:
            return "Bad request"
    else:
        return "Empty request"
#########################################################################################################################################################
@app.route('/device/<dev>/strobe', methods=["GET"])
def strobe(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --mode strobe --device " + dev + " --period .3")
        return "done"
    else:
        return "Bad request"
#########################################################################################################################################################

#red
@app.route('/device/<dev>/red', methods=["GET"])
def red(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 255 0 0")
        return "done"
    else:
        return "Empty request"

#green
@app.route('/device/<dev>/green', methods=["GET"])
def green(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 0 255 0")
        return "done"
    else:
        return "Empty request"

#blue
@app.route('/device/<dev>/blue', methods=["GET"])
def blue(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 0 0 255")
        return "done"
    else:
        return "Empty request"

#crimson
@app.route('/device/<dev>/crimson', methods=["GET"])
def crimson(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 220 20 60")
        return "done"
    else:
        return "Empty request"

#cyan
@app.route('/device/<dev>/cyan', methods=["GET"])
def cyan(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 0 255 255")
        return "done"
    else:
        return "Empty request"

#fuchsia
@app.route('/device/<dev>/fuchsia', methods=["GET"])
def fuchsia(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 255 0 255")
        return "done"
    else:
        return "Empty request"

#gold
@app.route('/device/<dev>/gold', methods=["GET"])
def gold(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 255 215 0")
        return "done"
    else:
        return "Empty request"

#lavender
@app.route('/device/<dev>/lavender', methods=["GET"])
def lavender(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 230 230 250")
        return "done"
    else:
        return "Empty request"

#lime
@app.route('/device/<dev>/lime', methods=["GET"])
def lime(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 50 205 50")
        return "done"
    else:
        return "Empty request"

#magenta
@app.route('/device/<dev>/magenta', methods=["GET"])
def magenta(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 139 0 139")
        return "done"
    else:
        return "Empty request"

#orange
@app.route('/device/<dev>/orange', methods=["GET"])
def orange(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 255 165 0")
        return "done"
    else:
        return "Empty request"

#pink
@app.route('/device/<dev>/pink', methods=["GET"])
def pink(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 255 192 203")
        return "done"
    else:
        return "Empty request"

#purple
@app.route('/device/<dev>/purple', methods=["GET"])
def purple(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 128 0 128")
        return "done"
    else:
        return "Empty request"

#salmon
@app.route('/device/<dev>/salmon', methods=["GET"])
def salmon(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 250 128 114")
        return "done"
    else:
        return "Empty request"

#sky
@app.route('/device/<dev>/sky', methods=["GET"])
def sky(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 135 206 235")
        return "done"
    else:
        return "Empty request"

#teal
@app.route('/device/<dev>/teal', methods=["GET"])
def teal(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 0 128 128")
        return "done"
    else:
        return "Empty request"

#turquoise
@app.route('/device/<dev>/turquoise', methods=["GET"])
def turquoise(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 64 224 208")
        return "done"
    else:
        return "Empty request"

#violet
@app.route('/device/<dev>/violet', methods=["GET"])
def violet(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 238 130 238")
        return "done"
    else:
        return "Empty request"

#yellow
@app.route('/device/<dev>/yellow', methods=["GET"])
def yellow(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color 255 255 0")
        return "done"
    else:
        return "Empty request"

#energic
@app.route('/device/<dev>/energic', methods=["GET"])
def energic(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --music Energic --color 0 0 0")
        return "done"
    else:
        return "Empty request"
#########################################################################################################################################################
#color
@app.route('/device/<dev>/color/<r>/<g>/<b>', methods=["GET"])
def color(dev,r,g,b):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --color " + r + " " + g + " " + b)
        return "done"
    else:
        return "Empty request"

#music
@app.route('/music/<music_mode>/<r>/<g>/<b>', methods=["GET"])
def music(music_mode,r,g,b):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --music " + music_mode + " --color " + r + " " + g + " " + b)
        return "done"
    else:
        return "Empty request"

#scenes
@app.route('/device/<dev>/scene/<scene_mode>', methods=["GET"])
def scene(dev, scene_mode):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
            dev in device_keys:
        os.system("python3 tool.py --device " + dev + " --scene " + scene_mode.capitalize()  )
        return "done"
    else:
        return "Empty request"


#############################################################################################################################################################################
@app.route('/end_strobe')
def end():
    console.sendintr()
    return "Done"
##########################################################################################################################################################################



if __name__ == '__main__':
    t_keepalive = threading.Thread(target=keepalive_loop)
    t_keepalive.setName("keepalivethread")
    t_keepalive.start()

    app.run(host='0.0.0.0', port=server_port)
