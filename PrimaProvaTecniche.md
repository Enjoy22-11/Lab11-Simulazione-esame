Richieste: 

PUNTO	1	

a. L’utente seleziona dal corrispondente 

menù a tendina un genere musicale 

(tabella Genre). 

b. Premendo il pulsante “Crea grafo”, 

l’applicazione 

costruisce 

**un grafo** 

**orientato e pesato che rappresenta le** 

**relazioni di preferenza tra artisti. I vertici** 

**sono gli artisti (Artist) che possiedono** 

**almeno un brano (Track) appartenente** 

**al genere selezionato. Esiste un arco tra l’artista A e l’artista B se almeno un cliente ha acquistato brani di** 

**entrambi gli artisti**, **con verso da A verso B se la popolarità di A è maggiore della popolarità di B.** In caso i 

nodi A e B abbiano la stessa popolarità, aggiungere due archi in entrambi i versi. **Si calcoli la popolarità di un** 

**artista come la somma di tutti i brani acquistati di quell’artista.** Usare le tabelle invoceline e invoce per 

determinare gli acquisti dei clienti. **Il peso dell’arco tra l’artista A e l’artista B è la somma delle rispettive** 

**popolarità.** 

c. Costruito il grafo, l’applicazione visualizza **il numero di vertici e archi e l’artista con maggiore influenza.** 

**L’influenza di un artista è calcolata come: peso archi uscenti − peso archi entranti.** Inoltre, si visualizzino i 5 

archi con peso maggiore, in ordine decrescente. 















# **DAO**

from database.DB\_connect import DBConnect

from model.cantante import cantante





class DAO():

&#x20;   def \_\_init\_\_(self):

&#x20;       pass



###### **#cerco i generi musicali, no parametri**

&#x20;   @staticmethod

&#x20;   def getGenereMusicale():

&#x20;       conn =DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select name, genreId

&#x20;                  from genre"""

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           result.append(row\["name"])

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



###### **#ottengo gli artisti, con parametro (genere)**

&#x20;   @staticmethod

&#x20;   def getMusician(nomeGenere):

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select distinct a2.Name, a2.ArtistId

&#x20;                  from track as t, genre as g, album as a, artist as a2

&#x20;                  where g.GenreId = t.GenreId and t.AlbumId=a.AlbumId and a.ArtistId = a2.ArtistId

&#x20;                  and g.Name = %s"""

&#x20;       cursor.execute(query,(nomeGenere,))

&#x20;       for row in cursor:

&#x20;           result.append(cantante(\*\*row))

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



###### **#Metto la base per gli archi, no paramteri (ATTENZIONE USO DI DIZIONARIO associazione di valore a lista)**

&#x20;   @staticmethod

&#x20;   def getBaseArchi():

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = {}

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select distinct i2.CustomerId, a.ArtistId

&#x20;                  from invoiceline as i1, invoice as i2, track as t, album as a

&#x20;                  where i2.InvoiceId = i1.InvoiceId and i1.TrackId = t.TrackId and a.AlbumId = t.AlbumId """

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           idCostumer = row\["CustomerId"]

&#x20;           idArtist = row\["ArtistId"]

&#x20;           if idCostumer not in result:

&#x20;               result\[idCostumer] = \[]

&#x20;           result\[idCostumer].append(idArtist)

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



###### **#Metto la base per i pesi, no paramteri (ATTENZIONE USO DI DIZIONARIO)**



&#x20;   @staticmethod

&#x20;   def getPopolarita():

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = {}

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select a.ArtistId, count(a.ArtistId ) as popolarita

&#x20;                  from invoiceline as i1, track as t, album as a

&#x20;                  where a.AlbumId  = t.AlbumId and t.TrackId = i1.TrackId

&#x20;                  group by a.ArtistId"""

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           idArtist = row\["ArtistId"]

&#x20;           popolarita = row\["popolarita"]

&#x20;           result\[idArtist]=popolarita

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result





































































# \#Cantante

from dataclasses import dataclass



###### **#dataclass**

@dataclass

class cantante:

&#x20;   ArtistId: int

&#x20;   Name: str



###### **#da mettere sempre dataclass**

&#x20;   def \_\_hash\_\_(self):

&#x20;       return hash(self.ArtistId)

&#x20;   def \_\_eq\_\_(self, other):

&#x20;       return self.ArtistId == other.ArtistId

&#x20;   def \_\_str\_\_(self):

&#x20;       return f"Nome: {self.Name}, IdArtista: {self.ArtistId}"



&#x20;   def getName(self):

&#x20;       return self.Name

&#x20;   def getIdArtista(self):

&#x20;       return self.ArtistId











































































# **#Test model**

from model.model import Model

myModel = Model()

myModel.creaGrafo("Metal")

Nnodes = myModel.getNumeroNodi()

print(f"numero dei nodi pari a: {Nnodes}")







































