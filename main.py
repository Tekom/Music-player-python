from tkinter import *
from tkinter import filedialog
from PIL import Image
import io
import os
from tinytag import TinyTag, TinyTagException
import shutil
import pygame
import time
import binascii
import numpy as np
import scipy.cluster

pygame.init()
pygame.mixer.init()

ventana_reproductor = Tk()
accion = 0
contador_siguiente_cancion = 0
contador_anterior_cancion = 0
song1 = True
img_2 = PhotoImage(file='tocar2.png')
img_3 = PhotoImage(file='next_button.png')
img_4 = PhotoImage(file='back_button.png')

canvas = Canvas(ventana_reproductor)
canvas.place(x=340, y=30)
barra = Scrollbar(canvas, orient=VERTICAL)
barra.pack(side=RIGHT, fill=Y)
lista_canciones = Listbox(canvas, width=40, height=10, bg='gray96')
lista_canciones.pack()
lista_canciones.configure(yscrollcommand=barra.set)
barra.configure(command=lista_canciones.yview)
buscar_cancion = Entry(ventana_reproductor, width=40, text='Buscar')
buscar_cancion.place(x=340, y=10)
valor_barra = DoubleVar()


def PrimeraCancion(path2):
    global panel, img, barra_progresion
    path_primera_cacion = path2
    tag = TinyTag.get("{}/{}".format(path_primera_cacion, canciones[0]), image=True)
    image_data = tag.get_image()
    cover = Image.open(io.BytesIO(image_data))
    cover = cover.resize((100, 100))
    cover.save('cover.png')
    barra_progresion.place(x=130, y=70)
    img = PhotoImage(file='cover.png')
    panel = Label(ventana_reproductor, image=img, background='#6c2656',highlightthickness=0,bd=0)
    panel.place(x=10, y=10)


ventana_reproductor.geometry('600x220')


def ObtenerPath():
    directorio = filedialog.askdirectory()
    pygame.mixer.music.unload()
    global primera_cancion, accion
    accion = 0
    primera_cancion = True
    if (directorio != ""):
        os.chdir(directorio)
    global path2, nombre_artista, nombre_album, nombre_cancion, canciones
    path2 = os.getcwd()

    canciones = []
    dir = os.walk(path2)
    # asd = 0
    for root, dirs, files in dir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if extension == ".mp3" or extension == ".wav":
                canciones.append(nombreFichero + extension)
                # shutil.copy("{}/{}".format(root,canciones[asd]),"C:/Users/pipea/Desktop/Music3")
                # subprocess.call('move ' + canciones[asd] + ' ' + "C:/Users/pipea/Desktop/Music3", shell=True)
                # print('asd')
                # asd = asd + 1

    PrimeraCancion(path2)

    tag_primera_cancion = TinyTag.get("{}/{}".format(path2, canciones[0]))
    nombre_artista = Label(ventana_reproductor, text="Artista: " + tag_primera_cancion.artist,fg='white')
    nombre_album = Label(ventana_reproductor, text="Album: " + tag_primera_cancion.album,fg='white')
    nombre_cancion = Label(ventana_reproductor, text="Nombre: " + tag_primera_cancion.title,fg='white')
    nombre_artista.place(x=10, y=160)
    nombre_album.place(x=10, y=140)
    nombre_cancion.place(x=10, y=120)

    MostrarCancionesEnLista()

def MostrarCancionesEnLista():
    global busqueda
    busqueda = []
    if len(canciones) > 0 and buscar_cancion.get() == "":
        lista_canciones.delete(0, END)
        busqueda.clear()
        for i in range(len(canciones)):
            song = TinyTag.get("{}/{}".format(path2, canciones[i]))
            lista_canciones.insert(END, "{}- {}".format(i, song.title))
    else:
        lista_canciones.delete(0, END)
        for i in range(len(canciones)):
            if buscar_cancion.get() in canciones[i]:
                busqueda.append(canciones[i])
        for i in range(len(busqueda)):
            song = TinyTag.get("{}/{}".format(path2, busqueda[i]))
            lista_canciones.insert(END, "{}- {}".format(i, song.title))
        print(busqueda)


def Etiquetas(path):
    tag = TinyTag.get(path, image=True)
    nombre_artista.configure(text="Artista: " + tag.artist)
    nombre_album.configure(text="Album: " + tag.album)
    nombre_cancion.configure(text="Nombre: " + tag.title)

def ColorPredominante():
    NUM_CLUSTERS = 5

    print('reading image')
    im = Image.open('cover.png')
    im = im.resize((150, 150))
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))

    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    peak2 = []
    for i in range(3):
        peak2.append(255-peak[i])

    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    colour2 = binascii.hexlify(bytearray(int(a) for a in peak2)).decode('ascii')
    print('most frequent is %s (#%s)' % (peak, colour))

    ventana_reproductor.configure(background='#'+colour)
    nombre_cancion.configure(background='#'+colour,fg='#'+colour2)
    nombre_artista.configure(background='#'+colour,fg='#'+colour2)
    nombre_album.configure(background='#'+colour,fg='#'+colour2)
    lista_canciones.configure(background='#'+colour,fg='#'+colour2)
    boton_anterior_cancion.configure(background='#'+colour,relief=SUNKEN, bd=0)
    boton_siguiente_cancion.configure(background='#'+colour,relief=SUNKEN, bd=0)
    boton_empezar_cacion.configure(background='#'+colour,relief=SUNKEN, bd=0)
    boton_seleccionar_directorio.configure(background='#'+colour2)
    barra_progresion.configure(background='#'+colour,bd=0,fg='#'+colour2,highlightthickness=0,troughcolor='#'+colour2)

