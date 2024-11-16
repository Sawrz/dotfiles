# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, qtile
from libqtile.widget import Spacer
from widget_builder import WidgetScreenBuilder

# Main Configuration
# -------------------------------------------------------------------------------------
# Modifiers
#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"

# Initialize Paths
home = os.path.expanduser('~')

# Set Lazy Functions
'''
@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)
'''

# Keybindings
# -------------------------------------------------------------------------------------
keys = [

    # Most of our keybindings are in sxhkd file - except these

    # Manipulate Sound Volume
    # Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+")),
    # Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-")),
    # Key([], "XF86AudioMute", lazy.spawn("amixer sset Master toggle")),

    # SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "a", lazy.to_screen(2), desc="Keyboard focus to monitor 1"),
    Key([mod], "s", lazy.to_screen(0), desc="Keyboard focus to monitor 2"),
    Key([mod], "d", lazy.to_screen(1), desc="Keyboard focus to monitor 3"),
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),

    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "shift"], "r", lazy.restart()),

    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "Tab", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),

    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
]

# Groups
# ----------------------------------------------------------------------------------
# Create Matches for Groups
matches = {
    "Web":
    Match(wm_class=[
        "firefox",
        "Google-chrome",
        "chromium",
        "qutebrowser",
        "LibreWolf",
    ]),
    "Misc":
    Match(wm_class=[
        "KeePassXC",
        "Virt-manager",
        "Timeshift-gtk",
        "Nitrogen",
        "Lxappearance",
        "Gwe",

    ]),
    "Dev":
    Match(wm_class=[
        "jetbrains-pycharm",
        "Zeal",
        "code-oss",
        "Atom",
        "Sublime_text",
        "subl",
        "Sublime_merge",
        "neovide",
        "emacs",
    ]),
    "Images":
    Match(wm_class=[
        "Gimp",
        "gimp-2.10",
        "GravitDesigner",
        "Inkscape",
    ]),
    "Video":
    Match(wm_class=[
        "resolve",
        "kdenlive",
    ]),
    "Writing":
    Match(wm_class=[
        "Joplin",
        "lyx",
    ]),
    "Gaming":
    Match(wm_class=[
        "Steam",
    ]),
    "Mail/Chat":
    Match(wm_class=[
        "TelegramDesktop",
        "Evolution",
        "discord",
    ]),
}

# Create Groups
groups = [
    Group(
        name="Web",
        matches=[matches["Web"]],
        exclusive=True,
        position=1,
        layout="max",
        label="",
    ),
    Group(
        name="Dev",
        matches=[matches["Dev"]],
        exclusive=True,
        position=2,
        layout="monadtall",
        label="",
    ),
    Group(
        name="Misc",
        matches=[matches["Misc"]],
        exclusive=False,
        position=3,
        layout="monadtall",
        label="",
    ),
    Group(
        name="Images",
        matches=[matches["Images"]],
        exclusive=False,
        position=4,
        layout="max",
        label="",
    ),
    Group(
        name="Video",
        matches=[matches["Video"]],
        exclusive=False,
        position=5,
        layout="max",
        label="",
    ),
    Group(
        name="Writing",
        matches=[matches["Writing"]],
        exclusive=True,
        position=6,
        layout="max",
        label="",
    ),
    Group(
        name="Gaming",
        matches=[matches["Gaming"]],
        exclusive=False,
        position=7,
        layout="floating",
        label="",
    ),
    Group(
        name="Mail/Chat",
        matches=[matches["Mail/Chat"]],
        exclusive=False,
        position=8,
        layout="monadtall",
        label="",
    ),
]

for group_entry in groups:
    keys.extend([
        #CHANGE WORKSPACES
        Key([mod], str(group_entry.position), lazy.group[group_entry.name].toscreen()),
        Key(["control"], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], str(group_entry.position), lazy.window.togroup(group_entry.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "mod1"], str(group_entry.position), lazy.window.togroup(group_entry.name),
            lazy.group[group_entry.name].toscreen()),
    ])

# Floating Rules
# Run the utility of `xprop` to see the wm class and name of an X client.
float_matches = [
    Match(wm_class="kdenlive"),  # kdenlive
]

intrusive_matches = [
    Match(wm_class="Xed"),
    Match(wm_class="Alacritty"),
    Match(wm_class="Pcmanfm"),
    Match(wm_class="thunar"),
    Match(wm_class="xfce4-terminal"),
    Match(wm_class="urxvt"),
]

