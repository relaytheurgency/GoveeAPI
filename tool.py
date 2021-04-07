from controller import *
import time
from math import floor
import argparse
import signal
from constants import *
from threading import Thread

"""
    To parse device option passed to command line, enter in device names (bed, window, shelf, etc)
    followed by an list consisting of their address. If you have a 'scene' like a bedroom consisting
    of multiple devices, enter them all into the list.
    Include 'all' as a list of all of your device addresses as well.
"""
name_addr_dict = devices

ps = argparse.ArgumentParser(description="Govee Home Control Script")
device_choices = device_names.append("all")
ps.add_argument('--mode', default="set", type=str, choices=device_modes)
ps.add_argument('--device', default="all", type=str, choices=device_choices)
ps.add_argument('--brightness', type=int)
ps.add_argument('--color', nargs=3, type=int)
ps.add_argument('--period', type=float)
ps.add_argument('--music', type=str, choices=music_modes)
ps.add_argument('--scene',type=str,choices=scene_modes)
ps.add_argument('--keepalive', type=str)
args = ps.parse_args()

if args.device == "all":
    chosen_devices = list(name_addr_dict.values())
else:
    chosen_devices = [name_addr_dict[args.device]]

if args.mode == "set":
    #device = "led" ## can remove if more than one device added for simplicity
    if args.brightness is not None:
        bright = args.brightness
        for device in chosen_devices:
            Thread(target=change_brightness, args=(bright, device, )).start()
    if args.color is not None and args.music is None:
        colort = tuple(args.color)
        for device in chosen_devices:
            Thread(target=change_color, args=(colort, device, )).start()
    if args.music is not None:
        music = args.music
        colort=tuple(args.color)
        for device in chosen_devices:
            Thread(target=change_music, args=(music, colort, device, )).start()
    if args.scene is not None:
        scene = args.scene
        for device in chosen_devices:
            Thread(target=change_scene, args=(scene, device, )).start()
    if args.keepalive is not None:
        for device in chosen_devices:
            Thread(target=send_keepalive, args=(device, )).start()
elif args.mode == "on":
    for device in chosen_devices:
        Thread(target=turn_on, args=(device, )).start()
elif args.mode == "off":
    for device in chosen_devices:
        Thread(target=turn_off, args=(device, )).start()
elif args.mode == "strobe":
    latency = args.period
    change_brightness_both(255)
    while True:
        for addr in chosen_devices:
            change_color(gen_rand_color(), addr)
        time.sleep(latency)
