import os
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


class Filebrowser:
    def __init__(self):
        """
        Luokkaan määritelty ohjelman käyttöliittymän elementit
        ja nappien funktiot.
          """

        self.__rootfolder = "/"
        self.__pathtext = "Current path: "
        self.__location = self.__rootfolder

        self.__window = Tk()
        self.__window.title("File browser")
        self.__window.columnconfigure(1, weight=1)

        self.__window.columnconfigure(1, weight=1)
        for i in range(6, 31):
            self.__window.rowconfigure(i, weight=1)

        self.__pathlabel = Label(text=self.__pathtext + self.__location)
        self.__pathlabel.grid(row=0, column=0, columnspan=2, pady=2, sticky=NW)

        self.__open_button = Button(text="Open", command=self.open, width=8)
        self.__open_button.grid(row=1, column=0, pady=1, padx=2)

        self.__back_button = Button(text="Back", command=self.back, width=8,
                                    state="disabled")
        self.__back_button.grid(row=2, column=0, pady=1)

        self.__makefolder_button = Button(text="New Folder",
                                          width=8, command=self.makefolder)
        self.__makefolder_button.grid(row=3, column=0, pady=1)

        self.__deletebutton = Button(text="Delete", width=8,
                                     command=self.delete_file)
        self.__deletebutton.grid(row=4, column=0, pady=1)

        self.__lstbx = Listbox(self.__window, width=60, height=25,
                               active="dotbox")
        self.__lstbx.grid(row=1, column=1, rowspan=30, padx=1, pady=0, sticky=NSEW)

        self.__lstbx.bind("<Double-Button>", lambda x: self.__open_button.invoke())

        for i in os.listdir(self.__location):
            self.__lstbx.insert(END, i)

    def open(self):
        """
        Open-napin ja kaksoisnäpäytyksen funktio joka avaa valitun kansion sisällön näytettäväksi
        listboxissa. Näyttää myös virheikkunan mikäli käyttäjä
        yrittää avata jonkin muun tiedoston kuin kansion
        tai kansion johon hänellä ei ole pääsyoikeutta.
        """
        goto = self.__lstbx.get(ACTIVE)
        if self.__location != self.__rootfolder:
            self.__location += ("/" + goto)
        else:
            self.__location += goto
        self.__pathlabel.configure(text=self.__pathtext + self.__location)

        self.__back_button.configure(state="active")

        try:
            self.refresh()

        except NotADirectoryError:
            self.back()
            messagebox.showerror("Error",
                                 "Choose a directory, not a file.")
        except PermissionError:
            self.back()
            messagebox.showerror("Error",
                                 "You do not have permission"
                                 " to view this folder.")

    def back(self):
        # Back-napin funktio joka palauttaa
        # listboxin sisällöksi edellisen kansion.

        if self.__location != self.__rootfolder:
            newpath = self.__location.split("/")
            newpath.remove(newpath[-1])
            path = "/".join(newpath)

            if path == "":
                path = self.__rootfolder
                self.__back_button.configure(state="disabled")
            self.__location = path
            self.__pathlabel.configure(text=self.__pathtext + self.__location)
        else:
            self.__back_button.configure(state="disabled")

        self.refresh()

    def makefolder(self):
        # New folder-napin funktio. Avaa uuden ikkunan
        # jossa pyydetään käyttäjältä uuden kansion nimeä
        # jonka jälkeen uusi kansio luodaan nykyisen kansion sisälle.

        inputwindow = Tk()
        inputwindow.withdraw()
        user_input = simpledialog.askstring(
            title="Name your folder",
            prompt="Create new folder in {}".format(self.__location))

        if user_input:
            if self.__location != self.__rootfolder:
                new_folder_path = self.__location + "/" + user_input
            else:
                new_folder_path = self.__location + user_input
            try:
                os.mkdir(new_folder_path)
            except PermissionError:
                messagebox.showerror("Error",
                                     "You do not have permission"
                                     " to make a folder in this directory.")

        self.refresh()

    def delete_file(self):
        # Poistaa valitun tiedoston tai tyhjän kansion.
        # Kysyy ensin käyttäjältä varmistusta.

        to_delete = self.__lstbx.get(ACTIVE)
        confirmation_window = messagebox.askyesno("Delete file",
                                                  "Delete {}?"
                                                  .format(to_delete))
        if self.__location != self.__rootfolder:
            deletion_path = self.__location + "/" + to_delete
        else:
            deletion_path = self.__rootfolder + to_delete

        if confirmation_window:
            try:
                os.rmdir(deletion_path)

            except NotADirectoryError:
                os.remove(deletion_path)

            except OSError:
                messagebox.showerror(
                    "Folder not empty",
                    "Remove all files from {} before deleting"
                        .format(to_delete))
        self.refresh()

    def refresh(self):
        # Päivittää Listboxin sisällön self.__path muuttujan mukaiseksi.
        # ja muuttaa open ja delete nappien tilaa mikäli
        # kansiossa on tai ei ole tiedostoja.

        directory_contents = os.listdir(self.__location)

        self.__lstbx.delete(0, END)
        for i in directory_contents:
            self.__lstbx.insert(END, i)

        if len(directory_contents) == 0:
            self.__open_button.configure(state="disabled")
            self.__deletebutton.configure(state="disabled")
        else:
            self.__open_button.configure(state="active")
            self.__deletebutton.configure(state="active")

    def start(self):
        # Käynnistää käyttöliittymän.

        self.__window.mainloop()


ui = Filebrowser()
ui.start()