# **Model**



###### **#da importare sempre**

import networkx as nx

from database.DAO import DAO





class Model:

&#x20;   def \_\_init\_\_(self):

###### **#da inserire sempre nell'init**

&#x20;       self.grafo = nx.DiGraph()

&#x20;       self.idMap = {}

&#x20;       self.mappaArtista\_influenza = {}

**#passo i generi**

&#x20;   def getallgenre(self):

&#x20;       return DAO.getGenereMusicale()





&#x20;   def creaGrafo(self,nomeGenere):

###### **#nel metodo per generare i nodi ricordarsi sempre di pulire mappa e grafo all'inzio**

&#x20;       self.grafo.clear()

&#x20;       self.idMap.clear()



&#x20;       cantantiDatoGenere = DAO.getMusician(nomeGenere)

&#x20;       mappa\_popolarita = DAO.getPopolarita()



&#x20;       self.grafo.add\_nodes\_from(cantantiDatoGenere)

&#x20;       for c in cantantiDatoGenere:

&#x20;           self.idMap\[c.ArtistId] = c



###### **#Quei due for i... e for j in range(i+1... servono a creare tutte le coppie possibili senza ripetizioni.**

&#x20;       clienti\_e\_Artisti = DAO.getBaseArchi()

&#x20;       for cliente, listaArtisti in clienti\_e\_Artisti.items():

&#x20;           for i in range(len(listaArtisti)):

&#x20;               for j in range(i+1,len(listaArtisti)):

&#x20;                   id\_a1 = listaArtisti\[i]

&#x20;                   id\_a2 = listaArtisti\[j]

&#x20;                   if id\_a1 in self.idMap and id\_a2 in self.idMap:

&#x20;                       nodo1= self.idMap\[id\_a1]

&#x20;                       nodo2 = self.idMap\[id\_a2]

&#x20;                       **#inserisco anche le popolarita in due variabili**

&#x20;                       popolarita1 = mappa\_popolarita.get(id\_a1,0)                             # il ,0 serve a mettere popolarita nulla se non c'è

&#x20;                       popolarita2 = mappa\_popolarita.get(id\_a2,0)

&#x20;                       peso\_arco = popolarita1 + popolarita2                                   #dato dalla somma delle popolarita



###### **#archi pesati**

&#x20;                       if popolarita1 > popolarita2:

&#x20;                           self.grafo.add\_edge(nodo1, nodo2, weight = peso\_arco)

&#x20;                       elif popolarita1 < popolarita2:

&#x20;                           self.grafo.add\_edge(nodo2, nodo1, weight = peso\_arco)

&#x20;                       #else:

&#x20;                         #   self.grafo.add\_edge(nodo1, nodo2, weight = peso\_arco)

&#x20;                         #  self.grafo.add\_edge(nodo2, nodo1, weight = peso\_arco)









##### **#numero Nodi e archi**

&#x20;   def getNumeroNodi(self):

&#x20;       return len(self.grafo.nodes())

&#x20;   def getNumeroArchi(self):

&#x20;       return len(self.grafo.edges())



###### **#Artista con maggiore influenza   (nodi entranti e uscenti)**

&#x20;   def getArtistaMaggioreInfluenza(self):

&#x20;       **self.mappaArtista\_influenza.clear(**)

&#x20;       for artist in self.grafo.nodes():

&#x20;           self.mappaArtista\_influenza\[artist] = (

###### &#x20;                   self.grafo.out\_degree(artist, weight="weight")         **#archi uscenti**

###### &#x20;                   - self.grafo.in\_degree(artist, weight="weight"))       **#archi entranti**



###### &#x20;       piuPopolare =sorted(self.mappaArtista\_influenza, key= self.mappaArtista\_influenza.get, reverse = True)\[0]      **#ordino e prendo quello piu popolare**

&#x20;       return piuPopolare





##### **#top five archi (dal più grande al più piccolo)**

&#x20;   def getTopFive(self):

&#x20;       #prendo tutti gli archi

&#x20;       tuttiGliArchi = self.grafo.edges(data=True)

&#x20;       archiInOrdine = sorted(tuttiGliArchi, key= lambda x: x\[2]\["weight"], reverse=True)

&#x20;       return archiInOrdine\[:5]











# **controller**

import flet as ft





class Controller:

&#x20;   def \_\_init\_\_(self, view, model):

&#x20;       # the view, with the graphical elements of the UI

&#x20;       self.\_view = view

&#x20;       # the model, which implements the logic of the program and holds the data

&#x20;       self.\_model = model



**#inseriamo i generi nel dropdown**

#### &#x20;   def fillDDGenre(self):

&#x20;       genres = self.\_model.getallgenre()

&#x20;       genreDD = \[]

&#x20;       for g in genres:

&#x20;           genreDD.append(ft.dropdown.Option(g))

&#x20;       self.\_view.\_ddGenre.options= genreDD

