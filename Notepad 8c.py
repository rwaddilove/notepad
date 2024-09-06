# RAW Notepad: A learning project for Python and Tkinter
# by Roland Waddilove (https://github.com/rwaddilove)
# This is a simple notes app written in Python as a learning exercise.
# It uses the built in Tkinter module to create the window, buttons and menus.
# It is not meant to be a commercial app. I used it to learn Python/Tkinter.
# It's probably not the best code, but hopefully, it will help others.
# Features:
# * Bold, Italic, Bold-Italic text
# Ctrl/Cmd X, C, V to cut, copy, paste on PC/Mac
# Load and save text files, including fonts and styles.


import tkinter as tk
from tkinter import ttk 
from tkinter import scrolledtext, font, filedialog, messagebox


# Menu handlers -------------------------------------
def menu_save():
    if myfile[1]:
        save_file()           # save if there's a file path
    else:
        menu_saveas()         # save as if there's no file path


def save_file():
    with open(myfile[1], 'w') as file:              # should really catch errors here
        text_content = textbox.get("1.0", "end-1c")
        file.write(text_content)                              # plain text
    with open(myfile[1]+'.tag', 'w') as file:       # other info saved separately
        file.write(str(combo_fonttype.get())+'\n')     # font family
        file.write(str(combo_fontsize.get())+'\n')     # font size
        file.write(str(textbox.dump('1.0', 'end', tag=True)))   # tags - text styles
    textbox.edit_modified(False)                          # text not modified (since saved)


def menu_saveas():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        myfile[1] = file_path
        save_file()
        set_title()


def set_title():
    if '/' in myfile[1]:
        myfile[0] = myfile[1].split('/')[len(myfile[1].split('/'))-1]     # Mac
    else:
        myfile[0] = myfile[1].split('\\')[len(myfile[1].split('\\'))-1]   # Windows
    window.title(myfile[0])


def menu_open():
    file_path = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=[('text files', '*.txt'), ('All files', '*.*')])
    if file_path == '': return                           # exit if no file selected
    menu_new()                                           # reset everything
    with open(file_path, 'r') as file:         # read plain text
        txt = file.read()
        textbox.insert('1.0', txt)
    with open(file_path+'.tag', 'r') as file:  # read tags styles
        ff = file.readline().strip()                     # font family
        fs = file.readline().strip()                     # font size
        tags = file.readline()                           # tags - text styles
    myfile[1] = file_path
    set_title()

    # set font and size in combo boxes
    combo_fonttype.current(fontfamily.index(ff))
    combo_fontsize.current(fontsizes.index(fs))
    set_font_size()

    # apply tags to text
    if len(tags) < 5: return            # no tags found
    chars = "[]()' "
    for char in chars:                  # remove unnecessary characters
        tags = tags.replace(char, '')
    tgs = tags.split(',')           # tgs=list (tagon,tagname,position), (tagonoff,tagname,position),...
    for i in range(0,len(tgs), 6):
        if tgs[i+1] == 'BOLD':
            textbox.tag_add('BOLD', tgs[i+2], tgs[i+5])
        if tgs[i+1] == 'ITALIC':
            textbox.tag_add('ITALIC', tgs[i+2], tgs[i+5])
        if tgs[i+1] == 'BOLDITALIC':
            textbox.tag_add('BOLDITALIC', tgs[i+2], tgs[i+5])
    textbox.edit_modified(False)        # text not modified (since opened)


def menu_copy():
    textbox.event_generate("<<Copy>>")

def menu_paste():
    textbox.event_generate("<<Paste>>")

def menu_cut():
    textbox.event_generate("<<Cut>>")


def button_bold():
    if textbox.tag_ranges(tk.SEL):
        button_clear()      # clear any previous tags
        textbox.tag_add("BOLD", "sel.first", "sel.last")

def button_italic():
    if textbox.tag_ranges(tk.SEL):
        button_clear()      # clear any previous tags
        textbox.tag_add("ITALIC", "sel.first", "sel.last")

def button_bolditalic():
    if textbox.tag_ranges(tk.SEL):
        button_clear()      # clear any previous tags
        textbox.tag_add("BOLDITALIC", "sel.first", "sel.last")

def button_clear():
    if textbox.tag_ranges(tk.SEL):
        textbox.tag_remove("BOLD",  "sel.first", 'sel.last')
        textbox.tag_remove("ITALIC",  "sel.first", 'sel.last')
        textbox.tag_remove("BOLDITALIC",  "sel.first", 'sel.last')


