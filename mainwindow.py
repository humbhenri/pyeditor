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
        self.set_title('pyeditor')
        self.master.geometry('640x480')
        self.buffers = []
        self.current_buffer = None
        self.create_widgets()
        self.set_keyboard_shortcuts()

    def create_widgets(self):
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.create_text_area()

    def create_text_area(self):
        self.text_area = Text(self.master, height=20, width=72)
        s = Scrollbar(self.master)
        self.text_area.focus_set()
        s.pack(side=RIGHT, fill=Y)
        self.text_area.pack(expand=1, fill=BOTH)
        s.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=s.set)
        self.buffers.append(Buffer(self.text_area))
        self.current_buffer = self.buffers[0]

    def get_contents(self):
        return self.current_buffer.contents.strip()

    def save_file(self, event=None, exiting=False):
        if self.current_buffer.filename is None and len(self.get_contents()) > 0:
            filename = self.show_save_dialog()
            self.current_buffer.filename = filename
            self.current_buffer.save()
            return
        if exiting:
            if self.show_question('Save file %s?' % self.current_buffer.filename):
                self.current_buffer.save()
            return
        self.current_buffer.save()

    def open_file(self, path):
        self.check_files_saved()
        self.current_buffer.filename = path
        self.current_buffer.load_file()
        self.set_title(path)

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
            self.current_buffer.filename = path
            self.current_buffer.load_file()

    def set_keyboard_shortcuts(self):
        self.master.bind('<Control-o>', self.show_open_dialog)
        self.master.bind('<Control-s>', self.save_file)

    def set_title(self, title):
        self.master.title(title)

    def show_question(self, msg):
        return tkMessageBox.askyesno('pyeditor', msg)


def run():
    root = Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    run()
