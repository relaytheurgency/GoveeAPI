from flask import Flask, request
import time
import threading
import pexpect
import os
import sys
from constants import server_secret, server_port, devices, color_dict

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

#color
@app.route('/device/<dev>/color/<color>', methods=["GET"])
def color(dev, color):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret and\
        dev in device_keys and color in color_dict.keys():
        os.system("python3 tool.py --device " + dev + \
        " --color " + color_dict[color])
        return "done"
    else:
        return "Empty Request"

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
#rgb
@app.route('/device/<dev>/rgb/<r>/<g>/<b>', methods=["GET"])
def rgb(dev,r,g,b):
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
