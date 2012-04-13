from Tkinter import Tk, RIGHT, LEFT, Y, Text, END, Frame, Label, Scrollbar
import text
import tkFileDialog
import tkMessageBox

class MainWindow(Frame):
    """
    Editor window
    """

    def __init__(self, master=None):
        Frame.__init__(self, master, width=800, height=600)
        self.master.title('pyeditor')
        self.open_files = []
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
        self.text_area.pack(side=LEFT, fill=Y)
        s.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=s.set)


    def get_contents(self):
        return self.text_area.get(1.0, END)


    def save_file(self, path):
        file = open(path, 'w+')
        file.write(self.get_contents())
        file.close()


    def open_file(self, path):
        self.check_files_saved()
        file = open(path, 'r')
        contents = file.read()
        self.text_area.delete(1.0, END)
        self.text_area.insert(1.0, contents)
        file.close()
        self.open_files.append((path, text.md5sum(contents)))


    def show_save_dialog(self, event=None, path=None):
        if not path is None:
            answer = tkMessageBox.askyesno('Save', 'Save file %s ?' % path)
            if answer:
                self.save_file(path)
        else:
            path = tkFileDialog.asksaveasfilename(defaultextension='.txt', title='Save file as')
            if len(path) > 0:
                self.save_file(path)


    def check_files_saved(self):
        contents = self.get_contents()
        if len(self.open_files) > 0:
            path, md5sum = self.open_files[0]
            if md5sum != text.md5sum(contents):
                self.show_save_dialog(path=path)
        elif len(contents) > 0:
            self.show_save_dialog()


    def quit(self):
        self.check_files_saved()
        self.master.destroy()


    def show_open_dialog(self, event=None):
        path = tkFileDialog.askopenfilename(title='Open file')
        self.open_file(path.strip())


    def set_keyboard_shortcuts(self):
        self.master.bind('<Control-o>', self.show_open_dialog)


def run():
    root = Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    run()
