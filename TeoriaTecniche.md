Il Metodo del Professore (Quello che ti spaventa):

###### **Lui nel DAO crea il dizionario e lo popola:**



Python

&#x20;       **# Nel DAO...**

&#x20;       for row in cursor:

&#x20;           idArtist = row\["ArtistId"]

&#x20;           popolarita = row\["popolarita"]

&#x20;           result\[idArtist] = popolarita  **# Crea la mappa qui**

&#x20;       return result

Il Tuo Metodo (Lista di Tuple + Mappa nel Model):





###### **Tu nel DAO restituisci una normalissima e tranquillissima lista di tuple (esattamente come fai per gli archi!):**

Python

&#x20;       **# Nel Tuo DAO...**

&#x20;       for row in cursor:

&#x20;           **# Butto tutto in una lista pacifica e me ne vado**

&#x20;           result.append((row\["ArtistId"], row\["popolarita"]))

&#x20;       return result



###### **E poi nel Model.py, quando ti serve usarla, fai la tua amata magia con la mappa:**



Python

&#x20;       # Nel Tuo Model...

&#x20;       lista\_popolarita = DAO.getPopolarita()

&#x20;       mappa\_popolarita = {}

&#x20;       

&#x20;       for id\_artista, pop in lista\_popolarita:

&#x20;            mappa\_popolarita\[id\_artista] = pop

&#x20;            

&#x20;       # E ora la usi esattamente come volevi tu!

Ancora meglio se usi le tue Dataclass! Se una query restituisce dati complessi di un Cliente o di un Artista, tu estrai le righe dal DAO con result.append(Artista(row)), e poi in Python verifichi i dati con i metodi get, controlli se appartengono al periodo giusto, e decidi se metterli nella tua idMap e nel grafo.

















###### 

###### **Assolutamente sì! Le tuple possono contenere infiniti elementi. Se la tua query SQL restituisce 4 o 5 colonne, tu nel DAO farai result.append((row\["col1"], row\["col2"], row\["col3"])) e nel Model scriverai esattamente come hai intuito:**



###### **Python**

###### **for el1, el2, el3 in lista\_di\_tuple:**

###### &#x20;   **# fai le tue verifiche**





























##### **Gli Archi e il Verso (Orientato)**

Ti chiede un grafo orientato (nx.DiGraph()).

L'arco esiste se c'è "almeno un cliente in comune". Come si fa? Esattamente con la Self-Join che abbiamo visto oggi pomeriggio!



Fai la query per trovare le coppie di artisti comprati dallo stesso cliente.



Nel ciclo for in Python estrai la coppia (artista\_A, artista\_B).



La trappola subdola del verso: Invece di fare add\_edge(A, B) direttamente, usi gli if e interroghi la tua mappa della popolarità:



Python

pop\_A = mappa\_popolarita\[A.id]

pop\_B = mappa\_popolarita\[B.id]

peso\_arco = pop\_A + pop\_B



if pop\_A > pop\_B:

&#x20;   grafo.add\_edge(A, B, weight=peso\_arco)

elif pop\_B > pop\_A:

&#x20;   grafo.add\_edge(B, A, weight=peso\_arco)

else: # Sono uguali

&#x20;   grafo.add\_edge(A, B, weight=peso\_arco)

&#x20;   grafo.add\_edge(B, A, weight=peso\_arco)

















##### **#ricorda <** 

t1.ArtistId < t2.ArtistId        -- Niente cloni













#### **#Ragionamento usato nelle popolarità**

**Step 1**: I Nodi e la Popolarità (in SQL)

Fai una **query normalissima per prendere gli artisti** e, già che ci sei, conti i loro brani venduti (la popolarità).

Nel Model, crei i nodi e salvi la popolarità in una tua mappa:



**Python**

\# Mappa magica che ti salva la vita

self.mappa\_popolarita\[artista.id] = artista.popolarita







**Step 2**: La Query degli Archi "Vuota" (in **SQL**)

Invece di spaccarti la testa per calcolare il peso e i versi in DBeaver, tu fai una query banalissima per trovare solo CHI è collegato a CHI.

"Hanno un cliente in comune?" Perfetto. Niente SUM, niente pesi complessi. Solo:



**SQL**

SELECT DISTINCT t1.ArtistId as id1, t2.ArtistId as id2

FROM invoiceline il1, invoiceline il2, track t1, track t2

WHERE il1.InvoiceId = il2.InvoiceId  -- Stessa fattura (stesso cliente)

