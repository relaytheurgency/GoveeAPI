# format- "device-name": "device-address"
devices = {"led":"A4:C1:38:A8:F5:79",
        "bulb1":"A4:C1:38:75:B1:55",
        "bulb2":"A4:C1:38:29:FD:39"
}
device_modes = ['set','on','off','strobe','diy']
device_names = list(devices.keys())
music_modes=['Energic','Spectrum','Rolling','Rhythm']
scene_modes=['Sunrise','Sunset','Movie','Dating','Romantic','Blinking','Candlelight','Snowflake']
addr_dev_dict = {v:k for k,v in devices.items()}
handle = 21
handle_hex = "0x{:04x}".format(handle)
keepalive ="aa010000000000000000000000000000000000ab"
server_secret = ""
server_port = 5000
color_dict = {
        "red": "255 0 0",
        "green": "0 255 0",
        "blue": "0 0 255",
        "crimson": "220 20 60",
        "cyan": "0 255 255",
        "fuchsia": "255 0 255",
        "gold": "255 215 0",
        "lavender": "230 230 250",
        "lime": "50 205 50",
        "magenta": "139 0 139",
        "orange": "255 165 0",
        "pink": "255 192 203",
        "purple": "128 0 128",
        "salmon": "250 128 114",
        "sky": "135 206 235",
        "teal": "0 128 128",
        "turquoise": "64 224 208",
        "violet": "238 130 238",
        "yellow": "255 255 0"
        }
