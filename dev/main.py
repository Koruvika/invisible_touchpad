import ctypes
import socket
import sys
import threading
from tkinter import messagebox

import comtypes
import customtkinter
import screen_brightness_control as sbc
import win32con
import win32gui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.mouse import Button, Controller

sys.path.insert(0, ".")
from bluetooth import bluetooth_scan
from get_volume import get_volume

# customtkinter.ScalingTracker.set_user_scaling(0.5)
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.init_server()
        self.init_parameter()
        self.init_frame()
        self.init_right()
        self.init_bottom()

    def init_parameter(self):
        self.mouse = Controller()

        self.default_dpi = 17
        self.default_scroll_speed = 15

        self.dpi = self.default_dpi
        self.scroll_speed = self.default_scroll_speed
        self.cursor = "Arrow"
        self.click = "Left Click"
        self.scroll_type = "Scroll"

        self.cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        self.save_system_cursor = ctypes.windll.user32.CopyImage(self.cursor, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)

    def init_frame(self):

        self.title("Air Mouse Config")
        self.geometry("600x520")

        self.grid_columnconfigure(0, weight=5)
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)

        # ============ create 2 frames ============
        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=10)
        self.frame_right.grid(row=0, column=0, sticky="nswe", padx=(10, 10), pady=(7, 0))

        self.frame_bottom = customtkinter.CTkFrame(master=self, height=100, corner_radius=10)
        self.frame_bottom.grid(row=1, column=0, sticky="ew", padx=(10, 10), pady=(0, 7))

    def init_right(self):
        self.frame_right.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_right.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_right.grid_rowconfigure(9, weight=1)
        self.frame_right.grid_rowconfigure(11, minsize=10)
        self.frame_right.grid_columnconfigure(0, weight=1, pad=0)
        self.frame_right.grid_columnconfigure(1, weight=1, pad=0)

        self.label_2 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="ADVANCED CONFIG",
                                              text_color=("gray10", "gray100"),
                                              font=("MS Sans Serif", 24))  # font name and size in px
        self.label_2.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="ew")

        self.label_dpi = customtkinter.CTkLabel(
            master=self.frame_right,
            text=f"DPI: {self.dpi}",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_dpi.grid(row=1, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.slider_dpi = customtkinter.CTkSlider(
            width=100,
            master=self.frame_right,
            from_=0,
            to=100,
            command=self.dpi_slider_event,
        )
        self.slider_dpi.grid(row=2, column=0, pady=(0, 5), padx=(25, 25), sticky="ew")
        self.slider_dpi.set(self.default_dpi)

        self.label_speed_scroll = customtkinter.CTkLabel(
            master=self.frame_right,
            text=f"Scroll Speed: {self.scroll_speed}",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_speed_scroll.grid(row=3, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.slider_scroll = customtkinter.CTkSlider(
            width=100,
            master=self.frame_right,
            from_=0,
            to=100,
            command=self.scroll_speed_slider_event,
        )
        self.slider_scroll.grid(row=4, column=0, pady=(0, 5), padx=(25, 25), sticky="ew")
        self.slider_scroll.set(self.default_scroll_speed)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="Dark Mode",
                                                variable=customtkinter.IntVar(value=1),
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        self.label_cursor_2 = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Customized Cursor ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_cursor_2.grid(row=1, column=1, pady=0, padx=(25, 25), sticky="ew")

        self.cbb_cursor_2 = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=["Arrow", "Heart", "Star", "Donut"],
            command=self.cbb_cursor_callback
        )
        self.cbb_cursor_2.grid(row=2, column=1, pady=0, padx=(25, 25), sticky="ew")

        self.label_click_2 = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Customized Click ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_click_2.grid(row=3, column=1, pady=0, padx=(25, 25), sticky="ew")

        self.cbb_click_2 = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=["Left Click", "Right Click"],
            command=self.cbb_click_callback
        )
        self.cbb_click_2.grid(row=4, column=1, pady=0, padx=(25, 25), sticky="ew")

        self.label_scroll_2 = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Customized Scroll ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_scroll_2.grid(row=5, column=1, pady=0, padx=(25, 25), sticky="ew")

        self.cbb_scroll_2 = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=["Scroll", "Volume", "Light"],
            command=self.cbb_scroll_callback
        )
        self.cbb_scroll_2.grid(row=6, column=1, pady=0, padx=(25, 25), sticky="ew")

    def init_bottom(self):
        self.frame_bottom.grid_columnconfigure(0, weight=10)
        self.frame_bottom.grid_columnconfigure(1, weight=1)

        self.label_ip = customtkinter.CTkLabel(
            master=self.frame_bottom,
            text=f"IP Address: {self.local_ip}",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 16))  # font name and size in px
        self.label_ip.grid(row=0, column=0, pady=(10, 0), padx=(25, 25), sticky="ew")

        self.label_port = customtkinter.CTkLabel(
            master=self.frame_bottom,
            text=f"Host: {self.local_port}",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 16))  # font name and size in px
        self.label_port.grid(row=1, column=0, pady=(0, 10), padx=(25, 25), sticky="ew")

        self.button_connect = customtkinter.CTkButton(
            master=self.frame_bottom,
            text="Connect",
            command=self.connect_button_event
        )
        self.button_connect.grid(row=0, column=1, pady=0, rowspan=2, padx=(25, 25), sticky="ew")

    def init_server(self):
        host_name = socket.gethostname()
        self.local_ip = socket.gethostbyname(host_name)
        self.local_port = 20001

        self.bufferSize = 1024
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def cbb_cursor_callback(self, choice):
        if choice == "Heart":
            cursor_file = "cache/heart.cur"
        elif choice == "Star":
            cursor_file = "cache/star.cur"
        elif choice == "Donut":
            cursor_file = "cache/donut-_1_.cur"
        else:
            self.restore_cursor()
            return
        cursor = ctypes.windll.user32.LoadImageW(None, cursor_file, win32con.IMAGE_CURSOR, 0, 0,
                                                 win32con.LR_LOADFROMFILE)
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)
        ctypes.windll.user32.DestroyCursor(cursor)


    def cbb_click_callback(self, choice):
        self.click = choice

    def cbb_scroll_callback(self, choice):
        self.scroll_type = choice

    def dpi_slider_event(self, value):
        self.dpi = int(value)
        self.label_dpi.configure(text=f"DPI: {self.dpi}")

    def scroll_speed_slider_event(self, value):
        self.scroll_speed = int(value)
        self.label_speed_scroll.configure(text=f"Scroll Speed: {self.scroll_speed}")

    def connect_button_event(self):
        try:
            self.udp_server_socket.bind((self.local_ip, self.local_port))
            # print("Connect Success")
            self.recv_thread = threading.Thread(target=self.recv)
            self.recv_thread.start()
        except OSError as e:
            print(f"Just {e}, it's not important here!")

    def recv(self):
        while True:
            byteAddressPair = self.udp_server_socket.recvfrom(self.bufferSize)
            # print(byteAddressPair)
            message = byteAddressPair[0].decode('utf-8')
            address = byteAddressPair[1]
            arr = message.strip().split(' ')
            print(arr)
            if len(arr) != 3:
                continue
            else:
                action, dx, dy = arr
            if action == 'move':
                self.mouse.move(int(float(dx) * self.dpi), int(float(dy) * self.dpi))
            elif action == 'click':
                if self.click == "Left Click":
                    self.mouse.click(Button.left, 1)
                elif self.click == "Right Click":
                    self.mouse.click(Button.right, 1)
            elif action == 'scroll_up':
                if self.scroll_type == "Scroll":
                    self.mouse.scroll(0, -10)
                elif self.scroll_type == "Volume":
                    current_volume = self.volume.GetMasterVolumeLevelScalar()
                    new_volume = current_volume - self.scroll_speed/100
                    new_volume = new_volume if new_volume < 1 else 1
                    self.volume.SetMasterVolumeLevelScalar(new_volume, None)
                elif self.scroll_type == "Light":
                    sbc.set_brightness(sbc.get_brightness()[0] - self.scroll_speed)
            elif action == 'scroll_down':
                if self.scroll_type == "Scroll":
                    self.mouse.scroll(0, 10)
                elif self.scroll_type == "Volume":
                    current_volume = self.volume.GetMasterVolumeLevelScalar()
                    new_volume = current_volume + self.scroll_speed/100
                    new_volume = new_volume if 0 < new_volume else 0
                    self.volume.SetMasterVolumeLevelScalar(new_volume, None)
                elif self.scroll_type == "Light":
                    sbc.set_brightness(sbc.get_brightness()[0] + self.scroll_speed)

    def restore_cursor(self):
        print("restore_cursor")
        ctypes.windll.user32.SetSystemCursor(self.save_system_cursor, 32512)
        ctypes.windll.user32.DestroyCursor(self.save_system_cursor)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.restore_cursor()
            self.destroy()

    def start(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

app = App()
app.start()

# if __name__ == "__main__":

    # cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR,
    #                             0, 0, win32con.LR_SHARED)
    # save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR,
    #                                                     0, 0, win32con.LR_COPYFROMRESOURCE)
    #
    #
    # def restore_cursor():
    #     print("restore_cursor")
    #     ctypes.windll.user32.SetSystemCursor(save_system_cursor, 32512)
    #     ctypes.windll.user32.DestroyCursor(save_system_cursor)
    #
    #
    # atexit.register(restore_cursor)
    #
    # cursor_file = "cache/heart.cur"
    # cursor = ctypes.windll.user32.LoadImageW(None, cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    #
    # ctypes.windll.user32.SetSystemCursor(cursor, 32512)
    # ctypes.windll.user32.DestroyCursor(cursor)
    # time.sleep(3)
    # exit