AND il1.TrackId = t1.TrackId 

AND il2.TrackId = t2.TrackId

AND t1.ArtistId < t2.ArtistId        -- Niente cloni

Fine. Il DAO ti restituisce solo una lista di tuple (id1, id2).



**Step 3:** La Magia in Python (Il tuo capolavoro)

Ora sei nel tuo **Model.py**, hai la tua lista di collegamenti grezzi e hai la mappa delle popolarità. Fai tutto qui, al calduccio e senza errori di sintassi SQL:



Python

&#x20;       archi\_grezzi = DAO.getArchiGrezzi()

&#x20;       

&#x20;       for id1, id2 in archi\_grezzi:

&#x20;           # Controllo che entrambi siano nel mio grafo (il tuo filtro di sicurezza!)

&#x20;           if id1 in self.mappa\_popolarita and id2 in self.mappa\_popolarita:

&#x20;               

&#x20;               # 1. Recupero le popolarità

&#x20;               pop1 = self.mappa\_popolarita\[id1]

&#x20;               pop2 = self.mappa\_popolarita\[id2]

&#x20;               

&#x20;               # 2. Calcolo il peso (il testo dice: somma delle popolarità)

&#x20;               peso\_totale = pop1 + pop2

&#x20;               

&#x20;               # 3. Decido il verso della freccia (il testo dice: dal più al meno popolare)

&#x20;               if pop1 > pop2:

&#x20;                   self.grafo.add\_edge(id1, id2, weight=peso\_totale)

&#x20;               elif pop2 > pop1:

&#x20;                   self.grafo.add\_edge(id2, id1, weight=peso\_totale)

&#x20;               else:

&#x20;                   # Popolarità uguale: doppio arco!

&#x20;                   self.grafo.add\_edge(id1, id2, weight=peso\_totale)

&#x20;                   self.grafo.add\_edge(id2, id1, weight=peso\_totale)















##### **⏱️ CHEAT SHEET: I metodi datetime**

La libreria MySQL-Connector è tua amica: quando fai una SELECT su una colonna Date o DateTime, Python te la trasforma già in un oggetto datetime. Non devi convertirla da stringa!



Python

**import datetime**



**# 1. Estrarre i pezzi della data**

anno = mia\_data.year

mese = mia\_data.month

giorno = mia\_data.day



**# 2. Confrontare le date (funziona con i normali operatori!)**

if data\_acquisto.year >= 2010 and data\_acquisto.year <= 2015:

&#x20;   print("È nel range!")



**# 3. Creare una data fissa a mano (se ti serve per un controllo)**

data\_limite = datetime.date(2010, 1, 1) # Anno, Mese, Giorno



**# 4. Ottenere la data di oggi (raro all'esame, ma utile)**

oggi = datetime.datetime.now()















#### **🕸️ CHEAT SHEET: I metodi NetworkX (nx)**

Questa è la Bibbia per il Punto 1 e il Punto 2. Non ti serve altro.



###### 1\. Creazione e Gestione Base

Python

**import networkx as nx**



self.grafo = nx.Graph()                              # NON orientato (senza frecce)

self.grafo = nx.DiGraph()                            # Orientato (con frecce, usato per "chi influenza chi")



self.grafo.clear()                                   # SVUOTA IL GRAFO (usalo sempre all'inizio del metodo!)



self.grafo.add\_node(nodo)                            #aggiungi nodo

self.grafo.add\_edge(nodo1, nodo2, weight=peso)       #aggiungi arco



###### 2\. Lettura e Statistiche (Punto 1)

Python

###### **# Quanti sono?**

num\_nodi = len(self.grafo.nodes())                   #numero di nodi

num\_archi = len(self.grafo.edges())                  #numero di archi



##### **# Estrarre gli archi con i loro pesi**

\# **data=True** è FONDAMENTALE, altrimenti ti dà solo la coppia di nodi senza il peso!

###### **tutti\_gli\_archi = self.grafo.edges(data=True)** 







###### **# Componenti Connesse (SOLO PER nx.Graph() NON orientati!)**

componenti = list(nx.connected\_components(self.grafo))

num\_comp = len(componenti)

comp\_maggiore = max(componenti, key=len) # Restituisce il SET di nodi più grande





###### **3. Analisi dei Pesi e Gradi (Le domande "subdole")**

Se il prof ti chiede "chi è l'artista più influente" o "calcola la differenza dei pesi", usa questi:



Python



##### **# Grado semplice (quanti vicini ha un nodo)**

vicini = self.grafo.degree(nodo) 

