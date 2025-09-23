from os.path import dirname, join
from ctypes import windll
from tkinter import Label, Button, Entry, Radiobutton, Frame
from tkinter.font import Font

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.Dark_Mode = True

        self.last_width = None
        self.last_height = None
        self.after_id = None

        self.Base_Dir = dirname(dirname(__file__))
        Fr_PRIVATE = 0x10
        font_path = join(self.Base_Dir, "Fonts", "Halo.ttf")
        windll.gdi32.AddFontResourceExW(font_path, Fr_PRIVATE, 0)

        self.Title_Font_Size = Font(root = root, family='Halo', size=30)
        self.Title_PadY_Size = 20
        self.SubTitle_Font_Size = Font(root = root, family='Halo', size=20)
        self.SubTitle_PadY_Size = 10
        self.Text_Font_Size = Font(root = root, family='Arial', size=10)
        self.Text_PadY_Size = 2

        self.scaled_sets = []

        root.bind("<Configure>", self.on_resize)

    def get_all_children(self, widget):
        children = widget.winfo_children()
        for child in children:
            children.extend(self.get_all_children(child))
        return children

    def update_paddings(self):
        for widget in self.get_all_children(self.root):
            try:
                info = widget.grid_info()
                if info:
                    font = widget.cget("font")
                    if font == str(self.Title_Font_Size):
                        pady = self.Title_PadY_Size
                    elif font == str(self.SubTitle_Font_Size):
                        pady = self.SubTitle_PadY_Size
                    elif font == str(self.Text_Font_Size):
                        pady = self.Text_PadY_Size
                    else:
                        continue
                    widget.grid_configure(pady=pady)
            except:
                pass

    def on_resize(self, event):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.after_id = self.root.after(100, self._do_resize, event.width, event.height)

    def _do_resize(self, width, height):
        self.after_id = None
        if self.last_width == width and self.last_height == height:
            return
        self.last_width = width
        self.last_height = height

        new_font_size = max(5, int(width / 100))
        new_pady_val = max(2, int(height / 200))

        self.Title_Font_Size.configure(size = int(new_font_size * 3))
        self.Title_PadY_Size = new_pady_val * 4

        self.SubTitle_Font_Size.configure(size = int(new_font_size * 1.5))
        self.SubTitle_PadY_Size = new_pady_val * 2

        self.Text_Font_Size.configure(size = max(8, int(new_font_size)))
        self.Text_PadY_Size = new_pady_val

        for title, subtitle, text, scale in self.scaled_sets:
            title.configure(size=int(self.Title_Font_Size['size'] * scale))
            subtitle.configure(size=int(self.SubTitle_Font_Size['size'] * scale))
            text.configure(size=int(self.Text_Font_Size['size'] * scale))

        self.update_paddings()

    def make_scaled_fonts(self, scale=0.75):
        title = self.Title_Font_Size.copy()
        subtitle = self.SubTitle_Font_Size.copy()
        text = self.Text_Font_Size.copy()

        self.scaled_sets.append((title, subtitle, text, scale))

        return title, subtitle, text

    def toggle_dm(self):
        self.Dark_Mode = not self.Dark_Mode

    def change_theme(self, widget):
        modes ={
            "Light": {"bg": '#FFFFFF', "fg": '#000000', "entry_bg": '#FFFFFF'},
            "Dark":{"bg": '#333333', "fg": '#FFFFFF', "entry_bg": '#333333'}}

        dm = "Dark" if self.Dark_Mode else "Light"
        theme = modes[dm]


        widget.config(bg=theme["bg"])
        for child in widget.winfo_children():
            if isinstance(child, (Label, Button, Radiobutton)):
                child.config(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(child, Entry):
                child.config(bg=theme["entry_bg"], fg=theme["fg"])
            if child.winfo_children():
                self.change_theme(child)

    def toggle_dark_mode(self):
        self.toggle_dm()
        self.change_theme(self.root)        