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
    if myfile[notebook.index(notebook.select())]:   # myfile[] contains file paths for tabs
        save_file()           # if there's a file path
    else:
        menu_saveas()         # if there's no file path


def save_file():
    file_path = myfile[notebook.index(notebook.select())]                          # get file path for this tab
    textbox = txt_widget[notebook.index(notebook.select())]                        # get text widget
    with open(file_path, 'w') as file:              # should really catch errors here
        text_content = textbox.get("1.0", "end-1c")
        file.write(text_content)                              # plain text
    with open(file_path+'.tag', 'w') as file:       # other info saved separately
        file.write(str(combo_fonttype.get())+'\n')     # save font family
        file.write(str(combo_fontsize.get())+'\n')     # save font size
        file.write(str(textbox.dump('1.0', 'end', tag=True)))  # save tags (text styles)
    textbox.edit_modified(False)                              # text not modified (since saved)


def menu_saveas():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path: return
    myfile[notebook.index(notebook.select())] = file_path   # remember file path
    save_file()
    set_title()


def set_title():
    notebook_idx = notebook.index(notebook.select())
    file_path = myfile[notebook_idx]
    if '/' in file_path:
        filename = file_path.split('/')[len(file_path.split('/'))-1]     # Mac
    else:
        filename = file_path.split('\\')[len(file_path.split('\\'))-1]   # Windows
    notebook.tab(notebook_idx, text=filename)


def menu_open_new_tab():
    add_tab()
    menu_open()


def menu_open() -> None:
    """Open a file in the current notebook tab."""
    notebook_idx = notebook.index(notebook.select())    # current tab number
    textbox = txt_widget[notebook_idx]                         # current textbox widget
    if textbox.edit_modified() and messagebox.askquestion('Warning!', 'Save current text?') == 'yes':
        menu_save()     # save if it has changed since last save

    file_path = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=[('text files', '*.txt'), ('All files', '*.*')])
    if file_path == '': return              # exit if no file selected
    myfile[notebook_idx] = file_path        # remember file path
    set_title()                             # set tab title to filename

    # menu_new()                                           # reset everything for this tab
    textbox.delete('1.0', 'end')
    try:
        with open(file_path, 'r') as file:         # read plain text
            txt = file.read()
            textbox.insert('1.0', txt)
    except:
        textbox.insert('1.0', 'File could not be opened!')
    try:
        with open(file_path+'.tag', 'r') as file:  # read tags styles
            fontfam = file.readline().strip()                       # font family
            fontsz = file.readline().strip()                        # font size
            tags = file.readline()                                  # get tags (text styles)
    except:
        fontfam, fontsz, tags = fontfamily[0], fontsizes[1], ''
    combo_fonttype.current(fontfamily.index(fontfam))  # select font family
    combo_fontsize.current(fontsizes.index(fontsz))    # select font size
    set_font_size()                                             # apply font size

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
    textbox = txt_widget[notebook.index(notebook.select())]
    textbox.event_generate("<<Copy>>")

def menu_paste():
    textbox = txt_widget[notebook.index(notebook.select())]
    textbox.event_generate("<<Paste>>")

def menu_cut():
    textbox = txt_widget[notebook.index(notebook.select())]
    textbox.event_generate("<<Cut>>")

def button_bold():
    textbox = txt_widget[notebook.index(notebook.select())]
    if textbox.tag_ranges(tk.SEL):
        button_clear()      # clear any previous tags
        textbox.tag_add("BOLD", "sel.first", "sel.last")

def button_italic():
    textbox = txt_widget[notebook.index(notebook.select())]
    if textbox.tag_ranges(tk.SEL):
        button_clear()      # clear any previous tags
        textbox.tag_add("ITALIC", "sel.first", "sel.last")

def button_bolditalic():
    textbox = txt_widget[notebook.index(notebook.select())]
    if textbox.tag_ranges(tk.SEL):
        button_clear()      # clear any previous tags
        textbox.tag_add("BOLDITALIC", "sel.first", "sel.last")

def button_clear():
    textbox = txt_widget[notebook.index(notebook.select())]
    if textbox.tag_ranges(tk.SEL):
        textbox.tag_remove("BOLD",  "sel.first", 'sel.last')
        textbox.tag_remove("ITALIC",  "sel.first", 'sel.last')
        textbox.tag_remove("BOLDITALIC",  "sel.first", 'sel.last')

def menu_new():
    textbox = txt_widget[notebook.index(notebook.select())]         # get textbox on current tab
    if textbox.edit_modified() and messagebox.askquestion('Warning!', 'Save current text?') == 'yes':
        menu_save()
    delete_tab()
    add_tab()

def set_font_size():
    myfont = [combo_fonttype.get(), int(combo_fontsize.get())]    # myfont = [font family, font size]
    textbox = txt_widget[notebook.index(notebook.select())]                              # textbox = text widget on current tab
    textbox.config(font=(myfont[0], myfont[1]))                     # set font size/family
    textbox.tag_config("BOLD", font=(myfont[0], myfont[1], "bold"))
    textbox.tag_config("ITALIC", font=(myfont[0], myfont[1], "italic"))
    textbox.tag_config("BOLDITALIC", font=(myfont[0], myfont[1], "bold", "italic"))  # shouldn't work, but does