&#x20;       self.\_view.update\_page()





#### &#x20;   def handleCreaGrafo(self, e):

###### **#prendo il valore del dropdown**

&#x20;       genereSelezionato = self.\_view.\_ddGenre.value

###### **#verifico non sia nullo**

&#x20;       if genereSelezionato is None:

&#x20;           self.\_view.txt\_result.controls.append(ft.Text("Selezionare un genere"))

&#x20;           self.\_view.update\_page()

&#x20;           return

###### **#creo il grafo mandando in input il genere selezionato**

&#x20;       self.\_model.creaGrafo(genereSelezionato)

###### **#prendo i valori dei nodi e degli archi**

&#x20;       numeroDiNodi = self.\_model.getNumeroNodi()

&#x20;       numeroDiArchi = self.\_model.getNumeroArchi()



**#artista con maggiore influenza**

&#x20;       artistaConMaggioreInfluenza = self.\_model.getArtistaMaggioreInfluenza()



**#archi top five**

&#x20;       architopfive = self.\_model.getTopFive()





###### **#prima di inserire valori ricordarsi di pulire il drodown**

&#x20;       self.\_view.txt\_result.controls.clear()



&#x20;       self.\_view.txt\_result.controls.append(ft.Text("Grafo creato correttamente"))

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))                  #stampo numero di nodi

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))                #stampo numero di archi



&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"l'artista con più influenza è:{artistaConMaggioreInfluenza.getName()}"))   #stampo artista con maggiore influenza

&#x20;       

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"gli artisti più influenti sono:"))                    #stampo artisti piu influenti

&#x20;       for arco in architopfive:

&#x20;           nome1 = arco\[0].getName()                      #primo nodo

&#x20;           nome2 = arco\[1].getName()                      #secondo nodo                     

&#x20;           peso = arco\[2]\["weight"]                       #peso



&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))   #stampo



&#x20;       **self.\_view.update\_page()**





&#x20;   def handleCammino(self,e):

&#x20;       pass















wiew

import flet as ft





class View(ft.UserControl):

&#x20;   def \_\_init\_\_(self, page: ft.Page):

&#x20;       super().\_\_init\_\_()

&#x20;       # page stuff

&#x20;       self.\_page = page

&#x20;       self.\_page.title = "Lab11-Simulazione esame"

&#x20;       self.\_page.horizontal\_alignment = 'CENTER'

&#x20;       self.\_page.theme\_mode = ft.ThemeMode.LIGHT

&#x20;       # controller (it is not initialized. Must be initialized in the main, after the controller is created)

&#x20;       self.\_controller = None

&#x20;       # graphical elements

&#x20;       self.\_title = None

&#x20;       self.txt\_name = None

&#x20;       self.btn\_hello = None

&#x20;       self.txt\_result = None

&#x20;       self.txt\_container = None



&#x20;   def load\_interface(self):

&#x20;       # title

&#x20;       self.\_title = ft.Text("TdP-Simulazione esame Chinook", color="blue", size=24)

&#x20;       self.\_page.controls.append(self.\_title)





&#x20;       self.\_ddGenre = ft.Dropdown(label="Genere")

&#x20;       self.\_controller.fillDDGenre()

&#x20;       self.\_btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on\_click=self.\_controller.handleCreaGrafo)



&#x20;       row1 = ft.Row(\[self.\_ddGenre, self.\_btnCreaGrafo],

&#x20;                     alignment=ft.MainAxisAlignment.CENTER)

&#x20;       self.\_page.controls.append(row1)



&#x20;       self.\_ddArtist = ft.Dropdown(label="Artist")

&#x20;       self.\_btnCreaGrafo = ft.ElevatedButton(text="Trova Cammino", on\_click=self.\_controller.handleCammino)



&#x20;       row2 = ft.Row(\[self.\_ddArtist, self.\_btnCreaGrafo],

&#x20;                     alignment=ft.MainAxisAlignment.CENTER)

&#x20;       self.\_page.controls.append(row2)



&#x20;       # List View where the reply is printed

&#x20;       self.txt\_result = ft.ListView(expand=1, spacing=10, padding=20, auto\_scroll=True)

&#x20;       self.\_page.controls.append(self.txt\_result)

&#x20;       self.\_page.update()



&#x20;   @property

&#x20;   def controller(self):

&#x20;       return self.\_controller



&#x20;   @controller.setter

&#x20;   def controller(self, controller):

&#x20;       self.\_controller = controller



&#x20;   def set\_controller(self, controller):

&#x20;       self.\_controller = controller



&#x20;   def create\_alert(self, message):

&#x20;       dlg = ft.AlertDialog(title=ft.Text(message))

&#x20;       self.\_page.dialog = dlg

&#x20;       dlg.open = True

&#x20;       self.\_page.update()



&#x20;   def update\_page(self):

&#x20;       self.\_page.update()

































