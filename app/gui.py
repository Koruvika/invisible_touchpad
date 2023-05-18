import tkinter
import tkinter.messagebox
import customtkinter
import sys
import win32api
import socket
from pynput.mouse import Button, Controller
import threading
import screen_brightness_control as sbc


# customtkinter.ScalingTracker.set_user_scaling(0.5)
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.init_server()
        self.init_parameter()
        self.init_frame()
        self.init_left()
        self.init_right()
        self.init_bottom()

    def init_parameter(self):
        self.mouse = Controller()

        self.dpi = 50
        self.scroll_speed = 50
        self.cursor = "Arrow"
        self.click = "Left"
        self.scroll_type = "Scroll"

    def init_frame(self):

        self.title("Air Mouse Config")
        self.geometry("780x520")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)

        # ============ create 3 frames ============
        self.frame_left = customtkinter.CTkFrame(master=self, width=100, corner_radius=10)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=(7, 3), pady=(7, 0))

        self.frame_right = customtkinter.CTkFrame(master=self, width=100, corner_radius=10)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=(3, 7), pady=(7, 0))

        self.frame_bottom = customtkinter.CTkFrame(master=self, height=100, corner_radius=10)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(7, 7), pady=(0, 7))

    def init_left(self):
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)
        self.frame_left.grid_columnconfigure(0, weight=1, pad=0)
        self.frame_left.grid_columnconfigure(1, weight=5, pad=0)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="CONFIG",
                                              text_color=("gray10", "gray100"),
                                              font=("MS Sans Serif", 24))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=10, columnspan=2, sticky="ew")

        self.label_dpi = customtkinter.CTkLabel(
            master=self.frame_left,
            text="DPI ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_dpi.grid(row=1, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.slider_dpi = customtkinter.CTkSlider(
            width=100,
            master=self.frame_left,
            from_=0,
            to=100,
            command=self.dpi_slider_event,
        )
        self.slider_dpi.grid(row=2, column=0, columnspan=2, pady=(0, 5), padx=(20, 20), sticky="ew")

        self.label_speed_scroll = customtkinter.CTkLabel(
            master=self.frame_left,
            text="Scroll Speed ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_speed_scroll.grid(row=3, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.slider_scroll = customtkinter.CTkSlider(
            width=100,
            master=self.frame_left,
            from_=0,
            to=100,
            command=self.scroll_speed_slider_event,
        )
        self.slider_scroll.grid(row=4, column=0, columnspan=2, pady=(0, 5), padx=(20, 20), sticky="ew")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

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

        self.label_cursor = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Customized Cursor ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_cursor.grid(row=1, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.cbb_cursor = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=["Arrow", "Heart", "Mouse"],
            command=self.cbb_cursor_callback
        )
        self.cbb_cursor.grid(row=2, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.label_click = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Customized Click ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_click.grid(row=3, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.cbb_click = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=["Left Click", "Right Click"],
            command=self.cbb_click_callback
        )
        self.cbb_click.grid(row=4, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.label_scroll = customtkinter.CTkLabel(
            master=self.frame_right,
            text="Customized Scroll ",
            justify="left",
            anchor="w",
            text_color=("gray30", "gray75"),
            font=("MS Sans Serif", 14))  # font name and size in px
        self.label_scroll.grid(row=5, column=0, pady=0, padx=(25, 25), sticky="ew")

        self.cbb_scroll = customtkinter.CTkComboBox(
            master=self.frame_right,
            values=["Volume", "Light", "Scroll"],
            command=self.cbb_scroll_callback
        )
        self.cbb_scroll.grid(row=6, column=0, pady=0, padx=(25, 25), sticky="ew")

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
            values=["Arrow", "Heart", "Mouse"],
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
            values=["Volume", "Light", "Scroll"],
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
        self.cursor = choice

    def cbb_click_callback(self, choice):
        self.click = choice

    def cbb_scroll_callback(self, choice):
        self.scroll_type = choice

    def dpi_slider_event(self, value):
        self.dpi = value

    def scroll_speed_slider_event(self, value):
        self.scroll_speed = value

    def connect_button_event(self):
        try:
            self.udp_server_socket.bind((self.local_ip, self.local_port))
        except OSError as e:
            print(f"Just {e}, it's not important here!")

        self.recv_thread = threading.Thread(target=self.recv)
        self.recv_thread.start()

    def recv(self):
        while True:
            byteAddressPair = self.udp_server_socket.recvfrom(self.bufferSize)
            message = byteAddressPair[0].decode('utf-8')
            address = byteAddressPair[1]
            arr = message.strip().split(' ')

            if len(arr) != 3:
                continue
            else:
                action, dx, dy = arr
            if action == 'move':
                self.mouse.move(int(float(dx) * self.dpi), int(float(dy) * self.dpi))
            elif action == 'click':
                self.mouse.click(Button.left, 1)
            elif action == 'scroll_up':
                self.mouse.scroll(0, -10)
            elif action == 'scroll_down':
                self.mouse.scroll(0, 10)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
