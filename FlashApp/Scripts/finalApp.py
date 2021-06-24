
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 09:13:27 2021

@author: Vmaha
"""
import sys
from pathlib import Path
import linecache
import os
import time
import shutil
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from ctypes import windll

#Database 
import sqlite3 as sl


#Need Below Packages for Graphs
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading as th

from PIL import Image,ImageTk


class AppLayout(tk.Tk):
    def __init__(self,BackGround_LeftPane,BackGround_RightPane,leftPanelActiveBackGroundColor,leftPanelActiveForeGroundColor
                 ,initial_height,initial_width):
        tk.Tk.__init__(self)
        self.BackGround_LeftPane            = BackGround_LeftPane
        self.BackGround_RightPane           = BackGround_RightPane
        self.leftPanelActiveBackGroundColor = leftPanelActiveBackGroundColor
        self.leftPanelActiveForeGroundColor = leftPanelActiveForeGroundColor
        self.initial_height                 = initial_height
        self.initial_width                  = initial_width
        
        self.path = str(Path.home())
        self.ProfileImagePath = ''
        self.isProfileImageEnabled = 0

        
        self.loadSystemSettings()
        self.masterPane = tk.PanedWindow(self,height = self.initial_height,width = self.initial_width,bd=0,sashwidth =0 )
        self.leftPane   = tk.Frame(self.masterPane,bg = self.BackGround_LeftPane,height = 600,width = 300,relief = 'raised')
        self.masterPane.add(self.leftPane)
        
        self.rightPane   = tk.Frame(self.masterPane,bg = self.BackGround_RightPane)
        self.masterPane.add(self.rightPane)
        
        self.masterPane.pack(fill = 'both',expand = True)
        self.AddButtonsToLeftPane()
        
        #GLobal variables required to Handle Profile Image
        self.markCheck = False
        self.ProfileObjectCreated = False
        self.Settings()
        
        self.dashBoard()
        
        
        
    def createDataBaseConnection(self,DataBaseName):
        self.DB_connection = None
        self.DataBaseName  = DataBaseName
        
        try:
            self.DB_connection = sl.connect(self.DataBaseName)
        except sl.Error as Err:
            print(Err)
            
        return self.DB_connection
    
    def connectToSQLite(self):
        self.DataBaseName = os.path.join(self.path,'FlashApp\DataBase','FlashApp.db')
        Connection = self.createDataBaseConnection(self.DataBaseName)
        Connection.row_factory = sl.Row
        Curs = Connection.cursor()
        return Connection,Curs
    
    def loadSystemSettings(self):
        try:
            Connection,cursor = self.connectToSQLite()
            data = (0,os.path.join(self.path,'FlashApp\Assets\Images','ProfileImagePlaceHolder.jpg'))
            cursor.execute('''create table if NOT EXISTS SystemTable(
                isProfileImageEnabled INTEGER NOT NULL DEFAULT 0 CHECK(isProfileImageEnabled IN(0,1)),
                ProfilefileImagePath TEXT NOT NULL DEFAULT "C:\\Users\\Vmaha\FlashApp\\Assets\\Images\\ProfileImagePlaceHolder.jpeg")
                           ''')
                           
            #if there are 0 records in table then only run below step
            if len(cursor.execute('''select * from SystemTable ''').fetchall()) == 0:
                cursor.execute('''INSERT INTO SystemTable VALUES(?,?) ''',data)
                
            cursor.execute('''select * from SystemTable ''')
            row = cursor.fetchone()
            
            self.isProfileImageEnabled = row['isProfileImageEnabled']
            self.ProfileImagePath      = row['ProfilefileImagePath']
            
            Connection.commit()
            Connection.close()
            
        except sl.Error as Err:
            print("System Table Not Created because of below error \n",Err)
    # Function the find the exact error spot  
    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
        
    def dashBoard(self):
        
        self.Dashboard_Frame = tk.Frame(self.rightPane,bg =self.BackGround_RightPane)
        self.Dashboard_Frame.grid(row=0,column =0,sticky ='nsew')
        
        self.MenuName_Label = tk.Label(self.Dashboard_Frame,text = 'Dashboard',relief ='raised',
                                       bg =self.BackGround_RightPane,fg ='white',bd=0,font=("Arial", 15,'bold','underline'))
        self.MenuName_Label.grid(row = 1,column =0,sticky ='wn',padx=(30,0),pady =(10,0))
        
        def Display_Chart():
            
            def Draw_Graph(fig_dim,fig_pady,fig_padx,fig_row,fig_column,fig_sticky):
                  
                data1 = {'Country': ['US','CA','GER','UK','FR','IN'],
                         'GDP_Per_Capita': [45000,42000,52000,49000,47000,85000]
                         }
                df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])
            
                figure1 = plt.Figure(figsize= fig_dim, dpi=100)
                ax1 = figure1.add_subplot(111)
                bar1 = FigureCanvasTkAgg(figure1, self.Dashboard_Frame)
                bar1.get_tk_widget().grid(row=fig_row,column =fig_column,sticky =fig_sticky,pady=fig_pady,padx=fig_padx)
                                   
                df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
                df1.plot(kind='line', legend=True, ax=ax1,color ='w')
                ax1.set_title('Country Vs. GDP Per Capita',color ='w')
                
                ax1.yaxis.label.set_color('w')
                ax1.xaxis.label.set_color('w')
                ax1.spines['bottom'].set_color('w')
                ax1.spines['top'].set_color('w') 
                ax1.spines['right'].set_color('w')
                ax1.spines['left'].set_color('w')
                figure1.patch.set_facecolor('w')
                
                ax1.tick_params(colors='w', which='both')
            
                ax1.set_facecolor('#0a043c')
                figure1.set_facecolor('#000839')
                
                self.Dashboard_Frame.rowconfigure(1, weight=1)
                self.Dashboard_Frame.columnconfigure(0, weight=1)
        
            th.Thread(target = Draw_Graph((6,3),(40,10),20,1,0,'nswe')).start()
            th.Thread(target = Draw_Graph((6,3),(0,20),20,2,0,'nswe')).start()
            
            #th.Thread(target = Draw_Graph((4,2),(40,10),0,1,1,'nswe')).start()
            #th.Thread(target = Draw_Graph((4,2),(0,20),0,2,1,'nswe')).start()
            
            self.rightPane.columnconfigure(0, weight=1)
            self.rightPane.rowconfigure(0, weight=1)
            self.Dashboard_Frame.rowconfigure(1, weight=1)         
            self.Dashboard_Frame.rowconfigure(2, weight=1)       
            self.Dashboard_Frame.columnconfigure(0, weight=1)
            self.Dashboard_Frame.columnconfigure(1, weight=1)
            self.Dashboard_Frame.columnconfigure(3, weight=1)

        
        th.Thread(target=Display_Chart()).start()
        
    def AutomationMenu(self):
        
        self.Automation_Frame = tk.Frame(self.rightPane,bg =self.BackGround_RightPane)
        self.MenuName_Label = tk.Label(self.Automation_Frame,text = 'Automation',relief ='raised',
                                       bg =self.BackGround_RightPane,fg ='white',bd=0,font=("Arial", 15,'bold','underline'))
        self.MenuName_Label.grid(row = 1,column =0,sticky ='wn',padx=20,pady =(10,0))
        
        UpdateStatus = tk.StringVar() 
        tk.Label(self.Automation_Frame,pady = 10,font ='arial 9 bold',foreground ='green',
                 textvariable = UpdateStatus,bg = '#0C0026').grid(row=1,column =2,pady =(120,0))

        UpdateStatus.set('                                                       ')
      
        def ChooseFile():
            UpdateStatus.set('                                                          ')
            name_entry.delete(0, 'end')
            filename = filedialog.askopenfilename()
            name_entry.insert(0, filename)   

        def UploadFile():
            UpdateStatus.set('                                                            ')
            # show_ProgressBar function is running in seperate Thread to avoid Screen Freeze
            def show_ProgressBar():
                if (name_entry.get()) != '':
                    if os.path.isfile(name_entry.get()):
                        UpdateStatus.set('')
                        newval = 0
                        style = ttk.Style(self.Automation_Frame)
                        style.layout('text.Horizontal.TProgressbar',
                                     [('Horizontal.Progressbar.trough',
                                       {'children':[('Horizontal.Progressbar.pbar',
                                                     {'side':'left','sticky':'ns'})],
                                        'sticky':'nswe'}),
                                      ('Horizontal.Progressbar.label',{'sticky': ''})])
                                      
                        style.configure('text.Horizontal.Tprogressbar',text ='0 %')
                        
                        progress_Bar = ttk.Progressbar(self.Automation_Frame,style='text.Horizontal.TProgressbar',length =250,
                                                       maximum =100,value = 0)
                        progress_Bar.grid(row=1,column =2,pady =(120,0))
                        shutil.copy(name_entry.get(),r'C:\Users\Vmaha\Desktop\Work')
                        
                        for i in range(5):
                            self.Automation_Frame.update_idletasks()
                            progress_Bar['value'] +=20
                            newval +=20
                            style.configure('text.Horizontal.TProgressbar',text ='{:g} %'.format(newval))
                            time.sleep(1)
                        
                        progress_Bar.destroy()
                        UpdateStatus.set('File Uploaded Successfully!')
                      
                    else:
                        UpdateStatus.set('         File Not Found!')
                        
                else:
                    UpdateStatus.set('No File Selected for Upload')
            
            th.Thread(target = show_ProgressBar).start()

                
        def RunAutomation():
            pass
        
        ttk.Style().configure('pad.TEntry', padding='75 1 1 1')
        
        name_entry    = ttk.Entry(self.Automation_Frame,font =('calibre',10,'normal'),style='pad.TEntry')
        name_entry.focus()
        
        Browse_Button = tk.Button(self.Automation_Frame,text = 'Choose File',command = ChooseFile)
        Upload_Button = tk.Button(self.Automation_Frame,text = 'Upload',command = UploadFile)
        Run_Button = tk.Button(self.Automation_Frame,text = 'Run',command = RunAutomation)
        
        self.Automation_Frame.grid(row=0,column =0,sticky ='nsew')
        name_entry.grid(row=1,column=2,ipadx=80,ipady =4,sticky ='we')
        Browse_Button.grid(row=1,column=2,sticky ='w',padx=2)
        Upload_Button.grid(row=1,column=3,padx=3)
        Run_Button.grid(row=1,column=2,pady =(60,0))

        
        self.rightPane.columnconfigure(0, weight=1)
        self.rightPane.rowconfigure(0, weight=1)


        self.Automation_Frame.rowconfigure(1, weight=1)
        self.Automation_Frame.columnconfigure(1, weight=2)
        self.Automation_Frame.columnconfigure(5, weight=2)
   
    def MenuButton(self,PaneObj):
        global canvas
        canvas = tk.Canvas(PaneObj,relief ='sunken',bg=self.BackGround_LeftPane,width = 50,height = 40,highlightthickness = 0)
        line = canvas.create_line(10,10,80,10,fill = 'white',width = 5)
        line = canvas.create_line(10,20,80,20,fill = 'white',width = 5)
        line = canvas.create_line(10,30,80,30,fill = 'white',width = 5)
        canvas.grid(row =0 ,column =0,sticky ='nw')
        canvas.bind("<ButtonPress-1>",self.press)
        canvas.bind("<ButtonRelease-1>",self.release)   
     
    def Settings(self):
        self.isProfileImageOn  = tk.IntVar()
        
        def enableProfileImage():
            Connection,cursor = self.connectToSQLite()
            if self.isProfileImageOn.get() ==1:
                try:
                    cursor.execute('''update SystemTable set isProfileImageEnabled =1 ''')
                    if self.ProfileObjectCreated ==True:
                        self.canvas.grid()
                        self.imageEditIcon.grid()
                    else:
                        self.profileImage()
                        
                    self.markCheck = True
                    self.SettingsBtn1.select()
                except sl.Error as Err:
                    print("SQL Update Error in Settings Button",Err)
            else:
                cursor.execute('''update SystemTable set isProfileImageEnabled = 0 ''')
                self.canvas.grid_remove()
                self.imageEditIcon.grid_remove()
                self.SettingsBtn1.deselect()
                self.markCheck = False
                
            Connection.commit()
            Connection.close()
            
        
        self.Settings_Frame = tk.Frame(self.rightPane,bg = self.BackGround_RightPane)
        self.MenuName_Label = tk.Label(self.Settings_Frame,text = 'Settings',relief = 'raised',
                                       bg = self.BackGround_RightPane,fg ='white',bd =0,font =('Arial',15,'bold','underline'))
        
        self.SettingsBtn1 = tk.Checkbutton(self.Settings_Frame,text = 'Display Profile Picture',bg = self.BackGround_RightPane,
                                           fg ='white',font=('Arial',12),variable = self.isProfileImageOn,selectcolor ='black',
                                           onvalue =1,offvalue =0,command = enableProfileImage,padx =15,pady=15,
                                           activebackground = self.BackGround_RightPane)
        
        if self.isProfileImageEnabled ==1:
            self.profileImage()
            self.isProfileImageEnabled = 0
            self.SettingsBtn1.select()
            self.markCheck = True
            self.ProfileObjectCreated = True
            
        if self.markCheck ==True:
            self.SettingsBtn1.select()
            
        self.MenuName_Label.grid(row =1,column =0,sticky ='wn',padx=20,pady =20)
        self.SettingsBtn1.grid(row =2,column =0)
        self.Settings_Frame.grid(row =0,column =0,sticky ='news')
        
    def profileImage(self):
        
        self.editIconPath = os.path.join(self.path, 'FlashApp\Assets\Images',"edit.png")
        self.editIcon = ImageTk.PhotoImage(Image.open(self.editIconPath).resize((15,15),Image.ANTIALIAS))
        
        self.canvas = tk.Canvas(self.leftPane,width = 200,height =180,borderwidth =0,highlightthickness =0,
                                bg = self.BackGround_LeftPane)
        
        self.imageEditIcon = tk.Button(self.leftPane,command = self.changeProfileImage,
                                       image = self.editIcon,fg = self.BackGround_LeftPane,compound ='left',bd=0)
        
        self.imageEditIcon.grid(row =1,column =0,sticky ='e',padx=(0,25))
        
        self.img = ImageTk.PhotoImage(Image.open(self.ProfileImagePath).resize((150,150),Image.ANTIALIAS))
        self.image_on_canvas = self.canvas.create_image(120,110, image = self.img)
        
        self.canvas.create_oval(30,30,210,180,width=25,outline ='green')
        self.canvas.create_oval(0,0,240,210,width=80,outline =self.BackGround_LeftPane)
        self.canvas.grid(row=1,column =0,sticky ='n')
        
    def changeProfileImage(self):
        try:
            self.imgFileName = tk.filedialog.askopenfilename()
            shutil.copy(self.imgFileName,(os.path.join(self.path,'FlashApp\Assets\Images')))
            self.newImage = Path(self.imgFileName).name
            self.img_path = os.path.join(self.path,'FlashApp\Assets\Images',self.newImage)
            #if user has selected image then only update the files in database
            if self.imgFileName:
                data = (1,self.img_path)
                connection,cursor = self.connectToSQLite()
                cursor.execute('''update Systemtable set isProfileImageEnabled =?,ProfileImagePath =? ''',data)
                connection.commit()
                connection.close()
                
            self.img = ImageTk.PhotoImage(Image.open(self.img_path).resize((150,150),Image.ANTIALIAS))
            self.canvas.itemconfig(self.image_on_canvas,image = self.img)
        except sl.Error as Err:
            print('SQL Error Changing the profile Picture',Err)
            
    def on_enter(self,e):
        e.widget['background'] = self.leftPanelActiveForeGroundColor

    def on_leave(self,e):
        e.widget['background'] = self.BackGround_LeftPane
        
    def press(self,event):
        canvas.config(relief ='sunken')
        if LeftPanel ==0:
            self.hidePane()
        else:
            self.UnhideLeftPane()
    
    def release(self,event):
        canvas.config(relief ='flat')
        
    def UnhideLeftPane(self):
        global MenuButton1
        global LeftPanel1
        global LeftPanel
        LeftPanel =0
        
        # Reverting the padx =0 which was set to 40 in hidePane function 
        self.MenuName_Label.configure(padx=0)
        
        self.masterPane.paneconfigure(self.leftPane,hide = 'FALSE')
        canvas.grid_forget()
        
    def hidePane(self):
        global MenuButton1
        global LeftPanel
        self.bg2 = tk.PhotoImage(file =r'C:\Users\preet\.spyder-py3\Project Files\RightPan.png')
        self.bg2 = self.bg2.subsample(5,5)
        LeftPanel = 1
        
        # To avoid MenuName hide under Ham Burger Icon... Adding padx =40
        self.MenuName_Label.configure(padx=40)
        
        self.masterPane.paneconfigure(self.leftPane,hide = 'TRUE')   
        
        self.MenuButton(self.rightPane)
        canvas.grid(row =0,column =0)
        

    
    def AddButtonsToLeftPane(self):
      
        self.Img_DashBoard = tk.PhotoImage(file =r'C:\Users\Vmaha\Desktop\Blockchain\Tkinter\Assets\Dashboard5.png')
        self.Img_DashBoard = self.Img_DashBoard.subsample(12,12)
        
        self.Img_Automation = tk.PhotoImage(file =r'C:\Users\Vmaha\Desktop\Blockchain\Tkinter\Assets\Automation2.png')
        self.Img_Automation = self.Img_Automation.subsample(5,5)

        self.Img_CGMStatus = tk.PhotoImage(file =r'C:\Users\Vmaha\Desktop\Blockchain\Tkinter\Assets\Status2.png')
        self.Img_CGMStatus = self.Img_CGMStatus.subsample(5,5)

        self.Img_Settings = tk.PhotoImage(file =r'C:\Users\Vmaha\Desktop\Blockchain\Tkinter\Assets\Settings.png')
        self.Img_Settings = self.Img_Settings.subsample(10,12)
        
        self.Img_Hist = tk.PhotoImage(file =r'C:\Users\Vmaha\Desktop\Blockchain\Tkinter\Assets\Dashboard4.png')
        self.Img_Hist = self.Img_Hist.subsample(5,5)
                            
        
        self.Img_Watch = tk.PhotoImage(file =r'C:\Users\Vmaha\Desktop\Blockchain\Tkinter\Assets\Dashboard3.png')
        self.Img_Watch = self.Img_Watch.subsample(10,12)
        
        self.MenuButton(self.leftPane)
        
        
        
        btn1 = tk.Button(self.leftPane, text = 'Dashboard   ', image = self.Img_DashBoard,command =self.dashBoard, bg =self.BackGround_LeftPane,relief ='flat',
                  bd =0,padx =10,pady=10,font ='Arial',fg='white',activebackground = self.leftPanelActiveBackGroundColor,activeforeground=self.leftPanelActiveForeGroundColor,compound ='left') 
        
        btn2 = tk.Button(self.leftPane, text = 'Automation ',image = self.Img_Automation,bg =self.BackGround_LeftPane,
                         command = self.AutomationMenu, relief ='flat',
                      bd =0,padx =10,pady=10,font ='Arial',fg='white',activebackground = self.leftPanelActiveBackGroundColor,activeforeground=self.leftPanelActiveForeGroundColor,compound ='left')
        
        btn3 = tk.Button(self.leftPane, text = 'CGM Status',image = self.Img_CGMStatus,command = self.hidePane,bg = self.BackGround_LeftPane,relief ='flat',
                  bd =0,padx =10,pady=10,font ='Arial',fg='white',activebackground = self.leftPanelActiveBackGroundColor,activeforeground=self.leftPanelActiveForeGroundColor,compound ='left')
    
        btn4 = tk.Button(self.leftPane, text = 'History        ',image = self.Img_Hist,command = self.hidePane,bg = self.BackGround_LeftPane,relief ='flat',
                  bd =0,padx =10,pady=10,font ='Arial',fg='white',activebackground = self.leftPanelActiveBackGroundColor,activeforeground=self.leftPanelActiveForeGroundColor,compound ='left')
    
        btn5 = tk.Button(self.leftPane, text = 'Watch Later',image = self.Img_Watch,command= self.hidePane,bg =self.BackGround_LeftPane,relief ='flat',
                  bd =0,padx =10,pady=10,font ='Arial',fg='white',activebackground = self.leftPanelActiveBackGroundColor,activeforeground=self.leftPanelActiveForeGroundColor,compound ='left')
    
    
        btn6 = tk.Button(self.leftPane, text = 'Settings      ',image = self.Img_Settings,command = self.Settings,bg =self.BackGround_LeftPane,relief ='flat',
                  bd =0,padx =10,pady=10,font ='Arial',fg='white',activebackground = self.leftPanelActiveBackGroundColor,activeforeground=self.leftPanelActiveForeGroundColor,compound ='left')
    
        
        Company_Info = tk.Label(self.leftPane,text = 'Copyright @2021 Developed by Manpreet Malhi',fg ='white',bg = self.BackGround_LeftPane)
        
        btn1.grid(row =1,column =0,sticky ='we',ipady=5,ipadx =40) 
        btn2.grid(row =2,column =0,sticky ='we',ipady=5)
        btn3.grid(row =3,column =0,sticky ='we',ipady=5)
        btn4.grid(row =4,column =0,sticky ='we',ipady=5)
        btn5.grid(row =5,column =0,sticky ='we',ipady=5)
        btn6.grid(row =6,column =0,sticky ='we',ipady=5,pady =(110,20))
        Company_Info.grid(row=7,column =0,sticky ='e',pady=10,padx=(0,5))
        

        self.leftPane.rowconfigure(6, weight=1)
 
        btn1.bind("<Enter>", self.on_enter)
        btn1.bind("<Leave>", self.on_leave)
        
        btn2.bind("<Enter>", self.on_enter)
        btn2.bind("<Leave>", self.on_leave)
        
        btn3.bind("<Enter>", self.on_enter)
        btn3.bind("<Leave>", self.on_leave)
        
        btn4.bind("<Enter>", self.on_enter)
        btn4.bind("<Leave>", self.on_leave)
        
        btn5.bind("<Enter>", self.on_enter)
        btn5.bind("<Leave>", self.on_leave)
        
        btn6.bind("<Enter>", self.on_enter)
        btn6.bind("<Leave>", self.on_leave)
            
        
LeftPanel = 0
BackGround_LeftPane = '#0C0032'
BackGround_RightPane = '#0C0026'
leftPanelActiveBackGroundColor     = '#0C0060'
leftPanelActiveForeGroundColor     = '#0C0070'

initial_height = 650
initial_width  = 950


app = AppLayout(BackGround_LeftPane,BackGround_RightPane,leftPanelActiveBackGroundColor,leftPanelActiveForeGroundColor,
                initial_height,initial_width)
app.iconbitmap(r"C:\Users\preet\.spyder-py3\Project Files\flash.ico")

#Below 2 Lines of code are used to setup Icon for Task Bar
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app.title('Flash')
app.mainloop()