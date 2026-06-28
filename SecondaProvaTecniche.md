Richieste: 

PUNTO 1

a. L'utente seleziona dal corrispondente menù a tendina un tipo di formato multimediale (MediaType, dalla tabella MediaType).



b. Premendo il pulsante "Crea Grafo", l'applicazione costruisce un grafo **NON orientato e pesato** che rappresenta le associazioni di acquisto tra i brani musicali.



**I vertici: Sono le tracce (Track)** **che appartengono al formato multimediale selezionato dall'utente**. N.B. Si consideri come campo del nodo Traccia anche la sua dimensione in Megabyte (calcolata a partire dal campo Bytes. Hint: 1 MB = 1.048.576 Bytes. Controllare che il campo Bytes sia valido, ovvero strettamente maggiore di 0, prima di inserire la traccia nel grafo).



**Gli archi: Esiste un arco tra due tracce se sono state acquistate insieme in almeno una stessa Fattura** (tabella Invoice, collegata tramite InvoiceLine).



**Il peso: Il peso dell'arco è pari alla somma dei totali** (Total della tabella Invoice) di tutte le fatture in cui le due tracce compaiono insieme.









































# **DAO**

from database.DB\_connect import DBConnect

from model.Traccia import Traccia





class DAO():

&#x20;   def \_\_init\_\_(self):

&#x20;       pass



###### **#trovo tipi dei media, no parametri**

&#x20;   @staticmethod

&#x20;   def GetMediaTipo():

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select m.Name, m.MediaTypeId

&#x20;                  from mediatype as m """

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           result.append(row\["Name"])

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



###### **#trovo TracceId, tracceNomi e Byte, passo parametro (tipoFile)**

&#x20;   @staticmethod

&#x20;   def get\_track(tipo\_file):

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select t.TrackId, t.Name, t.Bytes 

&#x20;                  from mediatype as m, track as t

&#x20;                  where m.MediaTypeId = t.MediaTypeId and m.Name = %s """

&#x20;       cursor.execute(query,(tipo\_file,))

&#x20;       for row in cursor:

&#x20;           result.append(**Traccia**(\*\*row))

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result





###### **#trovo archi con il loro peso, no parametri (uso delle tuple top)**

&#x20;   @staticmethod

&#x20;   def getNodiePeso():

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select i1.TrackId as ID1, i2.TrackId as ID2, sum(i.Total) as Peso 

&#x20;                  from invoiceline as i1, invoiceline as i2, invoice as i

&#x20;                  where i1.InvoiceId = i2.InvoiceId 

&#x20;                  and i1.InvoiceId  = i.InvoiceId  

&#x20;                  and i1.TrackId < i2.TrackId

&#x20;                  group by i1.TrackId, i2.TrackId  """

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           result.append((row\["ID1"], row\["ID2"], row\["Peso"]))

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result





















































# **test model**

**from model.model import Model**

**myModel = Model()**

myModel.creaGrafo("MPEG audio file")

Nnodes = myModel.getNumeroNodi()

Narchi = myModel.getNumeroArchi()

print(f"numero dei nodi pari a: {Nnodes} e {Narchi} archi")













































# 

# **model**

###### **#da importare sempre**

import networkx as nx

from database.DAO import DAO





class Model:

###### **#da inserire sempre nell'init**

&#x20;   def \_\_init\_\_(self):

&#x20;       **self.grafo = nx.Graph()**

&#x20;       **self.idMap = {}**





&#x20;   def getallMediaType(self):                             **#solito metodo per passare al controller la lista**

&#x20;       return DAO.GetMediaTipo()





##### **#nel metodo per generare i nodi ricordarsi sempre di pulire mappa e grafo all'inzio**

###### &#x20;   def **creaGrafo**(self,tipoMedia):

&#x20;       self.grafo.clear()

&#x20;       self.idMap.clear()



\#prendo nodi e archi dal DAO

&#x20;       tracceDatoTipo = DAO.get\_track(tipoMedia)

&#x20;       allarchipesati = DAO.getNodiePeso()





\#verifico che i Byte siano positivi

&#x20;       for traccia in tracceDatoTipo:

&#x20;           tracciaMB = traccia.dammiMB()

&#x20;           if tracciaMB <= 0:

&#x20;               continue

&#x20;           else:

&#x20;               traccia.setMB(tracciaMB)

&#x20;               self.grafo.add\_node(traccia)



**#inserisco nella mappa**

&#x20;               self.idMap\[traccia.TrackId] = traccia



###### **#archi pesati**

&#x20;       for traccia1, traccia2, peso in allarchipesati:

&#x20;           if traccia1 in self.idMap and traccia2 in self.idMap:            **#verifico siano nella mappa**

&#x20;               nodo1 = self.idMap\[traccia1]

&#x20;               nodo2 = self.idMap\[traccia2]

&#x20;               pesoarco = peso

&#x20;               self.grafo.add\_edge(nodo1, nodo2, weight=pesoarco)           **#creo l'arco**







##### **#numero Nodi e archi**

&#x20;   def getNumeroNodi(self):

&#x20;       return len(self.grafo.nodes())

&#x20;   def getNumeroArchi(self):

&#x20;       return len(self.grafo.edges())





##### **#top five archi (dal più grande al più piccolo)**

