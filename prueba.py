from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os
import customtkinter
import customtkinter as ctk
from tkinter import simpledialog
from tkinter.simpledialog import askstring
from tkinter import messagebox
from PIL import Image, ImageDraw
from PIL import ImageGrab


customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()
root.title("AllBoard")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.config(bg="#0D1119")
root.state("zoomed")
root.resizable(False, False)

cursor_x = 0
cursor_y = 0
color = "black"
image_filename = ""
selected_item = None
image_objects = []


def locate_xy(work):
    global cursor_x, cursor_y
    cursor_x = work.x
    cursor_y = work.y


def addline(work):
    global cursor_x, cursor_y, color
    lienso.create_line((cursor_x, cursor_y, work.x, work.y), width=get_current_value(), fill=color,
                       capstyle=tk.ROUND, smooth=True)
    cursor_x, cursor_y = work.x, work.y


def HerramientaBorra():
    global color
    new_color = "#F3F9FF"
    if new_color:
        color = new_color


def borrar_canvas():
    lienso.delete("all")


def guardar_archivo():
    try:
        filename = filedialog.asksaveasfilename(defaultextension='.png',
                                                  filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

        x = lienso.winfo_rootx()
        y = lienso.winfo_rooty()
        width = lienso.winfo_width()
        height = lienso.winfo_height()

        captured_image = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        captured_image.save(filename, format="PNG")

        messagebox.showinfo("Guardado", "La imagen ha sido guardada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la imagen. Error: {e}")

def importaimagenes():
    global filename, f_img, image_objects, cursor_x, cursor_y
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona una imagen",
                                          filetypes=(("PNG file", "*.png"), ("All files", "*.*")))
    f_img = tk.PhotoImage(file=filename)
    image_object = lienso.create_image(cursor_x, cursor_y, image=f_img, tags="user_image")
    lienso.tag_bind(image_object, '<ButtonPress-3>', lambda event, img=image_object: select_element(event, img))
    lienso.tag_bind(image_object, '<B3-Motion>', lambda event, img=image_object: move_image(event, img))
    image_objects.append(image_object)



def on_image_drag(event, img):
    global cursor_x, cursor_y
    x, y = event.x, event.y
    dx, dy = x - cursor_x, y - cursor_y
    lienso.move(img, dx, dy)
    cursor_x, cursor_y = x, y


def selecolor():
    global color
    new_color = colorchooser.askcolor()[1]
    if new_color:
        color = new_color


# barra
borrar = customtkinter.CTkButton(root, text="Borrar", command=HerramientaBorra, width=130, height=75, font=("Arial", 20))
borrar.place(x=1, y=400)

image1 = PhotoImage(file="goma.png")
label1 = ctk.CTkLabel(root, image=image1, text="", bg_color="#0D1119")
label1.place(x=140, y=405)

importaimg = customtkinter.CTkButton(root, text="Agrega imagenes", command=importaimagenes, width=150, height=75,
                                     font=("Arial", 20))
importaimg.place(x=15, y=250)

botoncolor = customtkinter.CTkButton(root, text="Color", command=selecolor, width=130, height=75, font=("Arial", 20))
botoncolor.place(x=1, y=520)

image2 = PhotoImage(file="lapiz.png")
label2 = ctk.CTkLabel(root, image=image2, text="", bg_color="#0D1119")
label2.place(x=140, y=517)


def agregar_texto():
    texto_ingresado = simpledialog.askstring("ㅤ", "Ingresa el texto:")
    if texto_ingresado:
        text_item = lienso.create_text(cursor_x, cursor_y, text=texto_ingresado, fill='black',
                                       font=("Arial", 20), tags="user_text")
        lienso.tag_bind(text_item, '<ButtonPress-3>', lambda event, txt=text_item: select_element(event, txt))
        lienso.tag_bind(text_item, '<B3-Motion>', move_text)


def move_image(event, img):
    global cursor_x, cursor_y
    x, y = event.x, event.y
    dx, dy = x - cursor_x, y - cursor_y
    lienso.move(img, dx, dy)
    cursor_x, cursor_y = x, y


def move_text(event):
    global selected_item
    try:
        lienso.coords(selected_item, event.x, event.y)
    except NameError:
        pass


def select_element(event, item):
    global selected_item
    selected_item = item


agregartexto = customtkinter.CTkButton(root, text="Texto", command=agregar_texto, width=150, height=75,
                                       font=("Arial", 20))
agregartexto.place(x=21, y=85)

block = customtkinter.CTkCanvas(root, width=215, height=150, background="#F2F6FF")
block.place(x=0, y=655)

agregartexto = customtkinter.CTkButton(root, text="Texto", command=agregar_texto, width=150, height=75,
                                       font=("Arial", 20))
agregartexto.place(x=21, y=85)


# pantalla principal
lienso = customtkinter.CTkCanvas(root, width=1145, height=800, background="#F3F9FF", cursor="hand2")
lienso.place(x=220, y=0)

lienso.bind('<Button-1>', locate_xy)
lienso.bind('<B1-Motion>', addline)

# menu superior
menu_top = tk.Frame(root, background='#070A0F')
menu_top.pack(side='top', fill='x')
archivo = tk.Menubutton(menu_top, text='Archivo', background='black', foreground='white', activeforeground='black',
                        activebackground='gray52')

# desplegable
menu_archivo = tk.Menu(archivo, tearoff=0)
menu_archivo.add_command(label='nuevo', command=borrar_canvas, background='black', foreground='white',
                         activeforeground='black', activebackground='gray52')
menu_archivo.add_command(label='guardar',command=guardar_archivo,background='black',foreground='white',activeforeground='black',activebackground='gray52')


archivo.config(menu=menu_archivo)
archivo.pack(side='left')

# funcion grosor

current_value = ctk.DoubleVar()


def get_current_value():
    return '{: .2f}'.format(current_value.get())


def slider_changed(event):
    valor_label.configure(text=get_current_value())


grosor = ttk.Scale(root, from_=0, to=50, orient="horizontal", command=slider_changed, variable=current_value, style="TScale")
grosor.place(x=45, y=695)

valor_label = ttk.Label(root, text=get_current_value())

root.mainloop()