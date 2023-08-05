"""
Common dialogs customised for hoverset platform
"""
# ======================================================================= #
# Copyright (C) 2020 Hoverset Group.                                      #
# ======================================================================= #

from hoverset.ui.widgets import Frame, Label, Window, Button, Application, ProgressBar
from hoverset.ui.icons import get_icon_image


class MessageDialog(Window):
    """
    Main class for creation of hoverset themed message dialogs. It has the various initialization
    methods for the common dialogs.
    """

    ICON_ERROR = "dialog_error"
    ICON_INFO = "dialog_info"
    ICON_WARNING = "dialog_warning"

    OKAY_CANCEL = "OKAY_CANCEL"
    YES_NO = "YES_NO"
    RETRY_CANCEL = "RETRY_CANCEL"
    SHOW_ERROR = "SHOW_ERROR"
    SHOW_WARNING = "SHOW_WARNING"
    SHOW_INFO = "SHOW_INFO"
    SHOW_PROGRESS = "SHOW_PROGRESS"
    BUILDER = "BUILDER"

    INDETERMINATE = ProgressBar.INDETERMINATE
    DETERMINATE = ProgressBar.DETERMINATE

    _MIN_BUTTON_WIDTH = 60

    def __init__(self, master, render_routine=None, **kw):
        super().__init__(master)
        self.configure(**self.style.dark)
        # ensure the dialog is above the parent window at all times
        self.transient(master)
        # take the screen focus
        self.grab_set()
        # prevent resizing by default
        self.resizable(False, False)
        self.bar = None
        # Common dialogs
        routines = {
            "OKAY_CANCEL": self._ask_okay_cancel,
            "YES_NO": self._ask_yes_no,
            "RETRY_CANCEL": self._ask_retry_cancel,
            "SHOW_ERROR": self._show_error,
            "SHOW_WARNING": self._show_warning,
            "SHOW_INFO": self._show_info,
            "SHOW_PROGRESS": self._show_progress,
            "BUILDER": self._builder  # Allows building custom dialogs
        }
        if render_routine in routines:
            # Completely custom dialogs
            routines.get(render_routine)(**kw)
        elif render_routine is not None:
            render_routine(self)
        self.enable_centering()
        self.value = None

    def _make_button_bar(self):
        self.bar = Frame(self, **self.style.dark, **self.style.dark_highlight_dim)
        self.bar.pack(side="bottom", fill="x")

    def _add_button(self, **kw):
        text = kw.get("text")
        focus = kw.get("focus", False)
        # If a button bar does not already exist we need to create one
        if self.bar is None:
            self._make_button_bar()
        btn = Button(self.bar, **self.style.dark_button, text=text, height=25)
        btn.configure(**self.style.dark_highlight_active)
        btn.pack(side="right", padx=5, pady=5)
        # ensure the buttons have a minimum width of _MIN_BUTTON_WIDTH
        btn.configure(width=max(self._MIN_BUTTON_WIDTH, btn.measure_text(text)))
        btn.on_click(kw.get("command", lambda _: self._terminate_with_val(kw.get("value"))))
        if focus:
            btn.focus_set()

    def _message(self, text, icon=None):
        # set default icon to INFO
        if icon is None:
            icon = self.ICON_INFO
        Label(self, **self.style.dark_text,
              text=text, anchor="w", compound="left", wrap=600, justify="left",
              pady=5, padx=15, image=get_icon_image(icon, 50, 50)
              ).pack(side="top", fill="x")

    def _ask_okay_cancel(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_INFO))
        self._add_button(text="Cancel", focus=True, command=lambda _: self._terminate_with_val(False))
        self._add_button(text="Ok", command=lambda _: self._terminate_with_val(True))

    def _ask_yes_no(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_INFO))
        self._add_button(text="No", focus=True, command=lambda _: self._terminate_with_val(False))
        self._add_button(text="Yes", command=lambda _: self._terminate_with_val(True))

    def _ask_retry_cancel(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_WARNING))
        self._add_button(text="Cancel", command=lambda _: self._terminate_with_val(False))
        self._add_button(text="Retry", focus=True, command=lambda _: self._terminate_with_val(True))

    def _show_error(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_ERROR))
        self._add_button(text="Ok", focus=True, command=lambda _: self.destroy())

    def _show_warning(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_WARNING))
        self._add_button(text="Ok", focus=True, command=lambda _: self.destroy())

    def _show_info(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_INFO))
        self._add_button(text="Ok", focus=True, command=lambda _: self.destroy())

    def _show_progress(self, **kw):
        self.title(kw.get("title", self.title()))
        text = kw.get('message', 'progress')
        icon = None
        if kw.get('icon'):
            icon = get_icon_image(icon, 50, 50)
        Label(self, **self.style.dark_text,
              text=text, anchor="w", compound="left", wrap=600, justify="left",
              pady=5, padx=15, image=icon
              ).pack(side="top", fill="x")
        self.progress = ProgressBar(self)
        self.progress.pack(side='top', fill='x', padx=20, pady=20)
        self.progress.mode(kw.get('mode', ProgressBar.DETERMINATE))
        self.progress.color(kw.get('colors', self.style.colors.get('accent', 'white')))
        self.progress.interval(kw.get('interval', ProgressBar.DEFAULT_INTERVAL))

    def _terminate_with_val(self, value):
        self.value = value
        self.destroy()

    def _builder(self, **kw):
        self.title(kw.get("title", self.title()))
        self._message(kw.get("message"), kw.get("icon", self.ICON_WARNING))
        actions = kw.get("actions")
        for action in actions:
            self._add_button(**action)

    @classmethod
    def ask(cls, form, **kw):
        """
        Create a dialog which returns a value when complete. You do not have to use this
        method directly since there are specialized methods for instance
        instead of -> use this
        MessageDialog.ask(MessageDialog.OKAY_CANCEL, ...) -> MessageDialog.ask_okay_cancel(...)
        MessageDialog.ask(MessageDialog.SHOW_INFO, ...) -> MessageDialog.show_info(...)
        :param form:
        :param kw: The keywords arguments included
        :return:
        """
        parent = kw.get("parent")
        dialog = MessageDialog(parent, form, **kw)
        dialog.wait_window()
        return dialog.value

    @classmethod
    def ask_okay_cancel(cls, **kw):
        return cls.ask(MessageDialog.OKAY_CANCEL, **kw)

    @classmethod
    def ask_question(cls, **kw):
        return cls.ask(MessageDialog.YES_NO, **kw)

    @classmethod
    def ask_retry_cancel(cls, **kw):
        return cls.ask(MessageDialog.RETRY_CANCEL, **kw)

    @classmethod
    def show_error(cls, **kw):
        parent = kw.get("parent")
        cls(parent, MessageDialog.SHOW_ERROR, **kw)

    @classmethod
    def show_warning(cls, **kw):
        parent = kw.get("parent")
        cls(parent, MessageDialog.SHOW_WARNING, **kw)

    @classmethod
    def show_info(cls, **kw):
        parent = kw.get("parent")
        cls(parent, MessageDialog.SHOW_INFO, **kw)

    @classmethod
    def show_progress(cls, **kw):
        parent = kw.get("parent")
        dialog = cls(parent, MessageDialog.SHOW_PROGRESS, **kw)
        return dialog

    @classmethod
    def builder(cls, *buttons, **kw):
        parent = kw.get("parent")
        kw["actions"] = buttons
        dialog = cls(parent, MessageDialog.BUILDER, **kw)
        if kw.get("wait", False):
            dialog.wait_window()
            return dialog.value


if __name__ == '__main__':
    app = Application()
    app.load_styles(r"themes\default.css")
    app.geometry('700x600')
    val = MessageDialog.builder(
        {"text": "Continue", "value": "continue", "focus": True},
        {"text": "Pause", "value": "pause"},
        {"text": "Cancel", "value": False},
        wait=True,
        title="Builder",
        message="We just built this dialog from scratch",
        parent=app,
        icon="flame"
    )
    print(val)
    MessageDialog.ask_retry_cancel(title="ask_okay", message="This is an ask-okay-cancel message", parent=app)
    app.mainloop()