&#x20;   #top 5 archi con peso maggiore

&#x20;   def getTopFive(self):

&#x20;       #prendo tutti gli archi

&#x20;       tuttiGliArchi = self.grafo.edges(data=True)

&#x20;       archiInOrdine = sorted(tuttiGliArchi, key= lambda x: x\[2]\["weight"], reverse=True)

&#x20;       return archiInOrdine\[:5]







##### **#componenti connesse (lunghezza e max/min)**

&#x20;   def getInfoComponenti(self):

&#x20;       # ATTENZIONE: connected\_components funziona SOLO su grafi NON orientati (nx.Graph)

&#x20;       # Trasformiamo i risultati in una lista di set Python

&#x20;       componenti = list(nx.connected\_components(self.grafo))



&#x20;       # Il numero totale di componenti connesse è la lunghezza della lista

&#x20;       num\_componenti = len(componenti)



&#x20;       # Per trovare la componente più grande, cerchiamo il set con più elementi (key=len)

&#x20;       comp\_maggiore = max(componenti, key=len) if componenti else \[]



&#x20;       return num\_componenti, comp\_maggiore



































# **traccia**

from dataclasses import dataclass



###### **#dataclass**

@dataclass

class Traccia:

&#x20;   TrackId : int

&#x20;   Name : str

&#x20;   Bytes : int



###### **#da mettere sempre dataclass**

&#x20;   def \_\_hash\_\_(self):

&#x20;       return hash(self.TrackId)

&#x20;   def \_\_eq\_\_(self, other):

&#x20;       return self.TrackId == other.TrackId

&#x20;   def \_\_str\_\_(self):

&#x20;       return f"Traccia: {self.Name}, Id: {self.TrackId} (Bytes: {self.Bytes})"





&#x20;   def dammiMB(self):

&#x20;       return int(self.Bytes/1048576)



&#x20;   def setMB(self, MB):

&#x20;       self.Bytes = MB



&#x20;   def getName(self):

&#x20;       return self.Name





































# **controller**

import flet as ft





#### class Controller:

&#x20;   def \_\_init\_\_(self, view, model):

&#x20;       # the view, with the graphical elements of the UI

&#x20;       self.\_view = view

&#x20;       # the model, which implements the logic of the program and holds the data

&#x20;       self.\_model = model



#### &#x20;   def fillDDGenre(self):

&#x20;       pass



###### **#inseriamo i tipi di media nel dropdown**

#### &#x20;   def fillDDmediaType(self):

&#x20;       mediaTipo = self.\_model.getallMediaType()

&#x20;       listamediatipo = \[]

&#x20;       for nometipo in mediaTipo:

&#x20;           listamediatipo.append(ft.dropdown.Option(nometipo))

&#x20;       self.\_view.\_ddGenre.options = listamediatipo

&#x20;       self.\_view.update\_page()





#### &#x20;   def handleCreaGrafo(self, e):

###### **#prendo il valore del dropdown**

&#x20;       tipoMedia = self.\_view.\_ddGenre.value

###### **#verifico non sia nullo**

&#x20;       if tipoMedia is None:

&#x20;           self.\_view.txt\_result.controls.append(ft.Text("Selezionare una tipologia di file multimediale"))

&#x20;           **self.\_view.update\_page()**

&#x20;           return





###### **#prendo i valori dei nodi e degli archi**

&#x20;       self.\_model.creaGrafo(tipoMedia)

&#x20;       numeroDiNodi = self.\_model.getNumeroNodi()

&#x20;       numeroDiArchi = self.\_model.getNumeroArchi()





###### **#prima di inserire valori ricordarsi di pulire il drodown**

&#x20;       self.\_view.txt\_result.controls.clear()



&#x20;       self.\_view.txt\_result.controls.append(ft.Text("Grafo creato correttamente"))

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))       **#stampo numero di Nodi**

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))     **#stampo numero di Archi**







###### **#stampo i 5 archi con peso maggiore**

&#x20;       architopfive = self.\_model.getTopFive()                                                     #prendo gli archi

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"I 5 archi con peso maggiore sono:"))

&#x20;       for arco in architopfive:

&#x20;           nome1 = arco\[0].getName()                                                               #primo nodo

&#x20;           nome2 = arco\[1].getName()                                                               #secondo nodo

&#x20;           peso = arco\[2]\["weight"]                                                                #peso



&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))   #stampo



&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f""))



###### **# per le componenti connesse del grafo**

&#x20;       numeroComponenti, componenteMaggiore = self.\_model.getInfoComponenti()                                        #prendo le componenti

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Le componenti connesse del grafo sono: {numeroComponenti}"))  #ne stampo il numero

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"La componente maggiore ha {len(componenteMaggiore)} nodi"))   #ne stampo il numero della maggiore

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f""))

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"I nodi della componente connessa maggiore sono:"))

&#x20;       for nodo in componenteMaggiore:

&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"{nodo.getName()}"))



&#x20;       **self.\_view.update\_page()**













&#x20;   def handleCammino(self,e):

&#x20;       pass















































# **view**

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





&#x20;       self.\_ddGenre = ft.Dropdown(label="formato multimediale")

&#x20;       self.\_controller.fillDDmediaType()

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



























