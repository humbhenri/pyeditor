# coding: latin

import Tkinter as tk
import text

class Buffer(tk.Text):
    """Manage file content in the editor
    """

    def __init__(self, master, filename=None, modified_callback=None):
        self.filename = filename
        self.md5 = None
        tk.Text.__init__(self, height=20, width=72)
        s = tk.Scrollbar(master)
        self.focus_set()
        s.pack(side=tk.RIGHT, fill=tk.Y)
        self.pack(expand=1, fill=tk.BOTH)
        s.config(command=self.yview)
        self.config(yscrollcommand=s.set)
        self.clear_modified_flag()
        self.bind('<<Modified>>', self.been_modified(modified_callback))

    def get_contents(self):
        return self.get(1.0, tk.END)

    def append(self, text):
        """
        Insert text in the end of the buffer
        """
        self.insert(tk.END, text)

    def add(self, text):
        """
        Insert text at current position
        """
        tk.Text.insert(tk.INSERT, text)

    def save(self):
        file = open(self.filename, 'w+')
        file.write(self.get_contents())
        file.close

    def load_file(self):
        file = open(self.filename, 'r')
        contents = file.read()
        file.close()
        self.delete(1.0, tk.END)
        self.insert(1.0, contents)
        self.md5 = text.md5sum(contents + '\n')

    def is_modified(self):
        return (not self.filename is None) and self.md5 != text.md5sum(self.contents)

    def clear_modified_flag(self):
        self._resetting_modified_flag = True
        try:
            self.tk.call(self._w, 'edit', 'modified', 0)
        finally:
            self._resetting_modified_flag = False

    def been_modified(self, event=None, callback=None):
        if self._resetting_modified_flag:
            return
        self.clear_modified_flag()
        if not callback is None:
            callback(event)

    contents = property(get_contents)
