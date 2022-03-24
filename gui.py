from shutil import copyfile
from os.path import exists

from EmbedQR import *
from PIL import ImageTk
from tkinter import BOTH, StringVar, Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from tkinter.ttk import (
    Button,
    Label,
    Frame,
    Combobox,
    Style,
)


class Gui:
    def __init__(self):

        # main window
        self.root = Tk()
        self.root.geometry("650x375")
        # self.root.resizable(False, False)

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

        # image ratio
        self.cb_ratio = Combobox(
            self.bot_l,
            state="readonly",
            values=(
                "1",
                "2",
                "4",
                "8",
                "16",
                "32",
            ),
            width=8,
        )
        self.cb_ratio.set("4")

        # image position
        self.cb_offset = Combobox(
            self.bot_l,
            state="readonly",
            values=(
                "Center",
                "Top Left",
                "Top Right",
                "Bottom Left",
                "Bottom Right",
            ),
            width=8,
        )
        self.cb_offset.set("Top Left")

        # preview
        self.b_preview = Button(
            self.bot_l, text="preview", width=7, command=self._preview
        )

        # placeholder image
        img = Image.new(mode="RGB", size=(350, 225))
        self.img = ImageTk.PhotoImage(img)
        self.p_img = Label(self.bot_r, image=self.img, width=60, justify="left")

        # manage files
        self.v_bg.set("bg.png")
        self.v_qr.set("qr.png")
        self._update_embedder()
        self._pack_gui()

    # update the embedder with current state
    def _update_embedder(self):
        self.b_save.config(state="disabled")
        try:
            self.embedder = EmbedQR(self.v_bg.get(), self.v_qr.get())
            self.b_preview.config(state="enabled")
        except:
            self.embedder = None
            self.b_preview.config(state="disabled")

    # pack gui widgets
    def _pack_gui(self):

        # top l
        self.b_qr.pack()
        self.b_bg.pack()
        self.b_save.pack()

        # top r
        self.l_qr.pack()
        self.l_bg.pack(pady=6)
        self.l_save.pack()

        # bot l
        self.cb_ratio.pack()
        self.cb_offset.pack()
        self.b_preview.pack()

        # bot r
        self.p_img.pack(pady=15, fill=BOTH)

    # choose qr image path
    def _choose_qr(self):
        path = askopenfilename()
        if path != "":
            self.v_qr.set(path)
            self._update_embedder()

    # choose bg image path
    def _choose_bg(self):
        path = askopenfilename()
        if path != "":
            self.v_bg.set(path)
            self._update_embedder()

    # choose qr size
    def _change_ratio(self):
        print("change ratio:", self.cb_ratio.get())
        self.embedder.resize_qr(self.cb_ratio.get())

    # choose qr position
    def _change_offset(self):
        print("change offset:", self.cb_offset.get())
        self.embedder.position_qr(self.cb_offset.get())

    # preview qr on bg image
    def _preview(self):

        if self.embedder != None:

            if self.cb_ratio.get() != "":
                self.embedder.resize_qr(int(self.cb_ratio.get()))

            if self.cb_offset.get() != "":
                self.embedder.position_qr(self.cb_offset.get())

            img = self.embedder.embed()
            w = self.root.winfo_screenwidth() / 4
            r = w / img.width
            h = img.height * r
            img = img.resize((int(w), int(h)))
            img = ImageTk.PhotoImage(img)
            self.img = img
            self.p_img.config(image=self.img)

            print("embed complete:")
            print(self.cb_offset.get())
            print(self.cb_ratio.get())

            self.root.update_idletasks()
            # img.show()

            self.b_save.config(state="enabled")

        else:
            print("no images to embed")

    # copy temporary image file to save location
    def _save(self):
        path = asksaveasfilename()
        if path != "":
            self.v_save.set(path)

            if exists("out.png"):
                copyfile("out.png", self.v_save.get())
            else:
                print("no embedded img 'out.png' to save")
