from utils import SoundDevices
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--device', required=True, help='name of sound device')
args = ap.parse_args()

sound_output = SoundDevices(device_aliases={"speakers": "Audioengine_Audioengine_2",
                                            "hdmi": "hdmi-stereo"})

sound_output.switch(args.device)
