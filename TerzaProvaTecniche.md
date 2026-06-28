Richieste:

PUNTO 1 (21 Punti)

1\. L'utente seleziona da due menù a tendina due anni che definiscono un range temporale (es. Da: 2009, A: 2011). Da un terzo menù a tendina, seleziona il nome di un dipendente (Employee, visualizzando "Nome Cognome"). I menù degli anni devono essere popolati interrogando il database per ottenere gli anni in cui è stata emessa almeno una fattura.



2\. Premendo sul tasto Crea grafo, l'applicazione dovrà costruire un grafo semplice, NON orientato e pesato, così costituito:



**I Nodi: Sono tutti i clienti (Customer) seguiti dal dipendente selezionato (campo SupportRepId) che hanno effettuato almeno un acquisto (tabella Invoice) nel range di anni indicato (estremi inclusi).**



Trappola di Validazione: Si inseriscano nel grafo solo i clienti la cui Email è valida (deve contenere il carattere @). Inoltre, si salvi nel nodo anche il nome dell'azienda (Company); se il cliente non ha un'azienda (campo NULL), il programma deve salvare automaticamente la stringa "Privato".



**Gli Archi: Due clienti (nodi) sono connessi da un arco se e solo se hanno acquistato brani appartenenti allo stesso Album (AlbumId) nel corso del periodo selezionato.**



**Il Peso: Il peso dell'arco è pari alla somma totale dell'importo speso per quell'album in comune.** Il calcolo si ottiene sommando (UnitPrice \* Quantity) dalla tabella InvoiceLine per i brani di quell'album, unendo la spesa del Cliente A e la spesa del Cliente B nel lasso di tempo selezionato.



3\. Costruito il grafo, l'applicazione visualizza il numero di nodi e di archi presenti. Alla pressione di un tasto Stampa Dettagli, il programma dovrà:



Stampare i 3 archi di peso maggiore (mostrando i nomi e cognomi dei due clienti e il peso).



Stampare il numero di componenti connesse.



Stampare Nome, Cognome e Azienda (Company / "Privato") dei clienti che compongono la componente connessa più piccola (con meno nodi).

































# **DAO**



from database.DB\_connect import DBConnect

from model.Costumer import Costumer

from model.Employee import Employee, Employee





class DAO():

&#x20;   def \_\_init\_\_(self):

&#x20;       pass



###### **#trovo impiegati, nessun parametro da passare**

&#x20;   @staticmethod

&#x20;   def getEmployees():

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select e.EmployeeId as Id, e.FirstName as Name, e.LastName as Surname

&#x20;               from employee as e """

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           result.append(**Employee**(\*\*row))

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



###### **#trovo nodi Passando un parametro**

&#x20;   @staticmethod

&#x20;   def getNodi(EmployeeId):

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select c.CustomerId as IdC, i.InvoiceDate as data, c.FirstName as Name, c.LastName as Surname, c.Company as azienda, c.Email as email

&#x20;                  from customer as c, employee as e, invoice as i

&#x20;                  where c.SupportRepId = e.EmployeeId

&#x20;                  and e.EmployeeId = %s

&#x20;                  and i.CustomerId = c.CustomerId"""

&#x20;       cursor.execute(query, (EmployeeId,))

&#x20;       for row in cursor:

&#x20;           result.append(**Costumer**(\*\*row))

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



###### **#trovo archi con il loro peso, no parametri**

&#x20;   @staticmethod

&#x20;   def getArchi():

&#x20;       conn = DBConnect.get\_connection()

&#x20;       result = \[]

&#x20;       cursor = conn.cursor(dictionary=True)

&#x20;       query = """select i1.CustomerId as ID1, i2.CustomerId as ID2, sum((il1.UnitPrice\*il1.Quantity)+(il2.UnitPrice\*il2.Quantity)) as peso

&#x20;                  from invoice as i1, invoiceline as il1, track as t1, invoice as i2, invoiceline as il2, track as t2

&#x20;                  where t1.AlbumId = t2.AlbumId

&#x20;                  and i1.CustomerId < i2.CustomerId

&#x20;                  and il1.TrackId = t1.TrackId

&#x20;                  and il2.TrackId = t2.TrackId

&#x20;                  and i1.InvoiceId = il1.InvoiceId

&#x20;                  and i2.InvoiceId = il2.InvoiceId

&#x20;                  group by i1.CustomerId, i2.CustomerId"""

