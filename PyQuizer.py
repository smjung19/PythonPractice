# Import Packages ====================================================================================================

from tkinter import *
from PIL import Image, ImageTk
import os
import random
import time

# Set Path ====================================================================================================

my_path = os.path.dirname(os.path.realpath(__file__))
image_path = my_path + "/Amino Acids"

# Import Dataset ====================================================================================================

FileList = os.listdir(image_path)
ImageList = []
for image in FileList:
    if image.endswith(".jpg"):
        ImageList.append(image)
indices = []
# Define Functions ====================================================================================================

def CheckAnswer():
    global ImageName
    InputAnswer = AnswerEntry.get()
    RawList = ImageName.split(".")[0]
    CorrectAnswer = RawList.split(",")
    LowerCorrectAnswer = [x.lower() for x in CorrectAnswer]
    AnswerEntry.delete(0, "end")
    if InputAnswer.lower() in LowerCorrectAnswer:
        CheckLabel.config(text=f"Correct!\nIt is '{CorrectAnswer[0]}, {CorrectAnswer[1]}, {CorrectAnswer[2]}'.", fg="#2ecc71", bg="#2c3e50", font=("Times New Roman", 20))
        tk.update()
        time.sleep(0.5)
    else:
        CheckLabel.config(text=f"Incorrect.\nThe correct answer is '{CorrectAnswer[0]}, {CorrectAnswer[1]}, {CorrectAnswer[2]}'.", fg="#e74c3c", bg="#2c3e50", font=("Times New Roman", 20))
        tk.update()
        time.sleep(1)
    DisplayImage()

def DisplayImage():
    global ImageName
    global indices
    if len(indices) == 0:
        indices = list(range(len(ImageList)))
        random.shuffle(indices)
        CheckLabel.config(text="Loop Finished!\nWait for a second...", fg="#2ecc71", bg="#2c3e50", font=("Times New Roman", 20))
        tk.update()
        time.sleep(1)
    CheckLabel.config(text="Type Your Answer!\n", fg="#2ecc71", bg="#2c3e50", font=("Times New Roman", 20))
    tk.update
    index = indices.pop(0)
    ImageName = ImageList[index]
    image = Image.open(image_path + "/" + ImageName).resize((340, 540))
    photo = ImageTk.PhotoImage(image)
    ImageLabel.config(image=photo)
    ImageLabel.image = photo

# Define Factors ====================================================================================================

tk = Tk()
tk.title("Flashcard Program")
tk.config(bg="#2c3e50")

ImageLabel = Label(tk, image=None)

AnswerEntry = Entry(tk)
AnswerEntry.bind("<Return>", lambda event: CheckAnswer())

CheckLabel = Label(tk)



# Set Location====================================================================================================

ImageLabel.pack(side = TOP, padx = 50, pady = 50)

CheckLabel.pack(side = TOP, padx = 10, pady = 10)

AnswerEntry.pack(side = TOP, padx = 10, pady = 10)

width = 600
height = 800

x = (tk.winfo_screenwidth() // 2) - (width // 2) - 35
y = (tk.winfo_screenheight() // 2) - (height // 2) - 35

tk.geometry("{}x{}+{}+{}".format(width, height, x, y))

# Main ====================================================================================================

indices = list(range(len(ImageList)))
random.shuffle(indices)

AnswerEntry.focus()

DisplayImage()

tk.mainloop()
