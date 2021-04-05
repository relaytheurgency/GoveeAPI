from random import randint
import time
import pexpect
import signal
import sys
from constants import *

gatt = pexpect.spawn('gatttool -I')
def exit_gracefully(sig, other):
    gatt.sendline("disconnect")
    gatt.sendline("quit")
    sys.exit(1)
signal.signal(signal.SIGINT, exit_gracefully)
def int_to_hex(intv):
    h = hex(intv).replace("0x", "")
    while len(h) < 2:
        h = "0" + h
    return h
def get_on():
    sig = (51 ^ 1 ^ 1)
    bins = [51, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_off():
    sig = (51 ^ 1)
    bins = [51, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)

def get_rgb_hex(r,g,b):
    sig = (51) ^ (5) ^ (2) ^ r ^ g ^ b
    #bins = [51, 5, 2, r, g, b, 0, 255, 174, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins = [51, 5, 2, r, g, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_brightness_hex(bright):
    bright = round((bright*255/100)) # converted to a percentage instead of value to 255.
    sig = (51) ^ (4) ^ bright
    bins = [51, 4, bright, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_music_mode(music,r,g,b):
    if music == "Energic":
        musicnum = 0
        r,g,b = 0, 0, 0
    elif music== "Spectrum":
        musicnum = 1
    elif music== "Rolling":
        musicnum = 2
    else:
        musicnum = 3
        r,g,b =0, 0, 0
    sig = ((51)^(5)^(1)^musicnum^r^g^b)
    bins = bins = [51, 5, 1, musicnum,0, r, g, b, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_scene(scene):
    if scene == "Sunrise":
        scenenum = 0
    elif scene == "Sunset":
        scenenum = 1
    elif scene == "Movie":
        scenenum = 4
    elif scene == "Dating":
        scenenum = 5
    elif scene == "Romantic":
        scenenum = 7
    elif scene == "Blinking":
        scenenum = 8
    elif scene == "Candlelight":
        scenenum = 9
    else:
        scenenum = 15
    sig = ((51)^(5)^(4)^scenenum)
    bins = [51, 5, 4, scenenum, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)

def write_data(data, addr):
    gatt.sendline(f"connect {addr}")
    try:
        gatt.expect("Connection successful", timeout=5)
    except pexpect.exceptions.TIMEOUT:
        dev = addr_dev_dict[addr]
        print(f"Failed to connect to {dev} {addr}")
        return

    gatt.sendline(f"char-write-req {handle_hex} {data}")
    gatt.expect(".*")
    gatt.sendline("disconnect")
    gatt.expect(".*")
def send_keepalive(addr):
    hexstr = keepalive
    write_data(hexstr,addr)
    print(f"Sent keepalive to {addr_dev_dict[addr]}")
def turn_on(addr):
    hexstr = get_on()
    write_data(hexstr,addr)
    print(f"Turned {addr_dev_dict[addr]} On")
def turn_off(addr):
    hexstr = get_off()
    write_data(hexstr,addr)
    print(f"Turned {addr_dev_dict[addr]} Off")
def change_color(rgbt, addr):
    r, g, b = rgbt
    hexstr = get_rgb_hex(r,g,b)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} color to {rgbt}")

def change_brightness(bright, addr):
    hexstr = get_brightness_hex(bright)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} brightness to {bright}%")
def change_music(music, rgbt, addr):
    r, g, b = rgbt
    hexstr = get_music_mode(music,r,g,b)
    print(hexstr)
    write_data(hexstr, addr)
    if music=="Energic" or music=="Rhythm":
        print(f"Changed {addr_dev_dict[addr]} Music mode to {music}")
    else:
        print(f"Changed {addr_dev_dict[addr]} Music mode to {music} and Color to {rgbt}")
def change_scene(scene, addr):
    hexstr = get_scene(scene)
    print(hexstr)
    write_data(hexstr, addr)
    print(f"Changed {addr_dev_dict[addr]} Scene to {scene}")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def change_color_all(rgbt):
    for addr in devices.values():
        change_color(rgbt, addr)
def change_brightness_both(bright):
    for addr in devices.values():
        change_brightness(bright, addr)
def gen_rand_color():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    max_c = max([r,g,b])
    factor = 255/max_c
    rp = round(r*factor)
    gp = round(g*factor)
    bp = round(b*factor)
    rgbt = (rp, gp, bp)
    return rgbt
