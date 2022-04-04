from shutil import copyfile
from os.path import exists
from threading import Thread

from time import sleep


from EmbedQR import *
from PIL import ImageTk
from tkinter import BOTH, VERTICAL, HORIZONTAL, Tk, StringVar
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror
from tkinter.ttk import (
    Button,
    Label,
    Frame,
    Style,
    Scale,
)


class Gui:
    def __init__(self):

        # main window
        self.root = Tk()
        self.root.geometry("650x375")
        # self.root.resizable(False, False)

        # vars
        self.embedder = None
        self._x = -1
        self._y = -1
        self._r = -1

        # grid
        self.top_l = Frame(self.root, width=100, height=100)
        self.top_l.grid(row=0, column=0, padx=20, pady=10)

        self.top_r = Frame(self.root, width=350, height=100)
        self.top_r.grid(row=0, column=1, pady=10)

        self.bot_l = Frame(self.root, width=100, height=500)
        self.bot_l.grid(row=1, column=0, padx=20, pady=10)

        self.bot_r = Frame(self.root, width=350, height=500)
        self.bot_r.grid(row=1, column=1, pady=10)

        style = Style()
        style.map("TButton", foreground=[("disabled", "black")])

        # choose qr code
        self.v_qr = StringVar()
        self.b_qr = Button(self.top_l, text="QR", width=5, command=self._choose_qr)
        self.l_qr = Label(self.top_r, textvariable=self.v_qr, width=60, justify="left")

        # choose bg image
        self.v_bg = StringVar()
        self.b_bg = Button(self.top_l, text="BG", width=5, command=self._choose_bg)
        self.l_bg = Label(self.top_r, textvariable=self.v_bg, width=60, justify="left")

        # save new image
        self.v_save = StringVar()
        self.b_save = Button(self.top_l, text="save", width=5, command=self._save)
        self.l_save = Label(
            self.top_r, textvariable=self.v_save, width=60, justify="left"
        )

        # QR size ratio
        def ratio_callback(value):
            self.ratio_label.config(text=round(float(value)))
        self.ratio_label = Label(self.bot_l, text='1')
        self.ratio_slide = Scale(self.bot_l, from_=1, to=32, command=ratio_callback)
        self.ratio_slide.set('2')

        # QR x-y offsets
        self.offset_x_slide = Scale(self.bot_r, from_=0, to=100)
        self.offset_y_slide = Scale(self.bot_r, from_=0, to=100, orient=VERTICAL)

        # placeholder image
        img = Image.new(mode="RGB", size=(350, 225))
        self.img = ImageTk.PhotoImage(img)
        self.p_img = Label(self.bot_r, image=self.img, width=60, justify="left")

        # manage files
        self.v_bg.set("bg.png")
        self.v_qr.set("qr.png")
        self._update_embedder()
        self._pack_gui()

        # preview thread
        self.t_preview = Thread(target=self._preview)
        self.t_preview.setDaemon(True)
        self.t_preview.start()

    # create embedder
    def _update_embedder(self):
        try:
            self.embedder = EmbedQR(self.v_bg.get(), self.v_qr.get())
        except:
            self.embedder = None

    # pack gui widgets
    def _pack_gui(self):

        # top l
        self.b_qr.grid()
        self.b_bg.grid()
        self.b_save.grid()

        # top r
        self.l_qr.grid()
        self.l_bg.grid()
        self.l_save.grid()

        # bot l
        self.ratio_label.grid()
        self.ratio_slide.grid()

        # bot r
        self.p_img.grid(row=1, column=0)
        self.offset_x_slide.grid(row=0, column=0)
        self.offset_y_slide.grid(row=1, column=1)

    # choose qr image path
    def _choose_qr(self):
        path = askopenfilename()
        if path != "":
            self.v_qr.set(path)
            self._update_embedder()
        self._x = -1
        self._y = -1
        self._r = -1

    # choose bg image path
    def _choose_bg(self):
        path = askopenfilename()
        if path != "":
            self.v_bg.set(path)
            self._update_embedder()
        self._x = -1
        self._y = -1
        self._r = -1

    def _preview(self):

        # loop forever
        while True:

            try:

                # current slider values
                _x = int(self.offset_x_slide.get())
                _y = int(self.offset_y_slide.get())
                _r = int(self.ratio_slide.get())

                # ensure embedder is set up
                if self.embedder != None:

                    # if slider values have changed
                    if self._x != _x or self._y != _y or self._r != _r:

                        # update embedded image values
                        self._x = _x
                        self._y = _y
                        self._r = _r

                        # resize and reposition qr on background
                        self.embedder.resize_qr(int(self.ratio_slide.get()))
                        self.embedder.position_qr((self.offset_x_slide.get(), self.offset_y_slide.get()))

                        img = self.embedder.embed()
                        w = self.root.winfo_screenwidth()/4
                        r = w/img.width
                        h = img.height * r
                        img = img.resize((int(w), int(h)))
                        img = ImageTk.PhotoImage(img)
                        self.img = img
                        self.p_img.config(image=self.img)

                        # self.root.update_idletasks()
                        # img.show()


                    else:

                        sleep(0.5)
                        pass


                    if (self.b_save.state() != ("enabled",)):
                        self.b_save.config(state="enabled")
                    else:
                        print('already enabled')
                    
                else:
                    self.b_save.config(state="disabled")
                    sleep(1.0)
                    pass

            except Exception as e:
                print(e)

    # copy temporary image file to save location
    def _save(self):
        try:
            path = asksaveasfilename()
            if path != "":
                self.v_save.set(path)

                if exists("out.png"):
                    copyfile("out.png", self.v_save.get())
                else:
                    print("no embedded img 'out.png' to save")
        except Exception as e:
            print(e)
