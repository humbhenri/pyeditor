# -*- coding: UTF-8 -*-

from Tkinter import *
import text

class Buffer(object):
    """Manage file content in the editor
    """

    def __init__(self, textarea, filename=None):
        self.filename = filename
        self.textarea = textarea
        self.md5 = None

    def get_contents(self):
        return self.textarea.get(1.0, END)

    def append(self, text):
        """
        Insert text in the end of the buffer
        """
        self.textarea.insert(END, text)

    def insert(self, text):
        """
        Insert text at current position
        """
        self.textarea.insert(INSERT, text)

    def save(self):
        file = open(self.filename, 'w+')
        file.write(self.get_contents())
        file.close

    def load_file(self):
        file = open(self.filename, 'r')
        contents = file.read()
        file.close()
        self.textarea.delete(1.0, END)
        self.textarea.insert(1.0, contents)
        self.md5 = text.md5sum(contents)

    contents = property(get_contents)
