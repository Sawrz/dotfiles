import os
import argparse
from wm_utils import LockScreen

theme_colors = {
    'primary': '#4ec2e8',
    'primary_light': '#88f5ff',
    'primary_dark': '#0091b6',
    'black': '#272727',
    'black_light': '#686868',
    'black_dark': '#000000',
    'white': '#fafafa',
    'white_light': '#ffffff',
    'white_dark': '#c7c7c7',
    'red': '#F44336',
    'red_light': '#ff7961',
    'red_dark': '#ba000d',
    'green': '#4CAF50',
    'green_light': '#80e27e',
    'green_dark': '#087f23'
}

# Initialize Paths
home_dir = os.path.expanduser('~')
wallpapers_dir = os.path.join(home_dir, 'Pictures/wallpapers/2560x1440/')

lock_screen = LockScreen(bg_image=os.path.join(wallpapers_dir, 'sunset_forest.jpg'), theme_colors=theme_colors)
lock_screen.lock()