&#x20;       cursor.execute(query)

&#x20;       for row in cursor:

&#x20;           result.append((row\["ID1"], row\["ID2"], row\["peso"]))

&#x20;       cursor.close()

&#x20;       conn.close()

&#x20;       return result



















# **#TestModel**

**from model.model import Model**

**myModel = Model()**

myModel.creaGrafo("Metal")

Nnodes = **myModel**.getNumeroNodi()

print(f"numero dei nodi pari a: {Nnodes}")

myModel.anni2023\_2025()

for i in myModel.anni2023\_2025():

&#x20;   print(i)

for i in myModel.getEmployeers():

&#x20;   print(i)

print(myModel.getCostumers(3))











# Costumer

from dataclasses import dataclass



###### **#dataclass**

@dataclass

class Costumer:

&#x20;   IdC: int

&#x20;   data: str

&#x20;   Name: str

&#x20;   Surname: str

&#x20;   azienda: str

&#x20;   email: str



###### **#da mettere sempre dataclass**

&#x20;   def \_\_hash\_\_(self):

&#x20;       return hash(self.IdC)



&#x20;   def \_\_eq\_\_(self, other):

&#x20;       return self.IdC == other.IdC



&#x20;   def \_\_str\_\_(self):

&#x20;       return f" cliente numero: {self.IdC} nell'azienda: {self.azienda} (email: {self.email})"



\#ID

&#x20;   def getIdC(self):

&#x20;       return self.IdC

\#DATE

&#x20;   def getData(self):

&#x20;       return self.data

\#Azienda

&#x20;   def getAzienda(self):

&#x20;       return self.azienda

\#setAzienda

&#x20;   def setAzienda(self, inputazienda):

&#x20;       self.azienda =  inputazienda

\#email

&#x20;   def getEmail(self):

&#x20;       return self.email

\#Name

&#x20;   def getNameCostumer(self):

&#x20;       return self.Name

\#surname

&#x20;   def getSurnameCostumer(self):

&#x20;       return self.Surname



















# Employee

from dataclasses import dataclass



###### **#dataclass**

@dataclass

class Employee:

&#x20;   Id: int

&#x20;   Name: str

&#x20;   Surname: str

###### **#da mettere sempre dataclass**



&#x20;   def \_\_hash\_\_(self):

&#x20;       return hash(self.Id)



&#x20;   def \_\_eq\_\_(self, other):

&#x20;       return self.Id == other.Id



&#x20;   def \_\_str\_\_(self):

&#x20;       return f" {self.Name} {self.Surname} (ID: {self.Id})"









&#x20;   def getId(self):

&#x20;       return self.Id



























# **Model**

###### **#da importare sempre**

import networkx as nx

import datetime

from database.DAO import DAO



class Model:

&#x20;   def \_\_init\_\_(self):

###### **#da inserire sempre nell'init**

&#x20;       self.grafo = nx.Graph()

&#x20;       self.mappaCostumer = {}

&#x20;

\#inserisci anni 2023-2025

&#x20;   def anni2023\_2025(self):

&#x20;       anni = \[]

&#x20;       for i in range(2023,2026):

&#x20;           anni.append(i)

&#x20;       return anni





###### 

###### &#x20;   def getEmployeers(self):                    **#solito metodo per passare al controller la lista**

&#x20;       emp = DAO.getEmployees()

&#x20;       return emp





&#x20;   def getCostumers(self, IdEmployee, dataInizio, dataFine):      **#trovo i costumers dati tre parametri**



###### **#nel metodo per generare i nodi ricordarsi sempre di pulire mappa e grafo all'inzio**

&#x20;       self.grafo.clear()

&#x20;       self.mappaCostumer.clear()



&#x20;       listaCostumer = DAO.getNodi(IdEmployee)

&#x20;       if len(listaCostumer) == 0:                        **#verificare sempre che i dati presi dal Dao non siano 0**

&#x20;           return



&#x20;       else:                                              **#verifica che non ci sia nella mappa e quindi se necessario aggiungerlo**

&#x20;           for i in listaCostumer:

&#x20;               if i.getIdC() not in self.mappaCostumer:

&#x20;                   dataTransazione = i.getData()



&#x20;                   if dataTransazione.year >= dataInizio and dataTransazione.year <= dataFine:      #verifica data



&#x20;                       if i.getAzienda() is None:   #verifica azienda

