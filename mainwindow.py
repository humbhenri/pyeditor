# coding: latin
from Tkinter import Tk, RIGHT, LEFT, Y, Text, END, Frame, Label, Scrollbar, BOTH
import text
import tkFileDialog
import tkMessageBox
from buffer import Buffer

class MainWindow(Frame):
    """
    Editor window
    """

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('pyeditor')
        self.master.geometry('640x480')
        self.buffers = []
        self.current_buffer = None
        self.create_widgets()
        self.set_keyboard_shortcuts()

    def create_widgets(self):
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.create_text_area()

    def create_text_area(self):
        buffer = Buffer(self.master, modified_callback=self.set_title)
        self.buffers.append(buffer)
        self.current_buffer = buffer

    def get_contents(self):
        return self.current_buffer.contents.strip()

    def save_file(self, event=None, exiting=False):
        if len(self.get_contents()) == 0 and self.current_buffer.filename is None:
            return
        if self.current_buffer.filename is None:
            filename = self.show_save_dialog()
            if len(filename) == 0:
                return
            self.current_buffer.filename = filename
            self.current_buffer.save()
        elif exiting and \
                self.current_buffer.is_modified() and \
                self.show_question('Save file %s?' % self.current_buffer.filename):
            self.current_buffer.save()

    def open_file(self, path):
        self.check_files_saved()
        self.current_buffer.filename = path
        self.current_buffer.load_file()
        self.set_title()

    def show_save_dialog(self):
        path = tkFileDialog.asksaveasfilename(title='Save file as')
        return path

    def check_files_saved(self):
        self.save_file(exiting=True)

    def quit(self):
        self.check_files_saved()
        self.master.destroy()

    def show_open_dialog(self, event=None):
        path = tkFileDialog.askopenfilename(title='Open file')
        if len(path) > 0:
            self.open_file(path)

    def set_keyboard_shortcuts(self):
        self.master.bind('<Control-o>', self.show_open_dialog)
        self.master.bind('<Control-s>', self.save_file)

    def set_title(self, event=None):
        self.master.title(self.current_buffer.filename)

    def show_question(self, msg):
        return tkMessageBox.askyesno('pyeditor', msg)


def run():
    root = Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    run()
