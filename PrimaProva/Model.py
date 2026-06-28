
#Model

#da importare sempre
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
#da inserire sempre nell'init
        self.grafo = nx.DiGraph()
        self.idMap = {}
        self.mappaArtista_influenza = {}
#passo i generi
    def getallgenre(self):
        return DAO.getGenereMusicale()


    def creaGrafo(self,nomeGenere):
#nel metodo per generare i nodi ricordarsi sempre di pulire mappa e grafo all'inzio
        self.grafo.clear()
        self.idMap.clear()

        cantantiDatoGenere = DAO.getMusician(nomeGenere)
        mappa_popolarita = DAO.getPopolarita()

        self.grafo.add_nodes_from(cantantiDatoGenere)
        for c in cantantiDatoGenere:
            self.idMap[c.ArtistId] = c

#Quei due for i... e for j in range(i+1... servono a creare tutte le coppie possibili senza ripetizioni.
        clienti_e_Artisti = DAO.getBaseArchi()
        for cliente, listaArtisti in clienti_e_Artisti.items():
            for i in range(len(listaArtisti)):
                for j in range(i+1,len(listaArtisti)):
                    id_a1 = listaArtisti[i]
                    id_a2 = listaArtisti[j]
                    if id_a1 in self.idMap and id_a2 in self.idMap:
                        nodo1= self.idMap[id_a1]
                        nodo2 = self.idMap[id_a2]
                        #inserisco anche le popolarita in due variabili
                        popolarita1 = mappa_popolarita.get(id_a1,0)                             # il ,0 serve a mettere popolarita nulla se non c'è
                        popolarita2 = mappa_popolarita.get(id_a2,0)
                        peso_arco = popolarita1 + popolarita2                                   #dato dalla somma delle popolarita

#archi pesati
                        if popolarita1 > popolarita2:
                            self.grafo.add_edge(nodo1, nodo2, weight = peso_arco)
                        elif popolarita1 < popolarita2:
                            self.grafo.add_edge(nodo2, nodo1, weight = peso_arco)
                        #else:
                          #   self.grafo.add_edge(nodo1, nodo2, weight = peso_arco)
                          #  self.grafo.add_edge(nodo2, nodo1, weight = peso_arco)




#numero Nodi e archi
    def getNumeroNodi(self):
        return len(self.grafo.nodes())
    def getNumeroArchi(self):
        return len(self.grafo.edges())

#Artista con maggiore influenza   (nodi entranti e uscenti)
    def getArtistaMaggioreInfluenza(self):
        self.mappaArtista_influenza.clear()
        for artist in self.grafo.nodes():
            self.mappaArtista_influenza[artist] = (
                    self.grafo.out_degree(artist, weight="weight")         #archi uscenti
                    - self.grafo.in_degree(artist, weight="weight"))       #archi entranti

        piuPopolare =sorted(self.mappaArtista_influenza, key= self.mappaArtista_influenza.get, reverse = True)[0]      #ordino e prendo quello piu popolare
        return piuPopolare


#top five archi (dal più grande al più piccolo)
    def getTopFive(self):
        #prendo tutti gli archi
        tuttiGliArchi = self.grafo.edges(data=True)
        archiInOrdine = sorted(tuttiGliArchi, key= lambda x: x[2]["weight"], reverse=True)
        return archiInOrdine[:5]