###### **#se chiede i top vicini:**

def getTopCinqueVicini(self):

&#x20;       **# 1. self.grafo.degree() restituisce una lista di tuple: (Oggetto\_Nodo, numero\_di\_vicini)**

&#x20;       tutti\_i\_gradi = list(self.grafo.degree())

&#x20;       

&#x20;       **# 2. Ordiniamo la lista.** 

&#x20;       **# x\[0] è il nodo, x\[1] è il numero di vicini. Quindi usiamo x\[1] come chiave.**

&#x20;       **# reverse=True mette il più grande in cima.**

&#x20;       gradi\_ordinati = sorted(tutti\_i\_gradi, key=lambda x: x\[1], reverse=True)

&#x20;       

&#x20;       **# 3. Restituiamo i primi 5**

&#x20;       return gradi\_ordinati\[:5]



**Come stamparli nel Controller**

Siccome la funzione ti restituisce una lista di tuple fatte così: (nodo, grado), nel Controller puoi estrarli in modo elegantissimo e stamparli nella View:

**# Richiami la funzione**

&#x20;       top\_nodi = self.\_model.getTopCinqueVicini()

&#x20;       

&#x20;       self.\_view.txt\_result.controls.append(ft.Text("I 5 nodi con più vicini sono:"))

&#x20;       

&#x20;       **# Unpacking della tupla direttamente nel for**

&#x20;       for nodo, numero\_vicini in top\_nodi:

&#x20;           **# Essendo 'nodo' il tuo oggetto, puoi chiamare i suoi metodi o attributi**

&#x20;           nome\_cliente = nodo.getNameCostumer()

&#x20;           cognome\_cliente = nodo.getSurnameCostumer()

&#x20;           

&#x20;           self.\_view.txt\_result.controls.append(ft.Text(f"- {nome\_cliente} {cognome\_cliente} (Vicini: {numero\_vicini})"))





###### **Se l'esame ti chiede i vicini in un grafo NON orientato (nx.Graph()), usi self.grafo.degree().**



Ma se l'esame fosse sul grafo Orientato (nx.DiGraph()), la parola "vicini" diventa ambigua. Il professore preciserà se vuole:



I nodi verso cui "punta" (archi uscenti) -> **Usi list(self.grafo.out\_degree())**



I nodi da cui "è puntato" (archi entranti) -> **Usi list(self.grafo.in\_degree())**



Il resto del codice (il sorted e il lambda) rimane identico!









##### **# GRAFI ORIENTATI (DiGraph): Pesi in entrata e in uscita**

peso\_entrante = self.grafo.in\_degree(nodo, weight='weight')

peso\_uscente = self.grafo.out\_degree(nodo, weight='weight')

influenza = peso\_uscente - peso\_entrante



###### **# Trovare i vicini di un nodo specifico (Usatissimo nel Punto 2 per la Ricorsione!)**

lista\_vicini = list(self.grafo.neighbors(nodo\_partenza))



##### **4. Ordinamento Rapido (Il trucco della lambda)**

##### **Questa riga di codice compare nel 99% degli esami per stampare "i 5 archi col peso maggiore". Ricopiala a memoria:**

Python

**archi\_ordinati** = sorted(self.grafo.edges(data=True), key=lambda x: x\[2]\['weight'], reverse=True)

top\_5 = archi\_ordinati\[:5]

(Spiegazione rapida: x\[0] è nodo1, x\[1] è nodo2, x\[2] è il dizionario degli attributi, quindi x\[2]\['weight'] pesca il peso).





###### **1. Il mistero di sorted e lambda: Tuple o Dizionari?**

La risposta è: entrambi contemporaneamente.



Quando tu chiami **self.grafo.edges(data=True), NetworkX ti restituisce una Lista di Tuple.** **Ma l'ultimo elemento di questa tupla è un Dizionario.**



Immagina che NetworkX ti restituisca questa lista:



Python

\[

&#x20; (Nodo\_A, Nodo\_B, {"weight": 10, "color": "red"}), 

&#x20; (Nodo\_C, Nodo\_D, {"weight": 25, "color": "blue"})

]

Quando scrivi key=lambda x: x\[2]\['weight'], Python prende ogni singola tupla (che chiama x) e fa questo ragionamento:



x\[0] è il primo nodo.



x\[1] è il secondo nodo.



x\[2] è il dizionario degli attributi (terza posizione).



x\[2]\['weight'] entra nel dizionario e pesca il valore associato alla chiave "weight".































































