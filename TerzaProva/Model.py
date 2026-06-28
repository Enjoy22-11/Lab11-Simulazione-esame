#Model
# da importare sempre
import networkx as nx
import datetime
from database.DAO import DAO


class Model:
    def __init__(self):
        # da inserire sempre nell'init
        self.grafo = nx.Graph()
        self.mappaCostumer = {}

    # inserisci anni 2023-2025
    def anni2023_2025(self):
        anni = []
        for i in range(2023, 2026):
            anni.append(i)
        return anni

    def getEmployeers(self):  # solito metodo per passare al controller la lista
        emp = DAO.getEmployees()
        return emp

    def getCostumers(self, IdEmployee, dataInizio, dataFine):  # trovo i costumers dati tre parametri

        # nel metodo per generare i nodi ricordarsi sempre di pulire mappa e grafo all'inzio
        self.grafo.clear()
        self.mappaCostumer.clear()

        listaCostumer = DAO.getNodi(IdEmployee)
        if len(listaCostumer) == 0:  # verificare sempre che i dati presi dal Dao non siano 0
            return

        else:  # verifica che non ci sia nella mappa e quindi se necessario aggiungerlo
            for i in listaCostumer:
                if i.getIdC() not in self.mappaCostumer:
                    dataTransazione = i.getData()

                    if dataTransazione.year >= dataInizio and dataTransazione.year <= dataFine:  # verifica data

                        if i.getAzienda() is None:  # verifica azienda
                            i.setAzienda("Privato")

                        if "@" in i.getEmail():  # verifica mail
                            self.mappaCostumer[i.getIdC()] = i
                            self.grafo.add_node(i)
            # archi pesati
            listaArchi = DAO.getArchi()
            for id1, id2, peso in listaArchi:
                if id1 in self.mappaCostumer and id2 in self.mappaCostumer:  # verifico siano nella mappa
                    nodo1 = self.mappaCostumer[id1]
                    nodo2 = self.mappaCostumer[id2]
                    pesoarco = peso
                    self.grafo.add_edge(nodo1, nodo2, weight=pesoarco)  # creo l'arco
            return self.mappaCostumer

    # numero Nodi e archi
    def getNumeroNodi(self):
        return len(self.grafo.nodes())

    def getNumeroArchi(self):
        return len(self.grafo.edges())

    # top five archi (dal più grande al più piccolo)
    def getTopFive(self):
        # prendo tutti gli archi
        tuttiGliArchi = self.grafo.edges(data=True)
        archiInOrdine = sorted(tuttiGliArchi, key=lambda x: x[2]["weight"], reverse=True)
        return archiInOrdine[:5]

    # componenti connesse (lunghezza e max/min)
    def getInfoComponenti(self):
        # ATTENZIONE: connected_components funziona SOLO su grafi NON orientati (nx.Graph)
        # Trasformiamo i risultati in una lista di set Python
        componenti = list(nx.connected_components(self.grafo))

        # Il numero totale di componenti connesse è la lunghezza della lista
        num_componenti = len(componenti)

        # Per trovare la componente più grande, cerchiamo il set con più elementi (key=len)
        comp_minore = min(componenti, key=len) if componenti else []

        return num_componenti, comp_minore
