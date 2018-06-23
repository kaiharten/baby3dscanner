import tkinter as tk 
from tkinter import ttk
from tkinter import StringVar

import PIL
from PIL import Image
from PIL import ImageTk


import os
import cv2

LARGE_FONT = ("Verdana", 12)

class UserInterface(tk.Tk):
    
    def __init__(self, master):
        self.cam = master.cam
        self.master = master
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Babyscansysteem")

        screen_width = 800
        screen_height = 480
        resolution = str(screen_width) + "x" + str(screen_height)

        #self.geometry(resolution)

        self.frames= {}
        container = tk.Frame(self)
        container.grid(row=0,column=0,sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (UserInterface.StartPage, UserInterface.PageOne, UserInterface.GraphTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(UserInterface.StartPage)
        self.lift()
        self.attributes('-topmost',True)
        self.after_idle(self.attributes,'-topmost',False)
        self.attributes('-fullscreen', True)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    
    class StartPage(tk.Frame):
        def __init__(self, parent, controller):
            self.cam = controller.cam
            self.controller = controller
            tk.Frame.__init__(self, parent)
            self.config(cursor = 'none')

            top_frame = tk.Frame(self, bg='#F6F1D1', width=800, height=50)
            top_frame.grid(row=0, sticky="ew")

            black_bar = tk.Frame(top_frame, bg='#70A9A1', width=765, height=30)
            black_bar.grid(row=1, column=0, padx=20, pady=9)

            center = tk.Frame(self, bg='#F6F1D1', width=800, height=480)
            center.grid(row=1, sticky="nsew")

            bottom_frame = tk.Frame(self, bg='#F6F1D1', width=800, height=50)
            bottom_frame.grid(row=2, sticky="ew")

            progress_bar = ttk.Progressbar(bottom_frame, orient='horizontal', length = 765, mode='determinate')
            progress_bar.grid(row=1, column=0, padx =20, pady=5)
            
            black_bar2 = tk.Frame(bottom_frame, bg='#70A9A1', width=765, height=30)
            black_bar2.grid(row=2, column=0, padx=20, pady=3)
        
            center_left = tk.Frame(center, bg='#F6F1D1', width=380, height=380)
            center_left.grid(row=0, column=0, sticky="ns")

            self.center_right = tk.Frame(center, bg='#F6F1D1', width=420, height=380)
            self.center_right.grid(row=0, column=1, sticky="ns")

            self.label = tk.Label(center_left, bg='#90DDF0', text="idle", width=28)
            self.label.grid(row=0, column=0, padx=20)

            self.video = tk.Label(self.center_right, bg='#F6F1D1')
            self.video.grid(row=0, column=0)

            button_panel1 = tk.Frame(self.center_right, bg='#F6F1D1', width=200, height=200)
            button_panel1.grid(row=1, sticky="nsew")

            self.start_cam_button = tk.Button(button_panel1, text="Start Scan", height=4, width=11)
            self.start_cam_button.grid(row=0, column = 0, padx=5, pady=5)

            self.stop_cam_button = tk.Button(button_panel1, text="Test Motor", height=4, width=11)
            self.stop_cam_button.grid(row=0, column=1, padx=5, pady=5)

            self.but3_cam = tk.Button(button_panel1, text="Go To Results", height=4, width=12, command=lambda:controller.show_frame(UserInterface.PageOne))
            self.but3_cam.grid(row=0, column=2, padx=5, pady=5)

            self.but4_cam = tk.Button(button_panel1, text="Back Home", height=4, width=11)
            self.but4_cam.grid(row=0, column=3, padx=5, pady=5)

            self.show_video()
        def show_video(self):
            frame = self.cam.read()
            frame = cv2.resize(frame, (0,0), fx=0.395, fy=0.395)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video.imgtk = imgtk
            self.video.configure(image=imgtk)
            self.after(10, self.show_video)
        
        def add_function_to_button1(self,function):
            self.start_cam_button.config(command=function)

        def add_function_to_button2(self, function):
            self.stop_cam_button.config(command=function)
            
        def add_function_to_button3(self,function):
            self.but3_cam.config(command=function)
        
        def add_function_to_button4(self,function):
            self.but4_cam.config(command=function)
        
    class PageOne(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.config(cursor = 'none')
            label = tk.Label(self, text="Height Profile Page", font=LARGE_FONT)
            label.grid(row = 0, column = 1,pady=10,padx=10, sticky = "nesw")
            
            self.graph = tk.Label(self)
            self.graph.grid(row = 1, column = 1)
            
            self.data = []
            length_file = open("data/Untitled6456.m", "rb")
            self.data = length_file.readlines()
            self.data = self.data[0].decode("UTF-8")
            self.data = self.data.replace("00000", "")
            self.data = self.data.replace("e+02", "")
            self.data = self.data.replace(".", "")
            self.data = self.data.replace("   ", "")
            
            obj_length = self.data + " mm"
            self.length = tk.Label(self, text=obj_length)
            self.length.grid(row = 1, column = 2)
            
            button1 = tk.Button(self, text="Go to 3D Plot", command=lambda: controller.show_frame(UserInterface.GraphTwo))
            button1.grid(row = 2, column = 2)
            
            button2 = tk.Button(self, text="Go to Scan Page", command=lambda: controller.show_frame(UserInterface.StartPage))
            button2.grid(row = 2, column = 3)
            
            button3 = tk.Button(self, text="Update", command=self.update_graph)
            button3.grid(row = 2, column = 1)
            
            frame = cv2.imread("img/hoogteprofiel.png")
            
            frame = cv2.resize(frame, (0,0), fx=0.6, fy=0.6)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.graph.imgtk = imgtk
            self.graph.configure(image=imgtk)
            
        def update_graph(self):            
            frame = cv2.imread("img/hoogteprofiel.png")
            
            frame = cv2.resize(frame, (0,0), fx=0.6, fy=0.6)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.graph.imgtk = imgtk
            self.graph.configure(image=imgtk)
            
            length_file = open("data/Untitled6456.m", "rb")
            self.data = length_file.readlines()
            self.data = self.data[0].decode("UTF-8")
            self.data = self.data.replace("00000", "")
            self.data = self.data.replace("e+02", "")
            self.data = self.data.replace(".", "")
            self.data = self.data.replace("   ", "")
            
            obj_length = self.data + " mm"
            self.length = tk.Label(self, text=obj_length)
                
    class GraphTwo(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.config(cursor = 'none')
            label = tk.Label(self, text="3D Plot Page", font=LARGE_FONT)
            label.grid(row = 0, column = 1,pady=10,padx=10, sticky = "nesw")
            
            self.graph = tk.Label(self)
            self.graph.grid(row = 1, column = 1)
            frame = cv2.imread("img/3dplot.png")
            
            frame = cv2.resize(frame, (0,0), fx=0.6, fy=0.6)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.graph.imgtk = imgtk
            self.graph.configure(image=imgtk)
            
            button1 = tk.Button(self, text="Go to Height Plot", command=lambda: controller.show_frame(UserInterface.PageOne))
            button1.grid(row = 2, column = 2)
            
            button2 = tk.Button(self, text="Go to Scan Page", command=lambda: controller.show_frame(UserInterface.StartPage))
            button2.grid(row = 2, column = 3)
            
            button3 = tk.Button(self, text="Update", command=self.update_graph)
            button3.grid(row = 2, column = 1)
        def update_graph(self):            
            frame = cv2.imread("img/3dplot.png")
            
            frame = cv2.resize(frame, (0,0), fx=0.6, fy=0.6)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.graph.imgtk = imgtk
            self.graph.configure(image=imgtk)