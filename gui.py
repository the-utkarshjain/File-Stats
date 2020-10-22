from tkinter import *
import tkinter.scrolledtext as tkscrolled
from tkinter import filedialog
import string
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from collections import Counter
from stopwords import *
from numpy import *
from keywords import *

# Generates the GUI
def make_gui():

    # File explorer for text file
    def browseFiles():

        root.filename = filedialog.askopenfilename(initialdir = "./", title = "Select a file", filetypes = (("Text files", "*.txt"),("all files","*.*")))
        file_stats()
    

    # File explorer for keyword file
    def keywordfile():

        root.keywordfilename = filedialog.askopenfilename(initialdir = "./", title = "Select a file", filetypes = (("Text files", "*.txt"),("all files","*.*")))
        processkeyword()


    # Displays the sentences which have atleast one keyword
    def processkeyword():
       
        msg = search_keywords(root.keywordfilename, root.sentences, root.originalsentences)

        message_2.config(state='normal')
        message_2.delete('1.0', END)
        message_2.insert(END,msg)
        message_2.config(state='disabled')


    # Displays the file stats
    def file_stats():

        # opening the input text file in read mode
        file = open(root.filename, "r").read()
        
        root.words = [] # To store all the words
        root.originalsentences = file.replace("\n", " ").strip().split(".") # To store the orginal sentence
        root.sentences = root.originalsentences.copy() # To store processed sentences

        root.sentences = [i for i in root.sentences if i != '']

        # Stripping all the sentences and converting to lower case to match with keywords and get correct frequency
        for i in range(len(root.sentences)):
            processed_line = root.sentences[i].strip().lower()
            root.sentences[i] = processed_line
            root.words.extend([i.strip(string.punctuation) for i in processed_line.split()])
    
        root.dict = Counter(root.words) # root.dict stores the frequency of each word as a dictionary

        most_common, least_common = most_least_frequency() # Function call to most_least_frequency()
        show_hist() # Function call to show_hist()

        # Text to be printed in the stats message
        msg = "1. Number of words: " + str(len(root.words)) + "\n" 
        msg += "2. Number of sentences: " + str(len(root.sentences)) + "\n"
        msg += "3. Number of newlines: " + str(file.count("\n")) + "\n"
        msg += "4. Most occuring word: " + str(most_common) + "\n"
        msg += "5. Least occuring word: " + str(least_common)
        
        message_1.config(state='normal')
        message_1.delete('1.0', END)
        message_1.insert(END,msg)
        message_1.config(state='disabled')


    # Function to generate and display the histogram
    def show_hist():

        f.clear()
        p = f.gca()
        x = (range(len(root.dict)))
        y = (range(max(root.dict.values())+1))
        new_x = [2*i for i in x]
        p.bar(new_x,root.dict.values(),width=0.4,align = "edge")
        p.set_ylabel('Frequency', fontsize = 10)
        p.set_xticks(new_x,minor=False)
        p.set_yticks(y,minor=False)
        p.set_xticklabels(root.dict.keys(),fontdict = None,rotation=90, minor =False)
        
        ccanvas.draw()


    # Function to search the most and least frequent word
    def most_least_frequency():

        sorted_list = root.dict.most_common()

        # Searching the most common word
        for key, value in sorted_list:
            if(key not in stopwords):
                most_common = (key, value)
                break
            else:
                continue

        # Searching the least common word
        for key, value in reversed(sorted_list):
            if(key not in stopwords):
                least_common = (key, value)
                break
            else:
                continue
        
        return most_common, least_common
    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))


    root = Tk()
    root.title('File Stats')
    root.geometry("1500x1500")
    canvas = Canvas(root, borderwidth=0, background="#ffffff")
    frame = Frame(canvas, background="#ffffff")
    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    hsb = Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=hsb.set)

    hsb.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((-10,-10), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    

    # Canvas for displaying historgram
    f = Figure(figsize = (10,5), dpi = 100)
    ccanvas = FigureCanvasTkAgg(f, master=frame)
    toolbar = NavigationToolbar2Tk(ccanvas, frame) 
    toolbar.update()
    scrollbar = Scrollbar(master=root, orient=HORIZONTAL)
    scrollbar.pack(side = BOTTOM, fill = X)
    scrollbar["command"] = ccanvas.get_tk_widget().xview
    ccanvas.get_tk_widget()["xscrollcommand"] = scrollbar.set
   

    # Other components
    welcome_label = Label(frame, text="Welcome to File Stats!", width = 100, height = 1, font=("TkDefaultFont", 15, "bold"))
    label1 = Label(frame, text="Histogram", height = 1, anchor="w", font=("TkDefaultFont", 15, "bold"))
    label2 = Label(frame, text="Analysis for FILE - 1", height = 1, anchor="w", font=("TkDefaultFont", 15, "bold"))
    label3 = Label(frame, text="Analysis for FILE - 2", height = 1, anchor="w", font=("TkDefaultFont", 15, "bold"))

    file1_explorer = Button(frame, text = "Browse input files", command = browseFiles)
    file1_refresh = Button(frame, text = "Show Stats", command = file_stats)
    file2_explorer = Button(frame, text = "Browse keyword file", command = keywordfile)
    process = Button(frame, text = "Process", command = processkeyword)
    button_exit = Button(frame, text = "Exit", command = exit)

    message_1 = Text(frame, height=5, width=500, font=("TkDefaultFont", 15), state='disabled')
    message_2 = tkscrolled.ScrolledText(frame, height=6, width=500, font=("TkDefaultFont", 15), state='disabled')

    welcome_label.pack()
    label1.pack(fill = X, padx = 12)
    ccanvas.get_tk_widget().pack(padx = 12, anchor="w")
    label2.pack(fill = X, pady = 1, padx = 12)
    message_1.pack(padx = 12, anchor="w")
    label3.pack(fill = X, pady = 2, padx = 12)
    message_2.pack(padx = 12, anchor="w")
    file1_explorer.pack(side = LEFT, anchor = S, ipadx = 2, ipady = 2, padx = 3)
    file1_refresh.pack(side = LEFT, anchor = S, ipadx = 2, ipady = 2, padx = 3)
    file2_explorer.pack(side = LEFT, anchor = S, ipadx = 2, ipady = 2, padx = 3)
    process.pack(side = LEFT, anchor = S, ipadx = 2, ipady = 2, padx = 3)
    button_exit.pack(side = LEFT, anchor = S, ipadx = 2, ipady = 2, padx = 3)
    #populate(frame)
    root.mainloop()
