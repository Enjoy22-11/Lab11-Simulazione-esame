#model
#da importare sempre
import networkx as nx
from database.DAO import DAO


class Model:
#da inserire sempre nell'init
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}


    def getallMediaType(self):                             #solito metodo per passare al controller la lista
        return DAO.GetMediaTipo()


#nel metodo per generare i nodi ricordarsi sempre di pulire mappa e grafo all'inzio
    def creaGrafo(self,tipoMedia):
        self.grafo.clear()
        self.idMap.clear()

#prendo nodi e archi dal DAO
        tracceDatoTipo = DAO.get_track(tipoMedia)
        allarchipesati = DAO.getNodiePeso()


#verifico che i Byte siano positivi
        for traccia in tracceDatoTipo:
            tracciaMB = traccia.dammiMB()
            if tracciaMB <= 0:
                continue
            else:
                traccia.setMB(tracciaMB)
                self.grafo.add_node(traccia)

#inserisco nella mappa
                self.idMap[traccia.TrackId] = traccia

#archi pesati
        for traccia1, traccia2, peso in allarchipesati:
            if traccia1 in self.idMap and traccia2 in self.idMap:            #verifico siano nella mappa
                nodo1 = self.idMap[traccia1]
                nodo2 = self.idMap[traccia2]
                pesoarco = peso
                self.grafo.add_edge(nodo1, nodo2, weight=pesoarco)           #creo l'arco



#numero Nodi e archi
    def getNumeroNodi(self):
        return len(self.grafo.nodes())
    def getNumeroArchi(self):
        return len(self.grafo.edges())


#top five archi (dal più grande al più piccolo)
    #top 5 archi con peso maggiore
    def getTopFive(self):
        #prendo tutti gli archi
        tuttiGliArchi = self.grafo.edges(data=True)
        archiInOrdine = sorted(tuttiGliArchi, key= lambda x: x[2]["weight"], reverse=True)
        return archiInOrdine[:5]



#componenti connesse (lunghezza e max/min)
    def getInfoComponenti(self):
        # ATTENZIONE: connected_components funziona SOLO su grafi NON orientati (nx.Graph)
        # Trasformiamo i risultati in una lista di set Python
        componenti = list(nx.connected_components(self.grafo))

        # Il numero totale di componenti connesse è la lunghezza della lista
        num_componenti = len(componenti)

        # Per trovare la componente più grande, cerchiamo il set con più elementi (key=len)
        comp_maggiore = max(componenti, key=len) if componenti else []

        return num_componenti, comp_maggiore
