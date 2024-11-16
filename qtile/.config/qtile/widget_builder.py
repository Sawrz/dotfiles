import os
from libqtile import bar, widget
from libqtile.widget import Spacer
from arcobattery import BatteryIcon


class AppletCreator:
    def __init__(self, theme_colors):
        self._theme_colors = theme_colors

    def group_box(self):
        return [
            widget.GroupBox(
                font="FontAwesome",
                fontsize=16,
                margin_y=0,
                margin_x=0,
                padding_y=6,
                padding_x=5,
                disable_drag=True,
                rounded=False,
                foreground=self._theme_colors["foreground"],
                background=self._theme_colors["background"],
                active=self._theme_colors["accent_light"],
                inactive=self._theme_colors["white"],
                borderwidth=2,
                highlight_method="line",
                highlight_color=self._theme_colors["background"],
                this_current_screen_border=self._theme_colors["accent_light"],
                other_current_screen_border=self._theme_colors["background"],
                this_screen_border=self._theme_colors["accent_dark"],
                other_screen_border=self._theme_colors["background"],
                urgent_alert_method="line",
                urgent_border=self._theme_colors["red"],
                urgent_text=self._theme_colors["red"],
            )
        ]

    def separator(self):
        return [
            widget.Sep(
                linewidth=1,
                padding=10,
                foreground=self._theme_colors["foreground"],
                background=self._theme_colors["background"],
            )
        ]

    def current_layout(self):
        return [
            widget.CurrentLayout(
                font="Noto Sans Bold",
                foreground=self._theme_colors["white"],
                background=self._theme_colors["background"],
            )
        ]

    def current_layout_icon(self):
        return [widget.CurrentLayoutIcon(fontsize=16, background=self._theme_colors["background"])]

    def window_name(self):
        return [
            widget.WindowName(
                font="Noto Sans",
                fontsize=12,
                foreground=self._theme_colors["white"],
                background=self._theme_colors["background"],
            )
        ]

    def network(self):
        return [
            widget.Net(
                font="Noto Sans",
                fontsize=12,
                interface="eno2",
                foreground=self._theme_colors["foreground"],
                background=self._theme_colors["background"],
                padding=0,
            )
        ]

    def network_graph(self):
        return [
            widget.NetGraph(
                font="Noto Sans",
                fontsize=12,
                bandwidth="down",
                interface="auto",
                fill_color=self._theme_colors["accent_light"],
                foreground=self._theme_colors["foreground"],
                background=self._theme_colors["background"],
                graph_color=self._theme_colors["accent_light"],
                border_color=self._theme_colors["foreground"],
                padding=0,
                border_width=1,
                line_width=1,
            )
        ]

    def thermal_sensor(self):
        # do not activate in Virtualbox - will break qtile

        return [
            widget.ThermalSensor(foreground=self._theme_colors["white"],
                                 foreground_alert=self._theme_colors["red"],
                                 background=self._theme_colors["background"],
                                 metric=True,
                                 padding=3,
                                 threshold=80)
        ]

    def arcobattery(self):
        home = os.path.expanduser('~')
        return [
            BatteryIcon(
                padding=0,
                scale=0.7,
                y_poss=2,
                theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
                update_interval=5,
                background=self._theme_colors["background"],
            )
        ]

    def battery(self):
        return [
            widget.Battery(
                font="Noto Sans",
                update_interval=10,
                fontsize=12,
                foreground=self._theme_colors["white"],
                background=self._theme_colors["background"],
            )
        ]

    def cpu_graph(self):

        return [
            widget.TextBox(font="FontAwesome",
                           text="  ",
                           foreground=self._theme_colors["red"],
                           background=self._theme_colors["background"],
                           padding=0,
                           fontsize=16),
            widget.CPUGraph(border_color=self._theme_colors["foreground"],
                            fill_color=self._theme_colors["accent_light"],
                            graph_color=self._theme_colors["accent_light"],
                            background=self._theme_colors["background"],
                            border_width=1,
                            line_width=1,
                            core="all",
                            type="box")
        ]

    def memory(self):
        return [
            widget.TextBox(font="FontAwesome",
                           text="  ",
                           foreground=self._theme_colors["blue"],
                           background=self._theme_colors["background"],
                           padding=0,
                           fontsize=16),
            widget.Memory(
                font="Noto Sans",
                format='{MemUsed}M/{MemTotal}M',
                update_interval=1,
                fontsize=12,
                foreground=self._theme_colors["white"],
                background=self._theme_colors["background"],
            )
        ]

    def clock(self, show_time=True, show_date=True, show_icon=True, clock_font='Noto Sans'):
        clock_widgets = []

        if show_icon:
            if not show_date:
                icon = "  "
            else:
                icon = "  "

            clock_widgets.append(
                widget.TextBox(font="FontAwesome",
                               text=icon,
                               foreground=self._theme_colors["white"],
                               background=self._theme_colors["background"],
                               padding=0,
                               fontsize=16))

        if show_date and show_time:
            clock_format = "%Y-%m-%d %H:%M"
        elif show_date:
            clock_format = "%Y-%m-%d"
        elif show_time:
            clock_format = "%H:%M"
        else:
            return []

        clock_widgets.append(
            widget.Clock(foreground=self._theme_colors["white"],
                         background=self._theme_colors["background"],
                         font=clock_font,
                         fontsize=14,
                         format=clock_format))

        return clock_widgets

    def system_tray(self):
        return [widget.Systray(background=self._theme_colors["background"], icon_size=20, padding=4)]


class WidgetScreenBuilder:
    def __init__(self, theme_colors):
        ac = AppletCreator(theme_colors=theme_colors)

        self._widgets = {
            "group_box": ac.group_box,
            "current_layout": ac.current_layout,
            "current_layout_icon": ac.current_layout_icon,
            "window_name": ac.window_name,
            "network": ac.network,
            "network_graph": ac.network_graph,
            "thermal_sensor": ac.thermal_sensor,
            "arcobattery": ac.arcobattery,
            "battery": ac.battery,
            "cpu_graph": ac.cpu_graph,
            "memory": ac.memory,
            "clock": ac.clock,
            "clock_time": lambda: ac.clock(show_icon=True, show_date=False),
            "clock_date": lambda: ac.clock(show_icon=True, show_time=False),
            "system_tray": ac.system_tray,
        }

        self._applet_creator = ac

    def build_widget_screen(self, widgets, separators=True):
        last_widget_index = len(widgets) - 1
        widget_screen = []

        for i, widget_name in enumerate(widgets):
            widget_screen.extend(self._widgets[widget_name]())

            if separators and not widget_name == "window_name" and i < last_widget_index:
                widget_screen.extend(self._applet_creator.separator())

        return widget_screen