def menu_new():
    if textbox.edit_modified():  # if text has been modified
        if messagebox.askquestion('Warning!', 'Text has been modified. Save?') == 'yes':
            menu_save()
    textbox.delete('1.0', 'end')
    myfile[1], myfile[0] = '', ''        # filename, filepath
    window.title('RAW Notepad')
    combo_fonttype.current(0)   # reset font family
    combo_fontsize.current(1)   # reset font size
    set_font_size()
    textbox.focus()   # place cursor in text area
    textbox.edit_modified(False)     # text not modified (since new)


def set_font_size():
    myfont = [combo_fonttype.get(), int(combo_fontsize.get())]
    textbox.config(font=(myfont[0], myfont[1]))
    textbox.tag_config("BOLD", font=(myfont[0], myfont[1], "bold"))
    textbox.tag_config("ITALIC", font=(myfont[0], myfont[1], "italic"))
    textbox.tag_config("BOLDITALIC", font=(myfont[0], myfont[1], "bold", "italic"))  # shouldn't work, but does


def combo_fontsize_changed(event):
    set_font_size()

def combo_fonttype_changed(event):
    set_font_size()


# Create the main window -----------------------------------
window = tk.Tk()
window.geometry("600x400")
window.resizable(True, True)
window.columnconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

# Font setup -----------------------------------------------
fontfamily = ["Arial", "Verdana", "Times New Roman","Courier New"]
fontsizes = ["10", "12", "14", "16", "18", "24"]
normal_font = font.Font(family=fontfamily[0], size=int(fontsizes[0]), weight="normal")
bold_font = font.Font(family=fontfamily[0], size=int(fontsizes[0]), weight="bold")
italic_font = font.Font(family=fontfamily[0], size=int(fontsizes[0]), slant="italic")
bolditalic_font = font.Font(family=fontfamily[0], size=int(fontsizes[0]), weight="bold", slant="italic")

# Toolbar frame -------------------------------------------
pad_x = 5
tbar_frame= tk.Frame(window, pady=5)
tbar_frame.grid(column=0, row=0, sticky="nw")

btn_Bold = tk.Button(tbar_frame, text='Bold', command=button_bold)
btn_Ital = tk.Button(tbar_frame, text='Italic', command=button_italic)
btn_BoldItal = tk.Button(tbar_frame, text='Bold/Italic', command=button_bolditalic)
btn_clear = tk.Button(tbar_frame, text='Clear', command=button_clear)
btn_Bold.grid(row=0, column=0, padx=pad_x)
btn_Ital.grid(row=0, column=1, padx=pad_x)
btn_BoldItal.grid(row=0, column=2, padx=pad_x)
btn_clear.grid(row=0, column=3, padx=pad_x)

combo_fonttype=ttk.Combobox(tbar_frame, values=fontfamily, width=14)
combo_fontsize=ttk.Combobox(tbar_frame, values=fontsizes, width=4)
combo_fonttype.grid(row=0, column=6, padx=pad_x, sticky="sw")       # sticky="sw" - needed to align with buttons
combo_fontsize.grid(row=0, column=7, padx=pad_x, sticky="sw")
combo_fontsize.bind('<<ComboboxSelected>>', combo_fontsize_changed)
combo_fonttype.bind('<<ComboboxSelected>>', combo_fonttype_changed)

# Text frame -------------------------------------------
frame_2 = tk.Frame(window, padx=0, pady=0)
frame_2.grid(column=0, row=1, sticky="nsew")
frame_2.columnconfigure(0, weight=1)
frame_2.rowconfigure(0, weight=1)
textbox = scrolledtext.ScrolledText(frame_2, wrap=tk.WORD, font=normal_font, height=8, width=40) 
textbox.grid(column=0, row=0, pady=10, padx=10, sticky="nsew")
textbox.tag_configure("BOLD", font=bold_font)
textbox.tag_configure("ITALIC", font=italic_font)
textbox.tag_configure("BOLDITALIC", font=bolditalic_font)

# Menu bar -------------------------------------
menubar = tk.Menu(window)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label='New                ', command=menu_new)
file_menu.add_command(label='Open               ', command=menu_open)
file_menu.add_command(label='Save               ', command=menu_save)
file_menu.add_command(label='Save as...         ', command=menu_saveas)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=window.destroy)     # quit the program - save first!
menubar.add_cascade(label=' File', menu=file_menu)

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label='Copy           ', command=menu_copy)    # Can use Ctrl/Cmd+C
edit_menu.add_command(label='Cut            ', command=menu_cut)     # Can use Ctrl/Cmd+X
edit_menu.add_command(label='Paste          ', command=menu_paste)   # Can use Ctrl/Cmd+V
edit_menu.add_separator()
menubar.add_cascade(label="Edit", menu=edit_menu)

window.config(menu=menubar)

# All done -------------------------------------
myfile = ['', '']   # filename, filepath
menu_new()
window.mainloop()