intrusive_float_matches = [
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(wm_class="Arcolinux-welcome-app.py"),
    Match(wm_class="Arcolinux-tweak-tool.py"),
    Match(wm_class="Arcolinux-calamares-tool.pya"),
    Match(wm_class="arcolinux-logout"),
    Match(wm_class="arcologout.py"),
    Match(wm_class="arcolinux-betterlockscreen.py"),
    Match(wm_class="pamac-manager"),
    Match(wm_class="xfce4-settings-manager"),
    Match(wm_class="Conky"),
    Match(wm_class="conky"),
    Match(wm_class="systemConky"),
    Match(wm_class="confirmreset"),
    Match(wm_class="makebranch"),
    Match(wm_class="maketag"),
    Match(wm_class="Arandr"),
    Match(wm_class="feh"),
    Match(wm_class="Galculator"),
    Match(wm_class="branchdialog"),
    Match(wm_class="Open File"),
    Match(wm_class="pinentry"),
    Match(wm_class="Gcr-prompter"),
    Match(wm_class="xfce4-appfinder"),
    Match(wm_class="Pinentry-gtk-2"),  # GPG key password entry
    Match(wm_class="ssh-askpass"),  # ssh-askpass
    #Match(wm_class="Ssh-askpass-sublime"),  # Sublime Merge ssh-askpass
    Match(wm_class="pavucontrol"),  # Pavucontrol
    Match(wm_class="Nm-connection-editor"),  # NetworkManager connection editor
    Match(wm_class="File-roller"),  # File Roller
    Match(wm_class="nextcloud"),  # Nextcloud
]

floating_layout_theme = {"border_width": 0,}
floating_layout = layout.Floating(float_rules=float_matches + intrusive_float_matches, **floating_layout_theme)

# Create Rules for Windows not bound to a Group via Match
dgroups_app_rules = [Rule(match, intrusive=True) for match in intrusive_matches + intrusive_float_matches]
dgroups_key_binder = None

# Layouts, Widgets and Screens
# ----------------------------------------------------------------------------------
# # Set Colors
theme_colors = {
    "accent_light": "#6790eb",
    "accent_dark": "#5e81ac",
    "background": "#2F343F",
    "foreground": "#c0c5ce",
    "white": "#f3f4f5",
    "blue": "#3384d0",
    "red": "#cd1f3f",
    "green": "#62FF00",
    "orange": "#fba922",
}

# Add Layouts
layout_theme = {"margin": 5, "border_width": 2, "border_focus": theme_colors["accent_dark"], "border_normal": "#4c566a"}

layouts = [
    layout.Max(),
    layout.xmonad.MonadTall(**layout_theme),
    layout.floating.Floating(**floating_layout_theme),
    layout.Tile(ishift_windows=True, **layout_theme),
]

# Add Screens

widget_defaults = {"font": "Noto Sans", "fontsize": 12, "padding": 2, "background": theme_colors["background"]}

extension_defaults = widget_defaults.copy()

wsb = WidgetScreenBuilder(theme_colors)

main_screen_widgets = ["group_box", "window_name", "clock_time", "system_tray", "current_layout_icon"]
side_screen_widgets = ["group_box", "window_name", "clock_date", "current_layout_icon"]

screens = [
    Screen(top=bar.Bar(widgets=wsb.build_widget_screen(main_screen_widgets, separators=True), size=26, opacity=0.8)),
    Screen(top=bar.Bar(widgets=wsb.build_widget_screen(side_screen_widgets, separators=True), size=26, opacity=0.8)),
    Screen(top=bar.Bar(widgets=wsb.build_widget_screen(side_screen_widgets, separators=True), size=26, opacity=0.8))
]

# Mouse Configuration
# ----------------------------------------------------------------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size())
]

# Miscellaneous Options
# ----------------------------------------------------------------------------------
# Default Options since I mostly don't know what they're doing
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"  # or smart


# Hooks
# ----------------------------------------------------------------------------------
# Add Hook to automatically start programs on qtile startup
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup_once
def assign_groups_to_screens():
    screen_arrangement = [2, 0, 1]

    for index, screen_number in enumerate(screen_arrangement):
        qtile.groups_map[groups[index].name].cmd_toscreen(screen_number)


'''
@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
'''
'''
@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]
'''

wmname = "LG3D"
