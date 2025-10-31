from tkinter import Label, Button, Entry, Radiobutton, Scale, Toplevel, Tk
from tkinter.ttk import Combobox
from tkextrafont import Font
import Json_Handling as JH
import Json_Maps as JM

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.last_width = None
        self.last_height = None
        self.after_id = None

        self.Title_Font_Size = Font(family = 'Halo', size = 30)
        self.Title_PadX_Size = 10
        self.Title_PadY_Size = 20
        self.SubTitle_Font_Size = Font(family = 'Halo', size = 20)
        self.SubTitle_PadY_Size = 10
        self.SubTitle_PadX_Size = 5
        self.Text_Font_Size = Font(family = 'Arial', size = 10)
        self.Text_WrapLength = 100
        self.Text_PadX_Size = 2
        self.Text_PadY_Size = 2
        self.ToolTip_Font_Size = Font(family = 'Arial', size = 8)
        self.scaled_sets = []
        root.bind("<Configure>", self.on_resize)

        self.modes ={
            "Light": {"bg": '#FFFFFF', "fg": '#000000', "entry_bg": '#FFFFFF'},
            "Dark":{"bg": '#333333', "fg": '#FFFFFF', "entry_bg": '#333333'}}
        self.green = "#879250"


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
        new_padx_val = max(2, int(width / 200))
        new_wraplength = max(100, int(width / 5))
        new_pady_val = max(2, int(height / 200))


        self.Title_Font_Size.configure(size = int(new_font_size * 3))
        self.Title_PadX_Size = new_padx_val * 4
        self.Title_PadY_Size = new_pady_val * 4

        self.SubTitle_Font_Size.configure(size = int(new_font_size * 1.5))
        self.SubTitle_PadX_Size = new_padx_val * 2
        self.SubTitle_PadY_Size = new_pady_val * 2

        self.Text_Font_Size.configure(size = max(10, int(new_font_size)))
        self.Text_PadX_Size = new_padx_val
        self.Text_PadY_Size = new_pady_val
        self.Text_WrapLength = new_wraplength

        self.ToolTip_Font_Size.configure(size = max(8, int(new_font_size * 0.5)))

        for title, subtitle, text, scale in self.scaled_sets:
            title.configure(size=int(self.Title_Font_Size['size'] * scale))
            subtitle.configure(size=int(self.SubTitle_Font_Size['size'] * scale))
            text.configure(size=int(self.Text_Font_Size['size'] * scale))


        def update_paddings():
            def get_all_children(widget):
                children = widget.winfo_children()
                for child in children:
                    children.extend(get_all_children(child))
                return children

            for widget in get_all_children(self.root):
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
        update_paddings()

    def make_scaled_fonts(self, scale=0.75):
        title = self.Title_Font_Size.copy()
        subtitle = self.SubTitle_Font_Size.copy()
        text = self.Text_Font_Size.copy()

        self.scaled_sets.append((title, subtitle, text, scale))

        return title, subtitle, text

    def change_theme(self, window):
        theme = self.modes["Dark" if JH.get_json_val("Preferences.json", JM.Prefernce_map, "darkmode") else "Light"]

        def theme_recursion(widget, theme):
            widget.config(bg = theme["bg"])
            for child in widget.winfo_children():
                if isinstance(child, (Label, Radiobutton, Scale)):
                    child.config(bg = theme["bg"], fg = theme["fg"])
                elif isinstance(child, (Entry, Button)) and not isinstance(child, Combobox):
                    if isinstance(child, Entry) and (child.get().strip() != 0):
                        child.config(bg = theme["entry_bg"], fg = theme["fg"])
                    if child.cget("bg") == "#879250":
                        child.config(fg = theme["fg"])
                    else:
                        child.config(bg = theme["entry_bg"], fg = theme["fg"])
                elif isinstance(child, (Tk, Toplevel)):
                    child.config(bg = theme["bg"])
                if child.winfo_children():
                    theme_recursion(child, theme)
        theme_recursion(window, theme)

    def global_theme_change(self, root, toggle = False):
        if toggle:
            data = JH.read("Preferences.json")
            data["Settings"]["DarkMode"] = not data["Settings"]["DarkMode"]
            JH.save("Preferences.json", data)


        def get_all_toplevels(root):
            toplevels = [root]
            children = root.tk.call('winfo', 'children', '.')
            for child_path in children:
                if "toplevel" in child_path.lower():
                    toplevels.append(root.nametowidget(child_path))
            return toplevels


        for window in get_all_toplevels(root):
            self.change_theme(window) 
 
    def bool_update_label(self,file_name,label_map):
        data = JH.read(file_name)

        for key_list, label in label_map.items():
            keys = key_list.split(",")
            cur = data
            for key in keys[:-1]:
                cur = cur[key]
                    
            last_key = keys[-1]
            value = cur[last_key]
                    
            label.config(text="Active" if value else "Not Active")

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = 0
        self.y = 0
        self.theme = ThemeManager(widget)


    def showtip(self, text):
        self.text = text

        if self.tipwindow or not self.text or not JH.get_json_val("Preferences.json", JM.Prefernce_map, "tooltip"):
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 57
        y += cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text = self.text, justify = "left", relief = "solid", borderwidth = 1, font = self.theme.ToolTip_Font_Size)
        label.pack(ipadx = 1)
      
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def toggle():
        data = JH.read("Preferences.json")
        data["Settings"]["ToolTips"] = not data["Settings"]["ToolTips"]
        JH.save("Preferences.json", data)

def create_tooltip(widget, text):
    tooltip = ToolTip(widget)
    def enter(event):
        tooltip.showtip(text)

    def leave(event):
        tooltip.hidetip()
    
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)