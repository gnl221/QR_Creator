#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import platform
import qrcode
import sys


class QRCodeApp:
    def __init__(self, window, qr_text, second_line_text, text_wanted):
        self.photo = None
        self.window = window
        self.window.title("Greg's QR Label Generator")

        self.label = tk.Label(window, text="Enter text for QR Code.")
        self.label.grid(row=0, column=0, columnspan=2)

        self.entry = tk.Entry(window)
        self.entry.insert(0, qr_text)
        self.entry.grid(row=1, column=0, columnspan=2)

        self.label2 = tk.Label(window, text="Enter text for second line if needed.")
        self.label2.grid(row=2, column=0, columnspan=2)

        self.entry2 = tk.Entry(window)
        self.entry2.insert(0, second_line_text)
        self.entry2.grid(row=3, column=0, columnspan=2)

        self.show_text_var = tk.IntVar(value=1)
        self.show_text_check = tk.Checkbutton(window, text="Show text next to QR Code", variable=self.show_text_var)
        self.show_text_check.grid(row=4, column=0)

        self.word_wrap_var = tk.IntVar(value=1)
        self.word_wrap_check = tk.Checkbutton(window, text="Enable word wrap for QR field", variable=self.word_wrap_var)
        self.word_wrap_check.grid(row=4, column=1)
        self.word_wrap_check.grid_forget()

        self.create_button = tk.Button(window, text="Create", command=self.create_qr_code)
        self.create_button.grid(row=5, column=0)

        self.download_button = tk.Button(window, text="Download", command=self.download_qr_code)
        self.download_button.grid(row=5, column=1)

        self.image_label = tk.Label(window)
        self.image_label.grid(row=6, column=0)

        self.text_label = tk.Label(window, font=("Arial", 2), bg="white")
        self.text_label.grid(row=7, column=0)
        self.text_label.grid_forget()

        self.qr_code = None

        if qr_text:
            if sys.argv[3] == "False":
                self.show_text_var = tk.IntVar(value=0)
            self.create_qr_code()
            self.download_qr_code()
            self.window.destroy()

    def create_qr_code(self):
        fnt = None
        text = self.entry.get()
        if not text:
            messagebox.showerror("Error", "The text field is empty.")
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(text)
        qr.make(fit=True)

        qr_code_img = qr.make_image(fill='black', back_color='white')
        qr_code_img = qr_code_img.convert("RGB")

        second_text = self.entry2.get()

        if self.show_text_var.get() == 1:
            if self.word_wrap_var.get() == 1:
                display_text = self.word_wrap(text) + ("\n\n" + second_text)
            else:
                display_text = text + "\n\n" + second_text

            self.text_label.config(text=display_text)

            text_img = Image.new('RGB', (qr_code_img.width * 2, qr_code_img.height), color=(255, 255, 255))
            d = ImageDraw.Draw(text_img)
            current_os = platform.system()

            match current_os:
                case "Windows":
                    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\Arial.ttf', 35)
                case "Darwin":
                    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 35)
                case "Linux":
                    fnt = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Regular.ttf', 35)
                case "":
                    try:
                        fnt = ImageFont.truetype('Arial.ttf', 30)
                    except OSError:
                        messagebox.showerror("Error", "Please install the font Arial.ttf")

            d.text((2, 15), display_text, font=fnt, fill=(0, 0, 0))

            self.qr_code = Image.new('RGB', (qr_code_img.width * 3, qr_code_img.height))
            self.qr_code.paste(qr_code_img, (0, 0))
            self.qr_code.paste(text_img, (qr_code_img.width, 0))
        else:
            self.qr_code = qr_code_img

        self.photo = ImageTk.PhotoImage(self.qr_code)
        self.image_label.config(image=self.photo)

    def download_qr_code(self):
        if self.qr_code is None:
            messagebox.showerror("Error", "No QR code has been created yet.")
            return

        text = self.entry.get()
        self.qr_code.save(os.path.join(os.path.expanduser("~"), "Downloads", f"{text}.png"))
        if not qr_code_text:
            messagebox.showinfo("Success", "QR code has been saved to the Downloads folder.")

    @staticmethod
    def word_wrap(text, width=24):
        return '\n'.join([text[i:i+width] for i in range(0, len(text), width)])


if __name__ == "__main__":
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = screen_width // 2
    window_height = screen_height // 2

    root.geometry(f"{window_width}x{window_height}")

    qr_code_text = sys.argv[1] if len(sys.argv) > 1 else ""
    additional_text = sys.argv[2] if len(sys.argv) > 2 else ""
    show_text = sys.argv[3] if len(sys.argv) > 3 else ""

    app = QRCodeApp(root, qr_code_text, additional_text, show_text)
    root.mainloop()
