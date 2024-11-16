import argparse
from wm_utils import SoundDevices

# ARGUMENT INTERFACE
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--device_name', required=True, help='name of sound device for output')
args = ap.parse_args()

sound_output = SoundDevices(
    device_aliases={
        "usb_speakers": "Audioengine_Audioengine_2",
        "monitor_speakers": "hdmi-stereo-extra1",
        "headset": "Corsair_CORSAIR_VIRTUOSO",
    })

sound_output.update_device_map()
sound_output.switch(device_name=args.device_name)
