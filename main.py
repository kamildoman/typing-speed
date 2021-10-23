from tkinter import *
import tkinter.messagebox
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

timer = 0
counting_start = False
random_text = ""

#returns similarity between given text and entered text. The similarity is a float between 0 and 1
def check_similarity():
    a = entering_text.get(1.0, END)
    b = generated_dummy_text.get(1.0, END)
    return SequenceMatcher(None, a, b).ratio()

#starting to count the time and updates the counter
def count():
    if counting_start:
        global timer
        timer += 1
        window.after(1000, count)
        counter.config(text= timer)

#unblocks the input text and starts counting
def start():
    getDummyText()
    generated_dummy_text.config(state=NORMAL)
    generated_dummy_text.delete(1.0, END)
    generated_dummy_text.insert(INSERT, random_text)
    generated_dummy_text.config(state=DISABLED)

    entering_text.config(state=NORMAL)
    entering_text.delete(1.0, END)

    global counting_start, timer
    timer = 0
    counting_start = True
    bStartStop.config(text="Stop", command=finish)
    count()

#if you try to copy the generated dummy text it'll show you the information
def copyingInfo(*args):
    tkinter.messagebox.showinfo("Don't try it", "Please don't cheat :) You can't copy the text")

#it needs to take *args because you can activate the function both by the button and pressing enter
def finish(*args):
    global counting_start, timer
    counting_start = False
    ratio = round(check_similarity(), 2)
    length = len(entering_text.get(1.0, END)) - 1
    speed = round(length/float(timer), 2)
    #the minimum required similarity to get results is 0.8. If it's below it you get score 0
    if ratio < 0.8:
        tkinter.messagebox.showinfo("Finished!", f"Your result is {timer} seconds/{length} characters ({speed} chars/sec). The similarity is {ratio}. The similarity is too low - you get 0 points :(")
    else:
        points = round(ratio * 100 + speed * 10, 2)
        tkinter.messagebox.showinfo("Finished!", f"Your result is {timer} seconds/{length} characters ({speed} chars/sec). The similarity is {ratio}. The total score is: {points}")
    entering_text.config(state=DISABLED)
    bStartStop.config(text="Start", command=start)

#get a random dummy text
def getDummyText():
    global random_text
    link = "https://www.randomtextgenerator.com/"
    r = requests.get(link)
    r.status_code
    soup = BeautifulSoup(r.content, "html.parser")
    paragraphs = soup.find("div", { "id" : "randomtext_box" })
    random_text = paragraphs.text.split("\n")[1].strip()

window = Tk()
window.minsize(500, 500)
window.config(padx= 20, pady= 30)


generated_dummy_text = Text(font=("Arial", 15), width=80, height=10, padx=10, pady=10, state=NORMAL)
#prevents from copying the generated dummy text
generated_dummy_text.bind("<Key>", copyingInfo)
generated_dummy_text.grid(row=0, column=0)

#this one you enter your text. It's disabled untill you start the program
entering_text = Text(font=("Arial", 15), width=80, height=10, padx=10, pady=10, state=DISABLED)
entering_text.grid(row=1, column=0)
entering_text.focus_set()

bStartStop = Button(text="Start", command=start, width=20, height=2)
bStartStop.grid(row=2, column=0)


counter = Label(text = timer)
counter.grid(row=3, column=0)

window.bind("<Return>", finish)
count()


window.mainloop()

