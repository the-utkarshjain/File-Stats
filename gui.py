from tkinter import *
from tkinter import filedialog
import string
from collections import Counter

# Generates the GUI
def make_gui():

    # File explorer for text file
    def browseFiles():

        root.filename = filedialog.askopenfilename(initialdir = "./", title = "Select a file", filetypes = (("Text files", "*.txt"),("all files","*.*")))
        with open(root.filename,"r+") as file:
            for i in file:
                text.insert(END, i)
        file_stats()
    def saveFiles():

    
        with open(root.filename,"r+") as file:
            input=text.get("1.0",END)
            file.seek(0)
            file.write(re.sub(r"<string>ABC</string>(\s+)<string>(.*)</string>", r"<xyz>ABC</xyz>\1<xyz>\2</xyz>", input))
            file.truncate()

    # Displays the file stats
    def file_stats():

        file = open(root.filename, "r").read()
        root.words = []
        root.sentences = file.replace("\n", " ").strip().split(".")
        for i in range(len(root.sentences)):
            line = root.sentences[i]
            processed_line = line.strip().lower()
            root.words.extend([i.strip(string.punctuation) for i in processed_line.split()])
    
        root.dict = Counter(root.words)
        msg = "Number of words: " + str(len(root.words)) + "\n" 
        msg +="Number of sentences: " + str(len(root.sentences)) + "\n"
        msg += "Number of newlines: " + str(file.count("\n")) + "\n"

        message_1.config(text = msg, bg = 'grey')


    root = Tk()
    root.title('File Stats')
    root.geometry("1000x1000")

    welcome_label = Label(root, text="Welcome to File Stats!", width = 100, height = 4)
    file1_explorer = Button(root, text = "Browse Files", command = browseFiles)
    file1_save = Button(root, text = "Save File", command = saveFiles)
    file1_refresh = Button(root, text = "Show Stats", command = file_stats)

    button_exit = Button(root, text = "Exit kardunga", command = exit)

    message_1 = Message(root, text = "", width=500, justify = 'left')
    text = Text(root, height=10, width=200) 

    welcome_label.pack()
    file1_explorer.pack()
    file1_refresh.pack()
    file1_save.pack()
    button_exit.pack()
    message_1.pack()
    text.pack(side=RIGHT, expand=True)
    root.mainloop()

