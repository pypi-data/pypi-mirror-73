from tkinter import ttk, TclError

from hoverset.ui.icons import get_icon_image, get_icon
from hoverset.ui.widgets import Canvas, FontStyle, Frame, Entry, Button, Label, ScrollableInterface, EventMask


class CollapseFrame(Frame):

    def __init__(self, master, **cnf):
        super().__init__(master, **cnf)
        self.config(**self.style.dark)
        self._label_frame = Frame(self, **self.style.bright, height=20)
        self._label_frame.pack(side="top", fill="x", padx=2)
        self._label_frame.pack_propagate(0)
        self._label = Label(self._label_frame, **self.style.bright, **self.style.text_bright)
        self._label.pack(side="left")
        self._collapse_btn = Button(self._label_frame, width=20, **self.style.bright, **self.style.text_bright)
        self._collapse_btn.config(text=get_icon("triangle_up"))
        self._collapse_btn.pack(side="right", fill="y")
        self._collapse_btn.on_click(self.toggle)
        self.body = Frame(self, **self.style.dark)
        self.body.pack(side="top", fill="both", pady=2)
        self.__ref = Frame(self.body, height=0, width=0, **self.style.dark)
        self.__ref.pack(side="top")
        self._collapsed = False

    def update_state(self):
        self.__ref.pack(side="top")

    def collapse(self, *_):
        if not self._collapsed:
            self.body.pack_forget()
            self._collapse_btn.config(text=get_icon("triangle_down"))
            self.pack_propagate(0)
            self.config(height=20)
            self._collapsed = True

    def clear_children(self):
        self.body.clear_children()

    def expand(self, *_):
        if self._collapsed:
            self.body.pack(side="top", fill="both")
            self.pack_propagate(1)
            self._collapse_btn.config(text=get_icon("triangle_up"))
            self._collapsed = False

    def toggle(self, *_):
        if self._collapsed:
            self.expand()
        else:
            self.collapse()

    @property
    def label(self):
        return self._label["text"]

    @label.setter
    def label(self, value):
        self._label.config(text=value)


class SideBar(Canvas):

    def __init__(self, master):
        super().__init__(master)
        self.config(**self.style.dark, **self.style.no_highlight, width=20)
        self.features = {}

    def remove(self, feature):
        self.delete(feature.indicator)
        self.features.pop(feature)
        self._redraw()

    def _redraw(self):
        y = 0
        for feature in self.features:
            indicator = self.features[feature]
            font = FontStyle(self, self.itemconfig(indicator).get("font", "TkDefaultFont")[3])
            y += font.measure(feature.name) + 20
            self.coords(indicator, 18, y)

    def add_feature(self, feature):
        indicator = self.create_text(0, 0, angle=90, text=feature.name, fill=self.style.dark_on_hover.get("background"),
                                     anchor="sw", activefill=self.style.dark_on_hover.get("background"))
        font = FontStyle(self, self.itemconfig(indicator).get("font", "TkDefaultFont")[3])
        y = font.measure(feature.name) + self.bbox("all")[3] + 20
        self.coords(indicator, 18, y)
        self.tag_bind(indicator, "<Button-1>", lambda event: self.toggle_feature(feature))
        feature.indicator = indicator
        self.features[feature] = indicator

    def change_feature(self, new, old):
        self.tag_unbind(old.indicator, "<Button-1>")
        self.tag_bind(old.indicator, "<Button-1>", lambda event: self.toggle_feature(new))
        self.features.pop(old)
        self.features[new] = old.indicator
        new.indicator = old.indicator

    def deselect(self, feature):
        self.itemconfig(feature.indicator, fill=self.style.dark_text.get("foreground"))

    def select(self, feature):
        self.itemconfig(feature.indicator, fill=self.style.dark_on_hover.get("background"))

    def close_all(self):
        for feature in self.features:
            self.deselect(feature)

    def toggle_feature(self, feature):
        feature.toggle()