&#x20;                           i.setAzienda("Privato")



&#x20;                       if "@" in i.getEmail():                     #verifica mail

&#x20;                           self.mappaCostumer\[i.getIdC()] = i

&#x20;                           self.grafo.add\_node(i)

###### **#archi pesati**

&#x20;           listaArchi = DAO.getArchi()

&#x20;           for id1, id2, peso in listaArchi:

&#x20;               if id1 in self.mappaCostumer and id2 in self.mappaCostumer:     **#verifico siano nella mappa**

&#x20;                   nodo1 = self.mappaCostumer\[id1]

&#x20;                   nodo2 = self.mappaCostumer\[id2]

&#x20;                   pesoarco = peso

&#x20;                   self.grafo.add\_edge(nodo1, nodo2, weight=pesoarco)      **#creo l'arco**

&#x20;           return self.mappaCostumer



##### **#numero Nodi e archi**

&#x20;   def getNumeroNodi(self):

&#x20;       return len(self.grafo.nodes())





&#x20;   def getNumeroArchi(self):

&#x20;       return len(self.grafo.edges())



##### **#top five archi (dal più grande al più piccolo)**

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

&#x20;       comp\_minore = min(componenti, key=len) if componenti else \[]



&#x20;       return num\_componenti, comp\_minore





















# **Controller**

import flet as ft





class Controller:

&#x20;   def \_\_init\_\_(self, view, model):

&#x20;       # the view, with the graphical elements of the UI

&#x20;       self.\_view = view

&#x20;       # the model, which implements the logic of the program and holds the data

&#x20;       self.\_model = model







&#x20;   def fillDDGenre(self):

&#x20;       pass





\#anno inizio

###### **#inseriamo gli anni nel dropdown**

&#x20;   def selezionaAnni(self):

&#x20;       anni = self.\_model.anni2023\_2025()

&#x20;       listaAnni = \[]

&#x20;       for anno in anni:

&#x20;           listaAnni.append(ft.dropdown.Option(anno))

&#x20;       self.\_view.\_ddGenre.options = listaAnni

&#x20;       self.\_view.update\_page()







\#anno fine



&#x20;   def selezionaAnni2(self, e):

###### **#prendo il valore del dropdown**

&#x20;       annoSelezionatoInizio =  int(self.\_view.\_ddGenre.value)

###### **#verifico non sia nullo**

&#x20;       if annoSelezionatoInizio is None:

&#x20;           self.\_view.txt\_result.controls.append(ft.Text("Selezionare un anno di fine"))

&#x20;           self.\_view.update\_page()

&#x20;           return

###### **#inserisco un nuovo dropdown**

&#x20;       annidisponibili = self.\_model.anni2023\_2025()

&#x20;       listaAnni = \[]

&#x20;       for anno in annidisponibili:

&#x20;           if anno >= annoSelezionatoInizio:

&#x20;               listaAnni.append(ft.dropdown.Option(anno))

&#x20;       self.\_view.\_ddArtist.options = listaAnni

&#x20;       self.\_view.update\_page()





\#employ

##### **#inserisco un nuovo dropdown con scritta diversa da value (key)**

&#x20;   def employees(self):

&#x20;       emp1= self.\_model.getEmployeers()

&#x20;       listaEmployees = \[]

&#x20;       for employ in emp1:

&#x20;           listaEmployees.append(ft.dropdown.Option(key=str(employ.Id), text=str(employ)))

&#x20;       self.\_view.\_nomi.options = listaEmployees

&#x20;       self.\_view.update\_page()







###### **#costumer genera nodi**

&#x20;   def GeneraNodi(self, e):

&#x20;       if self.\_view.\_ddGenre.value is None:                                                   **#controllo se l'utente non ha selezionato nulla**

&#x20;           self.\_view.txt\_result.controls.append(ft.Text("Selezionare una data di inizio"))

&#x20;           self.\_view.update\_page()

&#x20;           return

&#x20;       if self.\_view.\_ddArtist.value is None:                                                  **#controllo se l'utente non ha selezionato nulla**

&#x20;           self.\_view.txt\_result.controls.append(ft.Text("Selezionare una data di fine"))

&#x20;           self.\_view.update\_page()

&#x20;           return

&#x20;       if self.\_view.\_nomi.value is None:                                                      **#controllo se l'utente non ha selezionato nulla**

