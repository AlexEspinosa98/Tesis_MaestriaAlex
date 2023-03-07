
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from PIL import Image, ImageTk 
#import matplotlib as plt
import os
import cv2

import shutil

class MyWindow:
    def __init__(self, win):
         #boton de selecion de archivo
        self.butt_carp1=Button(win, text='Guard_anomalias',command=self.save_carp1)#command=funcion
        self.butt_carp1.place(x=210, y=70)

        self.butt_carp2=Button(win, text='Guard_no_anomalias',command=self.save_carp2)#command=funcion
        self.butt_carp2.place(x=320, y=70)

        self.butt_carp3=Button(win, text='Guard_extras',command=self.save_carp3)#command=funcion
        self.butt_carp3.place(x=450, y=70)

        self.butt_selc=Button(win, text='sel_dirección', command=self.read_listfile)#command=funcion
        self.butt_selc.place(x=100, y=50)

        self.imageFrame2 = Frame(win, width=320, height=260)  #creo que no es necesario la segunda
        self.imageFrame2.place(x=200,y=150)   #ubicacion dentro del frame (cuadro dentro del cuadro)
        #self.imageFrame2.pack()


        self.butt_pass1=Button(win, text='<<',command=self.des_izquierda)#command=funcion
        self.butt_pass1.place(x=150, y=150)

        self.butt_pass2=Button(win, text='>>', command=self.des_derecha)#command=funcion
        self.butt_pass2.place(x=550, y=150)

        """ frame = Frame(win, width=600, height=400)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5) """

        self.display1 = Label(self.imageFrame2)
        self.display1.place(x=0,y=0)
        """ self.img = cv2.imread('./data/Fotos_muestras/result_g1/DJI_0010_0_0.JPG') # leeamos la imagen inicial de fondo : 
        self.img=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        print(self.img.shape[1])
        print(self.img.shape[0])
        print(self.img.shape)
        self.img=cv2.resize(self.img,dsize=(self.img.shape[1]*2,self.img.shape[0]*2), interpolation=cv2.INTER_LINEAR)
        #cv2.imshow("comparación",self.img)
        self.img = Image.fromarray(self.img) """

        

        """ self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.display1.imgtk = self.imgtk #Mostramos imagen sin procesar en el display 1(izquierda)
        self.display1.configure(image=self.imgtk) """
        
    def read_listfile(self):
        self.archivo_abierto=filedialog.askopenfilename(initialdir = "/",
            title = "Seleccione archivo",filetypes = (("jpeg files","*.jpg"),("jpeg files","*.mp4"),
            ("all files","*.*")))
        self.path_carpet=os.path.dirname(self.archivo_abierto)
        self.lista=os.listdir(os.path.dirname(self.path_carpet+'/'))

        self.limpieza_nombres()
        self.actualizar()

    def actualizar(self):
        self.img = cv2.imread(self.path_carpet+'/'+self.lis_jpg[self.var]) # leeamos la imagen inicial de fondo : 
        self.img=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        """ print(self.img.shape[1])
        print(self.img.shape[0])
        print(self.img.shape) """
        self.img=cv2.resize(self.img,dsize=(self.img.shape[1]*2,self.img.shape[0]*2), interpolation=cv2.INTER_LINEAR)
        #cv2.imshow("comparación",self.img)
        self.img = Image.fromarray(self.img)
        self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.display1.imgtk = self.imgtk #Mostramos imagen sin procesar en el display 1(izquierda)
        self.display1.configure(image=self.imgtk)
        pass

    def limpieza_nombres(self):
        #lis_jpg_tif=[]
        lis_jpg=[]
        for nombres in self.lista:
                #hacemos filtro de la lista
                #if not in funciona como: Si no esta en la lista
                #El split(".") divide la palabra en el punto y toma desde la parte de atras
                # por el -1
                if nombres.split(".")[-1].upper() in ["jpg","JPG"]:
                    lis_jpg.append(nombres)

        self.lis_jpg=lis_jpg #Lista con los nombrs de todos los archivos jpg y tif
        self.var=0
            #archivos=os.listdir(path) #Lee todos los archivos pero no hace confimarción 
            #print(archivos)           
            #return archivos

        #print(self.lis_jpg)
    def des_derecha(self):
        self.var+=1
        if self.var==len(self.lis_jpg):
            self.var=0
        self.img = cv2.imread(self.path_carpet+'/'+self.lis_jpg[self.var]) # leeamos la imagen inicial de fondo : 
        self.img=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        """ print(self.img.shape[1])
        print(self.img.shape[0])
        print(self.img.shape) """
        self.img=cv2.resize(self.img,dsize=(self.img.shape[1]*2,self.img.shape[0]*2), interpolation=cv2.INTER_LINEAR)
        #cv2.imshow("comparación",self.img)
        self.img = Image.fromarray(self.img)
        self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.display1.imgtk = self.imgtk #Mostramos imagen sin procesar en el display 1(izquierda)
        self.display1.configure(image=self.imgtk)

        
        

    def des_izquierda(self):
        self.var-=1
        if self.var==-1:
            self.var=len(self.lis_jpg)
        self.img = cv2.imread(self.path_carpet+'/'+self.lis_jpg[self.var]) # leeamos la imagen inicial de fondo : 
        self.img=cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        """ print(self.img.shape[1])
        print(self.img.shape[0])
        print(self.img.shape) """
        self.img=cv2.resize(self.img,dsize=(self.img.shape[1]*2,self.img.shape[0]*2), interpolation=cv2.INTER_LINEAR)
        #cv2.imshow("comparación",self.img)
        self.img = Image.fromarray(self.img)
        self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.display1.imgtk = self.imgtk #Mostramos imagen sin procesar en el display 1(izquierda)
        self.display1.configure(image=self.imgtk)

        
        

    def save_carp1(self):
        paths='./anomalia/'
        shutil.move(self.path_carpet+'/'+self.lis_jpg[self.var],paths+self.lis_jpg[self.var])
        self.actualizar_listajpg()
        pass
    def save_carp2(self):
        paths='./no_anomalia/'
        shutil.move(self.path_carpet+'/'+self.lis_jpg[self.var],paths+self.lis_jpg[self.var])
        self.actualizar_listajpg()
        pass
    def save_carp3(self):
        paths='./extra/'
        shutil.move(self.path_carpet+'/'+self.lis_jpg[self.var],paths+self.lis_jpg[self.var])
        self.actualizar_listajpg() 
        pass
    def actualizar_listajpg(self):
        self.path_carpet=os.path.dirname(self.archivo_abierto)
        self.lista=os.listdir(os.path.dirname(self.path_carpet+'/'))
        self.limpieza_nombres()
        self.actualizar()

        pass

if __name__=="__main__":

    window=Tk()
    mywin=MyWindow(window)
    window.title('Guide clas_img')
    window.geometry("1180x670+10+10")
    window.minsize(700,500)
    window.maxsize(700,500)
    window.mainloop()
