from tkinter import ttk
import bitmap
from tkinter import Tk, mainloop, Canvas, PhotoImage, filedialog


def rgb2hex(r, g, b):
    """
    Convert an r,g,b colour to a hex code
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


class Root(Tk):
    """
    This is the root object, which inherits from TK

    The benefit of inheritance is we can write:
    self.button instead of self.root.button
    """

    def __init__(self):
        super(Root, self).__init__()
        self.title("BMP compression analyzer")
        self.minsize(640, 400)
        self.row = 3

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.button()

    def get_row(self):
        self.row += 1
        return self.row

    def button(self):
        self.button = ttk.Button(
            self.labelFrame, text="Browse A File", command=self.file_dialog
        )
        self.button.grid(column=1, row=1)

    def file_dialog(self):
        """
        Opens a file dialog and has the user chose a file

        This then sets some labels afterwards
        """

        self.filename = filedialog.askopenfilename(
            initialdir="./", title="Select A File",
        )
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        if self.filename:
            self.get_bmp_info(self.filename)

    def get_bmp_info(self, filename):
        """
        Print some information about the bmp file

        Shows on the UI bmp
        """
        with open(filename, "rb") as bmp_file:
            bmp_data = bitmap.Image(bmp_file.read())

            self.show_image(
                bmp_data.getBitmapWidth(),
                bmp_data.getBitmapHeight(),
                bmp_data.getPixels(),
                self.get_row(),
                0,
            )

    def show_image(self, width, height, pixels, row, col):
        """
        Add an image to the gui
        """
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.grid(column=col, row=row)

        img = PhotoImage(width=width, height=height)
        self.canvas.create_image((width / 2, height / 2), image=img, state="normal")
        self.canvas.image = img

        for y_index, y in enumerate(pixels):
            for x_index, x in enumerate(y):
                blue, green, red = x
                hex_code = rgb2hex(r=red, g=green, b=blue)
                img.put(hex_code, (x_index, height - y_index))


if __name__ == "__main__":
    root = Root()
    root.mainloop()