&#x20;           self.\_view.txt\_result.controls.append(ft.Text("Selezionare un employ"))

&#x20;           self.\_view.update\_page()

&#x20;           return



&#x20;       dataInizio = int(self.\_view.\_ddGenre.value)  #registro valori

&#x20;       datafine = int(self.\_view.\_ddArtist.value)

&#x20;       employ = int(self.\_view.\_nomi.value)



&#x20;       dictionarycostumer =self.\_model.getCostumers(employ, dataInizio, datafine)               #li passo alla funzione



###### **#prendo i valori dei nodi e degli archi**

&#x20;       numeroDiNodi = self.\_model.getNumeroNodi()

&#x20;       numeroDiArchi = self.\_model.getNumeroArchi()



###### **#prima di inserire valori ricordarsi di pulire il drodown**

&#x20;       self.\_view.txt\_result.controls.clear()



&#x20;       self.\_view.txt\_result.controls.append(ft.Text("Grafo creato correttamente"))



&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))      **#stampo numero di Nodi**

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))    **#stampo numero di Archi**



&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"i costumer sono:"))



&#x20;       if dictionarycostumer is None:                                                            #controllo che la funzione non sia nulla

&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"non ci sono Costumer"))

&#x20;       else:

&#x20;           for i in dictionarycostumer:                                                          #stampo tutti i costumer

&#x20;               self.\_view.txt\_result.controls.append(ft.Text(f"{dictionarycostumer\[i]}"))



&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f""))





###### **#stampo i top five**

&#x20;           architopfive = self.\_model.getTopFive()                                                 #prendo gli archi

&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"I 5 archi con peso maggiore sono:"))

&#x20;           for arco in architopfive:

&#x20;               nome1 = arco\[0].getNameCostumer()                                                   #primo nodo

&#x20;               nome2 = arco\[1].getSurnameCostumer()                                                #secondo nodo

&#x20;               peso = arco\[2]\["weight"]                                                            #peso



&#x20;               self.\_view.txt\_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))   #stampo



&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f""))



###### **# per le componenti connesse del grafo**

&#x20;       numeroComponenti, componenteMinore = self.\_model.getInfoComponenti()

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"Le componenti connesse del grafo sono: {numeroComponenti}"))

&#x20;       self.\_view.txt\_result.controls.append(ft.Text(f"I nodi della componente connessa minore sono:"))

&#x20;       for nodo in componenteMinore:

&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"nome: {nodo.getNameCostumer()}, cognome: {nodo.getSurnameCostumer()}, Azienda: {nodo.getAzienda()}"))



&#x20;       **self.\_view.update\_page()**







&#x20;   def handleCreaGrafo(self, e):

&#x20;       pass



&#x20;   def handleCreaGrafo(self,e):

&#x20;       pass



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





###### **#Dropdown da, con cambiamento se selezioni un anno**

&#x20;       self.\_ddGenre = ft.Dropdown(label="ANNI DA:", on\_change=self.\_controller.selezionaAnni2)

**#richiamo della funzione**

&#x20;       self.\_controller.selezionaAnni()

&#x20;       self.\_btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo e Stampa Dettagli", on\_click=self.\_controller.GeneraNodi)



**#aggiunta alle righe**

&#x20;       row1 = ft.Row(\[self.\_ddGenre, self.\_btnCreaGrafo],

&#x20;                     alignment=ft.MainAxisAlignment.CENTER)

&#x20;       self.\_page.controls.append(row1)



**#secondo dropdown**

&#x20;       self.\_ddArtist = ft.Dropdown(label="A:")

&#x20;       self.\_btnCreaGrafo = ft.ElevatedButton(text="Trova Cammino", on\_click=self.\_controller.handleCammino)



&#x20;       row2 = ft.Row(\[self.\_ddArtist, self.\_btnCreaGrafo],

&#x20;                     alignment=ft.MainAxisAlignment.CENTER)

&#x20;       self.\_page.controls.append(row2)



**#terzo dropdown**

&#x20;       self.\_nomi = ft.Dropdown(label="Employees:")

&#x20;       self.\_controller.employees()

&#x20;       self.\_btnpuzzetta = ft.ElevatedButton(text="puzzetta")



&#x20;       row3 = ft.Row(\[self.\_nomi, self.\_btnpuzzetta],

&#x20;                     alignment=ft.MainAxisAlignment.CENTER)

&#x20;       self.\_page.controls.append(row3)



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

