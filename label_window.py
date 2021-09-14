import os
import json

import tkinter as tk
from PIL import ImageTk, Image

class LabelUI(tk.Frame):
    '''
    |-----------|
    | 5   4   3 |
    | 6   *   2 |
    | 7   0   1 |
    |-----------|
    | <       > |
    '''

    def __init__(self, main:tk.Tk=None):
        super().__init__(main)
        self.main = main
        self.main.geometry('600x700')
        self.create_widgets()


    # Initializing =======================================================================
    def load_directory(self, dir_path, out):
        self.label_json_path = out
        self.dir_path = dir_path
        self.load_image_queue()
        self.curr_queue_index = 0
        self.load_labels()
        self.load_image()
        self.curr_label = -1


    def load_image_queue(self):
        self.image_queue = []
        for f in os.listdir(self.dir_path):
            image_path = os.path.join(self.dir_path, f)
            if os.path.isfile(image_path) and os.path.splitext(image_path)[1] in ['.jpg', '.jpeg', '.png']:
                self.image_queue.append(f)


    def load_labels(self):
        if os.path.isfile(self.label_json_path):
            with open(self.label_json_path, 'r') as f:
                self.label_json = json.load(f)
        else:
            self.label_json = dict()
        print('Printing {}'.format(self.label_json_path))


    # Creating UI =======================================================================
    def create_widgets(self):
        self.skip_labeled = tk.IntVar(value=0)
        self.create_label_section()
        self.create_nav_section()


    def create_label_section(self):
        button0 = tk.Button(master=self.main, text = 'front\n(,)', command= lambda: self.labelCallBack(0))
        button1 = tk.Button(master=self.main, text = 'front-right\n(.)', command= lambda: self.labelCallBack(315))
        button2 = tk.Button(master=self.main, text = 'right\n(l)', command= lambda: self.labelCallBack(270))
        button3 = tk.Button(master=self.main, text = 'back-right\n(o)', command= lambda: self.labelCallBack(225))
        button4 = tk.Button(master=self.main, text = 'back\n(i)', command= lambda: self.labelCallBack(180))
        button5 = tk.Button(master=self.main, text = 'back-left\n(u)', command= lambda: self.labelCallBack(135))
        button6 = tk.Button(master=self.main, text = 'left\n(j)', command= lambda: self.labelCallBack(90))
        button7 = tk.Button(master=self.main, text = 'front-left\n(m)', command= lambda: self.labelCallBack(45))

        button0.grid(row = 2, column = 1, sticky='NSEW', pady=2)
        button1.grid(row = 2, column = 2, sticky='NSEW', pady=2)
        button2.grid(row = 1, column = 2, sticky='NSEW', pady=2)
        button3.grid(row = 0, column = 2, sticky='NSEW', pady=2)
        button4.grid(row = 0, column = 1, sticky='NSEW', pady=2)
        button5.grid(row = 0, column = 0, sticky='NSEW', pady=2)
        button6.grid(row = 1, column = 0, sticky='NSEW', pady=2)
        button7.grid(row = 2, column = 0, sticky='NSEW', pady=2)
        
        self.main.columnconfigure(0, weight=1)
        self.main.columnconfigure(1, weight=1)
        self.main.columnconfigure(2, weight=1)
        self.main.rowconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=1)
        self.main.rowconfigure(2, weight=1)
    
        self.main.bind('<KeyPress>', lambda event: self.labelKeyPressCallBack(event))


    def labelKeyPressCallBack(self, e):
        if e.char == ',':
            self.labelCallBack(0)
        if e.char == '.':
            self.labelCallBack(315)
        if e.char == 'l':
            self.labelCallBack(270)
        if e.char == 'o':
            self.labelCallBack(225)
        if e.char == 'i':
            self.labelCallBack(180)
        if e.char == 'u':
            self.labelCallBack(135)
        if e.char == 'j':
            self.labelCallBack(90)
        if e.char == 'm':
            self.labelCallBack(45)


    def labelCallBack(self, label):
        print(label)
        self.curr_label = label
        self.save_label()
        self.nextCallBack()


    def load_image(self):
        self.curr_image_name = self.image_queue[self.curr_queue_index]
        curr_image_path = os.path.join(self.dir_path, self.curr_image_name)
        print(self.curr_image_name)
        image = Image.open(curr_image_path)
        image.thumbnail(size=(300, 300))
        self.photo = ImageTk.PhotoImage(image=image)

        image_pane = tk.Label(master=self.main, image=self.photo)
        image_pane.grid(row=1, column=1, sticky='NSEW', pady=2)


    def save_label(self):
        if self.curr_label != -1:
            self.label_json[self.curr_image_name] = self.curr_label
            with open(self.label_json_path, 'w') as f:
                json.dump(self.label_json, f)


    def create_nav_section(self):
        instruct = tk.Label(master=self.main, text='Which direction is the character facing?')
        buttonprev = tk.Button(master=self.main, text='prev\n(left-arrow)', command= lambda:self.prevCallBack())
        buttonsave = tk.Button(master=self.main, text='save', command= lambda:self.saveCallBack())
        buttonnext = tk.Button(master=self.main, text='next\n(right-arrow/Return)', command= lambda:self.nextCallBack())
        buttondelete = tk.Button(master=self.main, text='delete', command= lambda:self.deleteImageCallBack())
        checkbuttonskip = tk.Checkbutton(master=self.main, text='Skip Labeled Images', variable=self.skip_labeled)

        instruct.grid(row=3, column=1, columnspan=2)
        checkbuttonskip.grid(row=3, column=0, pady=2)
        buttonprev.grid(row=4, column=0, sticky='NSEW', pady=2)
        buttonsave.grid(row=4, column=1, sticky='NSEW', pady=2)
        buttonnext.grid(row=4, column=2, sticky='NSEW', pady=2)
        buttondelete.grid(row=5, column=0, sticky='NSEW', pady=2)

        self.main.bind('<Left>', lambda event: self.prevCallBack())
        self.main.bind('<Right>', lambda event: self.nextCallBack())
        self.main.bind('<Return>', lambda event: self.nextCallBack())


    def nextCallBack(self):
        self.curr_queue_index = min(len(self.image_queue) - 1, self.curr_queue_index + 1)
        if self.skip_labeled.get():
            while self.curr_queue_index < len(self.image_queue) - 1 and self.image_queue[self.curr_queue_index] in self.label_json:
                self.curr_queue_index = min(len(self.image_queue) - 1, self.curr_queue_index + 1)
        print('next', self.curr_queue_index)
        self.load_image()
        self.curr_label = -1


    def prevCallBack(self):
        self.curr_queue_index = max(self.curr_queue_index - 1, 0)
        print('prev', self.curr_queue_index)
        self.load_image()
        self.curr_label = -1

    
    def saveCallBack(self):
        self.save_label()


    def deleteImageCallBack(self):
        img_name = self.image_queue[self.curr_queue_index]
        curr_image_path = os.path.join(self.dir_path, img_name)
        try:
            os.remove(curr_image_path)
            if img_name in self.label_json:
                self.label_json.pop(img_name)
            self.image_queue.pop(self.curr_queue_index)

            self.save_label()
            self.load_image()
        except OSError:
            pass
        except IndexError:
            image_pane = tk.Label(master=self.main, text="No more images.")
            image_pane.grid(row=1, column=1, sticky='NSEW', pady=2)