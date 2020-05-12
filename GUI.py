from tkinter import *
from functools import partial
from tkinter.font import Font

from pynput.mouse import Listener, Button as Btn

from TravianLoginAction import TravianUtils


def main():
    TravianBotApp().mainloop()


class TravianBotApp(Tk):
    travianUtils = TravianUtils()

    def __init__(self, *args, **kwargs):
        super().__init__()
        Tk.__init__(self, *args, **kwargs)

        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        # container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, travian_utils=self.travianUtils)
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
    def __init__(self, parent, controller, travian_utils, **kw):
        Frame.__init__(self, parent)
        super().__init__(**kw)
        self.controller = controller
        self.travian_utils = travian_utils

        # username label and text entry box
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
        self.travian_utils.login(username.get(), password.get())


class MainPage(Frame):
    listener = None

    def __init__(self, parent, controller, travian_utils, **kw):
        Frame.__init__(self, parent)
        super().__init__(**kw)
        self.controller = controller
        self.travian_utils = travian_utils

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

    def on_click(self, x, y, button, pressed):
        if pressed and button == Btn.middle:
            self.travian_utils.add_oasis_to_custom_farm_list()
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
