from PIL import Image, ImageOps


class EmbedQR:
    def __init__(self, background: str, qrcode: str):

        # file names
        self.fname_bg = background
        self.fname_qr = qrcode

        # images
        self.bg = Image.open(self.fname_bg)
        self.qr = Image.open(self.fname_qr)

        # qr code location
        self.offset = (0, 0)  # top left

    # ratio of qr code width to background width
    def resize_qr(self, ratio: int):
        print("qr resize ratio:", ratio)
        self.qr = ImageOps.scale(self.qr, 1 / ratio)

    # location of qr code on background
    def position_qr(self, offset):
        bg_w = self.bg.size[0]
        bg_h = self.bg.size[1]
        qr_w = self.qr.size[0]
        qr_h = self.qr.size[1]

        x_off = int((bg_w * offset[0]/100) - qr_w/2)
        if (x_off + qr_w) > bg_w:
            x_off = int(bg_w - qr_w)
        elif x_off < 0:
            x_off = 0

        y_off = int((bg_h * offset[1]/100) - qr_h/2)
        if (y_off + qr_h) > bg_h:
            y_off = int(bg_h - qr_h)
        elif y_off < 0:
            y_off = 0

        self.offset=(x_off, y_off)

        print("offset:", offset)

    # embed qr code onto background
    def embed(self):
        self.bg.paste(self.qr, self.offset)
        self.bg.save("out.png")
        temp = self.bg
        self.bg = Image.open(self.fname_bg)
        self.qr = Image.open(self.fname_qr)
        return temp