def Cover(path):
    global img
    tag_3 = TinyTag.get(path, image=True)
    image_data = tag_3.get_image()
    cover = Image.open(io.BytesIO(image_data))
    cover = cover.resize((100, 100))
    cover.save('cover.png')
    img = PhotoImage(file='cover.png')
    panel.config(image=img)
    ColorPredominante()


def CargarCancion(path):
    global path_cancion
    path_cancion = path
    pygame.mixer.music.load(path_cancion)
    print(path_cancion)


def AdelantarAtrasarCancion(event):
    global primera_cancion
    if primera_cancion:
        print('hola')
        path_adelantar_atrasar_cancion = TinyTag.get("{}/{}".format(path2, canciones[0]), image=True)
        barra_progresion.configure(to=path_adelantar_atrasar_cancion.duration)
        pygame.mixer.music.set_pos(barra_progresion.get())
    else:
        path_adelantar_atrasar_cancion = TinyTag.get(path_cancion, image=True)
        barra_progresion.configure(to=path_adelantar_atrasar_cancion.duration)
        time.sleep(0.15)
        pygame.mixer.music.set_pos(barra_progresion.get())

barra_progresion = Scale(ventana_reproductor,variable=valor_barra, from_=0, to=100,
                             orient=HORIZONTAL,command=AdelantarAtrasarCancion,length=200)

def SeleccionarCancion():
    global accion, primera_cancion, song1
    accion = accion + 1
    if primera_cancion:
        pygame.mixer.music.load("{}/{}".format(path2, canciones[0]))
        Etiquetas("{}/{}".format(path2, canciones[0]))
        lista_canciones.select_set(0)
        song1 = True
        primera_cancion = False
    if (accion == 1):
        pygame.mixer.music.play(1)
    if (accion == 2):
        pygame.mixer.music.pause()
    if (accion == 3):
        pygame.mixer.music.unpause()
        accion = 1


def SiguienCancion():
    global contador_siguiente_cancion, accion, contador_anterior_cancion, song1
    if song1:
        lista_canciones.select_clear(0)
        song1 = False
    accion = 1
    contador_siguiente_cancion = contador_siguiente_cancion + 1
    lista_canciones.select_clear(contador_siguiente_cancion - 1)
    lista_canciones.select_set(contador_siguiente_cancion)
    contador_anterior_cancion = contador_siguiente_cancion
    path = "{}/{}".format(path2, canciones[contador_siguiente_cancion])
    pygame.mixer.music.unload()
    CargarCancion(path)
    pygame.mixer.music.play(1)
    Cover(path)
    Etiquetas(path)
    barra_progresion.set(0)

def CancionAnterior():
    global contador_anterior_cancion, accion, contador_siguiente_cancion, song1
    if song1:
        lista_canciones.select_clear(0)
        song1 = False
    accion = 1
    contador_anterior_cancion = contador_anterior_cancion - 1
    lista_canciones.select_clear(contador_anterior_cancion + 1)
    lista_canciones.select_set(contador_anterior_cancion)
    contador_siguiente_cancion = contador_anterior_cancion
    path = "{}/{}".format(path2, canciones[contador_anterior_cancion])
    pygame.mixer.music.unload()
    CargarCancion(path)
    pygame.mixer.music.play(1)
    Cover(path)
    Etiquetas(path)
    barra_progresion.set(0)

boton_empezar_cacion = Button(ventana_reproductor, image=img_2, height=50, width=50, text='Seleccionar Musica',
                              command=SeleccionarCancion)
boton_siguiente_cancion = Button(ventana_reproductor, image=img_3, height=50, width=50, text='Seleccionar Musica',
                                 command=SiguienCancion)
boton_anterior_cancion = Button(ventana_reproductor, image=img_4, height=50, width=50, text='Seleccionar Musica',
                                command=CancionAnterior)
boton_seleccionar_directorio = Button(ventana_reproductor, width=26, text='Seleccionar directorio', command=ObtenerPath)

boton_empezar_cacion.place(x=200, y=10)
boton_siguiente_cancion.place(x=270, y=10)
boton_anterior_cancion.place(x=130, y=10)
boton_seleccionar_directorio.place(x=10, y=190)


def DobleClick(event):
    global primera_cancion, contador_siguiente_cancion, contador_anterior_cancion
    barra_progresion.set(0)
    cs = lista_canciones.curselection()
    pygame.mixer.music.unload()
    print(cs[0])
    guardar_i = 0

    if busqueda:
        for i in range(len(canciones)):
            if busqueda[cs[0]] in canciones[i]:
                guardar_i = i

        contador_siguiente_cancion = guardar_i
        contador_anterior_cancion = guardar_i
        path_doble_click = "{}/{}".format(path2, canciones[guardar_i])
    else:
        contador_siguiente_cancion = cs[0]
        contador_anterior_cancion = cs[0]
        path_doble_click = "{}/{}".format(path2, canciones[cs[0]])

    CargarCancion(path_doble_click)
    primera_cancion = False
    pygame.mixer.music.play(1)
    Cover(path_doble_click)
    Etiquetas(path_doble_click)


def BuscarCancion(event):
    MostrarCancionesEnLista()


buscar_cancion.bind('<Return>', BuscarCancion)
lista_canciones.bind('<Double-1>', DobleClick)
ventana_reproductor.mainloop()