class SearchBar(Frame):

    def __init__(self, master=None, **cnf):
        super().__init__(master, **cnf)
        self.config(**self.style.no_highlight, **self.style.dark)
        self._entry = Entry(self, **self.style.dark_input)
        self._clear_btn = Button(self, image=get_icon_image("close", 15, 15),
                                 **self.style.dark_button, width=25, height=25)
        self._clear_btn.pack(side="right", fill="y")
        self._clear_btn.on_click(self._clear)
        Label(self, **self.style.dark_text, image=get_icon_image("search", 15, 15)).pack(side="left")
        self._entry.pack(side="left", fill="both", expand=True, padx=2)
        self._entry.on_entry(self._change)
        self._on_change = None
        self._on_clear = None

    def focus_set(self):
        super().focus_set()
        self._entry.focus_set()

    def on_query_change(self, func, *args, **kwargs):
        self._on_change = lambda val: func(val, *args, **kwargs)

    def on_query_clear(self, func, *args, **kwargs):
        self._on_clear = lambda: func(*args, **kwargs)

    def _clear(self, *_):
        if self._on_clear:
            self._on_clear()

    def _change(self, *_):
        if self._on_change:
            self._on_change(self._entry.get())


class DesignPad(ScrollableInterface, Frame):
    PADDING = 10

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._frame = Canvas(self, **kwargs, **self.style.no_highlight, **self.style.dark)
        self._frame.grid(row=0, column=0, sticky='nswe')
        self._scroll_y = ttk.Scrollbar(master, orient='vertical', command=self._y_scroll)
        self._scroll_x = ttk.Scrollbar(master, orient='horizontal', command=self._x_scroll)
        self._frame.configure(yscrollcommand=self._scroll_y.set, xscrollcommand=self._scroll_x.set)
        self.columnconfigure(0, weight=1)  # Ensure the design_pad gets the rest of the left horizontal space
        self.rowconfigure(0, weight=1)
        self._frame.bind('<Configure>', self.on_configure)
        self.bind('<Configure>', self.on_configure)
        self._child_map = {}
        self._on_scroll = None
        self._frame.create_line(0, 0, 0, 0)  # Ensure scroll_region always begins at 0, 0
        super().configure(bg="green")

    def on_mousewheel(self, event):
        try:
            if event.state & EventMask.CONTROL and self._scroll_x.winfo_ismapped():
                self._frame.xview_scroll(-1 * int(event.delta / 50), "units")
            elif self._scroll_y.winfo_ismapped():
                self._frame.yview_scroll(-1 * int(event.delta / 50), "units")
        except TclError:
            pass

    def scroll_position(self):
        return self._scroll_y.get()

    def on_scroll(self, callback, *args, **kwargs):
        self._on_scroll = lambda: callback(*args, **kwargs)

    def _y_scroll(self, *args):
        self._frame.yview(*args)
        if self._on_scroll:
            self._on_scroll()

    def _x_scroll(self, *args):
        self._frame.xview(*args)
        if self._on_scroll:
            self._on_scroll()

    def _show_y_scroll(self, flag):
        if flag and not self._scroll_y.winfo_ismapped():
            self._scroll_y.grid(in_=self, row=0, column=1, sticky='ns')
        elif not flag:
            self._scroll_y.grid_forget()
        self.update_idletasks()

    def _show_x_scroll(self, flag):
        if flag and not self._scroll_x.winfo_ismapped():
            self._scroll_x.grid(in_=self, row=1, column=0, columnspan=2, sticky='ew')
        elif not flag:
            self._scroll_x.grid_forget()
        self.update_idletasks()

    def on_configure(self, *_):
        try:
            self.update_idletasks()
            scroll_region = self._frame.bbox('all')
        except TclError:
            return
        if not scroll_region:
            print("failed to acquire scroll region")
            return
        scroll_w = scroll_region[2] - scroll_region[0]
        scroll_h = scroll_region[3] - scroll_region[1]

        self._show_y_scroll(scroll_h > self.winfo_height())
        self._show_x_scroll(scroll_w > self.winfo_width())

        self._frame.config(scrollregion=scroll_region)

    def place_child(self, child, **kw):
        x = kw.get("x", 0)
        y = kw.get("y", 0)
        w = kw.get("width", 1)
        h = kw.get("height", 1)
        self.forget_child(child)
        window = self._frame.create_window(x, y, window=child, width=w, height=h, anchor='nw')
        self._child_map[child] = window
        self.on_configure()

    def config_child(self, child, **kw):
        x = kw.get("x", child.winfo_x())
        y = kw.get("y", child.winfo_y())
        w = kw.get("width", child.winfo_width())
        h = kw.get("height", child.winfo_height())
        self._frame.coords(self._child_map[child], x, y)
        self._frame.itemconfigure(self._child_map[child], width=w, height=h)
        self.on_configure()

    def forget_child(self, child):
        if self._child_map.get(child) is not None:
            self._frame.delete(self._child_map[child])

    def configure(self, cnf=None, **kw):
        self._frame.configure(cnf, **kw)
        return super().configure(cnf, **kw)

    config = configure
