from tkinter import Tk, Button, Label
from bs4 import BeautifulSoup
import random
import requests

#Clase que representa un chiste
class Chiste:
    def __init__(self, titulo, chiste):
        self.titulo = titulo
        self.chiste = chiste

#Diferentes categorías que después se concatenan en la URL para extraer todos los chistes de cada una de ellas
categorias = ('abogados', 'animales', 'borrachos', 'chinos', 'feministas', 'feos', 'gordos', 'humor-negro', 'matematicos', 'medicos', 'navidad', 'ninos', 'novios', 'pepito', 'politicos', 'preguntas-respuestas', 'suegras', 'toc-toc', 'tontos', 'verdes')

url = 'https://feti-chistes.es/chistes'

chistes = []
num_pagina = 1

#recorre todas las categorías disponibles en el sitio web y scrappea todos los chistes de cada una y lo mete en la lista 'chistes'
for categoria in categorias:

    #la primer página no figura como 'https://feti-chistes.es/chistes/categoria/pag/1' por lo que ahorramos la parte de '/pag/1'
    request = requests.get(f'{url}/{categoria}')

    #ahora recorremos todas las páginas posibles de la categoría actual
    #el ciclo finaliza cuando no se encontró un resultado (la página no existe, error 404)
    while request.status_code != 404:
        num_pagina+=1

        fuente = request.text
        soup = BeautifulSoup(fuente, 'lxml')
        articulos = soup.find_all('article', class_='card')

        for articulo in articulos:
            titulo_chiste = articulo.header.h2.a.text
            chiste = articulo.div.text

            #crea un objeto Chiste y lo inserta en la lista 'chistes'
            chistes.append(Chiste(titulo_chiste, chiste))
        
        request = requests.get(f'{url}/{categoria}/pag/{num_pagina}')
    
    num_pagina = 1
    print(f"Chistes de la categoría '{categoria}' agregados.", end='\n')
    
cantidad_chistes = len(chistes)
print(f'Cantidad de chistes: {cantidad_chistes}')

def get_chiste_random():
    return random.choice(chistes)

class VentanaChiste():

    def __init__(self):
        self.root = Tk()

        self.set_chiste()
        self.crear_boton()

        self.root.mainloop()

    def nuevo_chiste(self):
        self.root.destroy()
        VentanaChiste()      

    def set_chiste(self):
        chiste = get_chiste_random()
        self.root.title(chiste.titulo)
        label = Label(self.root, text=chiste.chiste)
        label.grid(row=0)
    
    def crear_boton(self):
        button = Button(self.root, text='Otro chiste', command=self.nuevo_chiste)
        button.grid(row=1)

VentanaChiste()
