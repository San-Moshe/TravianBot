from tkinter import *
from functools import partial
from tkinter.font import Font

from pynput.mouse import Listener, Button as Btn

from Controller import Controller
from TravianActions import TravianActions
from TravianContract import TroopsRaidType, TroopsType


def main():
    TravianBotApp().mainloop()


class TravianBotApp(Tk):
    travian_controller = Controller()

    def __init__(self, *args, **kwargs):
        super().__init__()
        Tk.__init__(self, *args, **kwargs)

        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, travian_controller=self.travian_controller)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


class LoginPage(Frame):
    def __init__(self, parent, controller, travian_controller, **kw):
        Frame.__init__(self, parent)
        super().__init__(**kw)
        self.controller = controller
        self.travian_controller = travian_controller

        # username label and text entry box
        Label(self, text="Username").grid(row=0, column=0)
        username = StringVar()
        Entry(self, textvariable=username).grid(row=0, column=1)

        # password label and password entry box
        Label(self, text="Password").grid(row=1, column=0)
        password = StringVar()
        Entry(self, textvariable=password, show='*').grid(row=1, column=1)

        login_action = partial(self.login, username, password)

        # login button
        Button(self, text="Login",
               command=combine_funcs(login_action, lambda: controller.show_frame("MainPage"))).grid(row=4,
                                                                                                    column=0)

    def login(self, username, password):
        self.travian_controller.login(username.get(), password.get())


class MainPage(Frame):
    listener = None

    def __init__(self, parent, controller, travian_controller, **kw):
        Frame.__init__(self, parent)
        super().__init__(**kw)
        self.controller = controller
        self.travian_controller = travian_controller

        labelframe = LabelFrame(self, text="Record farms")
        switch_variable = StringVar(value="off")
        Radiobutton(labelframe, text="Off", variable=switch_variable,
                    indicatoron=False, value="off", width=8, command=self.unregister_click_listener).grid(
            row=0, column=1)
        Radiobutton(labelframe, text="On", variable=switch_variable,
                    indicatoron=False, value="on", width=8, command=self.register_click_listener).grid(
            row=0, column=2)

        labelframe.grid(row=2, columnspan=7, sticky='WE',
                        padx=5, pady=5, ipadx=5, ipady=5)

        Button(self, text="Raid", command=self.travian_controller.auto_mode)

        is_oasis = IntVar()
        is_farms = IntVar()
        is_stable = IntVar()
        is_barracks = IntVar()
        is_batch = IntVar()
        troops_type = TroopsType(1)
        auto_mode_label_frame = LabelFrame(self, text="Auto mode")
        C1 = Checkbutton(auto_mode_label_frame, text="Oasis", variable=is_oasis,
                         onvalue=1, offvalue=0, height=5,
                         width=20).grid(row=3, column=0)
        C2 = Checkbutton(auto_mode_label_frame, text="Farms", variable=is_farms,
                         onvalue=1, offvalue=0, height=5,
                         width=20).grid(row=3, column=1)
        C3 = Checkbutton(auto_mode_label_frame, text="Stable", variable=is_stable,
                         onvalue=1, offvalue=0, height=5,
                         width=20).grid(row=3, column=2)
        C4 = Checkbutton(auto_mode_label_frame, text="Barracks", variable=is_barracks,
                         onvalue=1, offvalue=0, height=5,
                         width=20).grid(row=3, column=3)
        C5 = Checkbutton(auto_mode_label_frame, text="Batch", variable=is_batch,
                         onvalue=1, offvalue=0, height=5,
                         width=20).grid(row=3, column=4)

        troops_type_label_frame = LabelFrame(auto_mode_label_frame, text="Troops Training Type")

        Radiobutton(troops_type_label_frame, text="Attacker", variable=troops_type,
                    indicatoron=False, value="off", width=8).grid(
            row=4, column=0)
        Radiobutton(troops_type_label_frame, text="Defender", variable=troops_type,
                    indicatoron=False, value="on", width=8).grid(
            row=4, column=1)

        Button(auto_mode_label_frame, text="Start Auto Mode", command=self.travian_controller.auto_mode).grid(row=5,
                                                                                                              column=5)
        troops_type_label_frame.grid(row=4, columnspan=7, sticky='WE',
                                     padx=5, pady=5, ipadx=5, ipady=5)
        auto_mode_label_frame.grid(row=3, columnspan=7, sticky='WE',
                                   padx=5, pady=5, ipadx=5, ipady=5)

        farm_list_label_frame = LabelFrame(self, text="Farm List")
        troops_raid_type_label_frame = LabelFrame(farm_list_label_frame, text="Troops Raid Type")

        troops_raid_type = TroopsRaidType(1)
        Radiobutton(troops_raid_type_label_frame, text="Infantry Attacker", variable=troops_raid_type,
                    value=TroopsRaidType.INFANTRY_ATTACKER,
                    width=16).grid(
            row=6, column=1)
        Radiobutton(troops_raid_type_label_frame, text="Infantry Defender", variable=troops_raid_type,
                    value=TroopsRaidType.INFANTRY_DEFENDER,
                    width=16).grid(
            row=7, column=1)
        Radiobutton(troops_raid_type_label_frame, text="Cavalry Attacker", variable=troops_raid_type,
                    value=TroopsRaidType.STABLE_ATTACKER,
                    width=16).grid(
            row=8, column=1)
        Radiobutton(troops_raid_type_label_frame, text="Cavalry Defender", variable=troops_raid_type,
                    value=TroopsRaidType.STABLE_DEFENDER,
                    width=16).grid(
            row=9, column=1)
        Label(farm_list_label_frame, text="Number Of Soldiers").grid(row=7, column=0)
        number_of_troops_entry = Entry(farm_list_label_frame, bd=5)
        number_of_troops_entry.grid(row=7, column=3)
        troops_raid_type_label_frame.grid(row=6, columnspan=7, sticky='WE',
                                          padx=5, pady=5, ipadx=5, ipady=5)
        farm_list_label_frame.grid(row=6, columnspan=7, sticky='WE',
                                   padx=5, pady=5, ipadx=5, ipady=5)

        farm_list_action = partial(self.on_add_farms_to_farm_list_click, troops_raid_type,
                                   number_of_troops_entry)
        Button(self, text="Farm account to farm list",
               command=farm_list_action).grid(row=6, column=5)

    def on_add_farms_to_farm_list_click(self, troops_type, number_of_troops_entry):
        self.travian_controller.add_farm_account_to_farm_list(troops_type, number_of_troops_entry.get())

    def on_click(self, x, y, button, pressed):
        if pressed and button == Btn.middle:
            self.travian_controller.add_oasis_to_custom_farm_list()
        elif button == Btn.right:
            return False

    def unregister_click_listener(self):
        if self.listener is not None:
            self.listener.stop()

    def register_click_listener(self):
        self.listener = Listener(
            on_click=self.on_click)
        self.listener.start()


if __name__ == '__main__':
    main()
