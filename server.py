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

app = Flask(__name__)

console = pexpect.spawn("bash")
#on
@app.route('/on', methods=["GET"])
def on():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --mode on")
        return "done"
    else:
        return "Empty request"
#off
@app.route('/off', methods=["GET"])
def off():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --mode off")
        return "done"
    else:
        return "Empty request"
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
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        command_str = f"python3 tool.py --device {dev} --mode on"
        os.system(command_str)
        return "done"
    else:
        return "Empty request"
#device off
@app.route('/device/<dev>/off', methods=["GET"])
def dev_off(dev):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        command_str = f"python3 tool.py --device {dev} --mode off"
        os.system(command_str)
        return "done"
    else:
        return "Empty request"
#brightness
@app.route('/brightness/<bright>', methods=["GET"])
def bright(bright):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --brightness " + bright)
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
@app.route('/strobe', methods=["GET"])
def strobe():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --mode strobe --period .3")
        return "done"
    else:
        return "Bad request"
#########################################################################################################################################################

#red
@app.route('/red', methods=["GET"])
def red():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 255 0 0")
        return "done"
    else:
        return "Empty request"

#green
@app.route('/green', methods=["GET"])
def green():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 0 255 0")
        return "done"
    else:
        return "Empty request"

#blue
@app.route('/blue', methods=["GET"])
def blue():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 0 0 255")
        return "done"
    else:
        return "Empty request"

#crimson
@app.route('/crimson', methods=["GET"])
def crimson():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 220 20 60")
        return "done"
    else:
        return "Empty request"

#cyan
@app.route('/cyan', methods=["GET"])
def cyan():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 0 255 255")
        return "done"
    else:
        return "Empty request"

#fuchsia
@app.route('/fuchsia', methods=["GET"])
def fuchsia():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 255 0 255")
        return "done"
    else:
        return "Empty request"

#gold
@app.route('/gold', methods=["GET"])
def gold():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 255 215 0")
        return "done"
    else:
        return "Empty request"

#lavender
@app.route('/lavender', methods=["GET"])
def lavender():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 230 230 250")
        return "done"
    else:
        return "Empty request"

#lime
@app.route('/lime', methods=["GET"])
def lime():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 50 205 50")
        return "done"
    else:
        return "Empty request"

#magenta
@app.route('/magenta', methods=["GET"])
def magenta():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 139 0 139")
        return "done"
    else:
        return "Empty request"

#orange
@app.route('/orange', methods=["GET"])
def orange():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 255 165 0")
        return "done"
    else:
        return "Empty request"

#pink
@app.route('/pink', methods=["GET"])
def pink():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 255 192 203")
        return "done"
    else:
        return "Empty request"

#purple
@app.route('/purple', methods=["GET"])
def purple():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 128 0 128")
        return "done"
    else:
        return "Empty request"

#salmon
@app.route('/salmon', methods=["GET"])
def salmon():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 250 128 114")
        return "done"
    else:
        return "Empty request"

#sky
@app.route('/sky', methods=["GET"])
def sky():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 135 206 235")
        return "done"
    else:
        return "Empty request"

#teal
@app.route('/teal', methods=["GET"])
def teal():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 0 128 128")
        return "done"
    else:
        return "Empty request"

#turquoise
@app.route('/turquoise', methods=["GET"])
def turquoise():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 64 224 208")
        return "done"
    else:
        return "Empty request"

#violet
@app.route('/violet', methods=["GET"])
def violet():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 238 130 238")
        return "done"
    else:
        return "Empty request"

#yellow
@app.route('/yellow', methods=["GET"])
def yellow():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color 255 255 0")
        return "done"
    else:
        return "Empty request"

#energic
@app.route('/energic', methods=["GET"])
def energic():
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --music Energic --color 0 0 0")
        return "done"
    else:
        return "Empty request"
#########################################################################################################################################################
#color
@app.route('/color/<r>/<g>/<b>', methods=["GET"])
def color(r,g,b):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --color " + r + " " + g + " " + b)
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
@app.route('/scene/<scene_mode>', methods=["GET"])
def scene(scene_mode):
    args_dict = request.args.to_dict()
    if "key" in args_dict.keys() and args_dict["key"] == server_secret:
        os.system("python3 tool.py --scene " + scene_mode.capitalize()  )
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