def add_tab():
    if len(txt_widget) > 10: return     # can't have more than 10 tabs
    tab = ttk.Frame(notebook)
    tab.columnconfigure(0, weight=1)
    tab.rowconfigure(0, weight=1)
    notebook.add(tab, text='Unsaved', sticky='nesw')
    textbox = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=normal_font)
    textbox.grid(column=0, row=0, sticky='nesw')
    textbox.tag_configure("BOLD", font=bold_font)
    textbox.tag_configure("ITALIC", font=italic_font)
    textbox.tag_configure("BOLDITALIC", font=bolditalic_font)
    txt_widget.append(textbox)      # add textbox to list
    myfile.append('')               # set file path to empty string
    notebook.select(tab)     # select new tab
    textbox.focus_set()
    combo_fonttype.current(0)   # reset font family
    combo_fontsize.current(1)   # reset font size
    set_font_size()
    textbox.edit_modified(False)     # text not modified (since new)

def delete_tab():
    txt_widget.pop(notebook.index(notebook.select()))                # remove textbox from list
    myfile.pop(notebook.index(notebook.select()))                    # remove file path from list
    if len(txt_widget) == 0: add_tab()                # got to have at least 1 tab
    notebook.forget(notebook.select())

def tab_selected(event):
    textbox = txt_widget[notebook.index(notebook.select())]    # textbox = text widget on current tab
    f = textbox.cget('font')
    if not ' ' in f: return
    for i in range(0, len(fontfamily)):
        if fontfamily[i] in f:
            combo_fonttype.current(i)
    for i in range(0, len(fontsizes)):
        if fontsizes[i] in f:
            combo_fontsize.current(i)

def combo_changed(event):
    set_font_size()

# End of functions ------------------------------------------


# Create the main window -----------------------------------
window = tk.Tk()
window.geometry("600x400")
window.title("RAW Notepad")
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
pad_x = 0
tbar_frame= tk.Frame(window, padx=20, pady=10)
tbar_frame.grid(column=0, row=0, sticky="nw")

btn_add_tab = tk.Button(tbar_frame, text=' + ', command=add_tab)
btn_Bold = tk.Button(tbar_frame, text='Bold', command=button_bold)
btn_Ital = tk.Button(tbar_frame, text='Italic', command=button_italic)
btn_BoldItal = tk.Button(tbar_frame, text='Bold/Italic', command=button_bolditalic)
btn_clear = tk.Button(tbar_frame, text='Clear', command=button_clear)
btn_add_tab.grid(row=0, column=0, padx = 5)
btn_Bold.grid(row=0, column=1, padx=pad_x)
btn_Ital.grid(row=0, column=2, padx=pad_x)
btn_BoldItal.grid(row=0, column=3, padx=pad_x)
btn_clear.grid(row=0, column=4, padx=pad_x)

combo_fonttype=ttk.Combobox(tbar_frame, values=fontfamily, width=14)
combo_fontsize=ttk.Combobox(tbar_frame, values=fontsizes, width=4)
combo_fonttype.grid(row=0, column=5, padx=5, sticky="sw")       # sticky="sw" - needed to align with buttons
combo_fontsize.grid(row=0, column=6, padx=5, sticky="sw")

# Create a notebook widget --------------------------------
txt_widget = []     # list of text widgets on tabs
myfile = ['']       # filenames of opened files
notebook = ttk.Notebook(window)
notebook.grid(column=0, columnspan=10, row=1, sticky="nsew")

# Menu bar -------------------------------------
menubar = tk.Menu(window)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label='New                ', command=menu_new)
file_menu.add_command(label='New tab            ', command=add_tab)
file_menu.add_separator()
file_menu.add_command(label='Open               ', command=menu_open)
file_menu.add_command(label='Open on new tab    ', command=menu_open_new_tab)
file_menu.add_separator()
file_menu.add_command(label='Save               ', command=menu_save)
file_menu.add_command(label='Save as...         ', command=menu_saveas)
file_menu.add_separator()
file_menu.add_command(label='Delete tab         ', command=delete_tab)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=window.destroy)     # quit the program - save first!
menubar.add_cascade(label=' File', menu=file_menu)

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label='Copy           ', command=menu_copy)    # Can use Ctrl/Cmd+C
edit_menu.add_command(label='Cut            ', command=menu_cut)     # Can use Ctrl/Cmd+X
edit_menu.add_command(label='Paste          ', command=menu_paste)   # Can use Ctrl/Cmd+V
menubar.add_cascade(label="Edit", menu=edit_menu)

window.config(menu=menubar)
combo_fontsize.bind('<<ComboboxSelected>>', combo_changed)
combo_fonttype.bind('<<ComboboxSelected>>', combo_changed)
notebook.bind("<<NotebookTabChanged>>", tab_selected)

# All done -------------------------------------
add_tab()
window.mainloop()
