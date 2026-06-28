#Controller
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def fillDDGenre(self):
        pass


#anno inizio
#inseriamo gli anni nel dropdown
    def selezionaAnni(self):
        anni = self._model.anni2023_2025()
        listaAnni = []
        for anno in anni:
            listaAnni.append(ft.dropdown.Option(anno))
        self._view._ddGenre.options = listaAnni
        self._view.update_page()



#anno fine

    def selezionaAnni2(self, e):
#prendo il valore del dropdown
        annoSelezionatoInizio =  int(self._view._ddGenre.value)
#verifico non sia nullo
        if annoSelezionatoInizio is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno di fine"))
            self._view.update_page()
            return
#inserisco un nuovo dropdown
        annidisponibili = self._model.anni2023_2025()
        listaAnni = []
        for anno in annidisponibili:
            if anno >= annoSelezionatoInizio:
                listaAnni.append(ft.dropdown.Option(anno))
        self._view._ddArtist.options = listaAnni
        self._view.update_page()


#employ
#inserisco un nuovo dropdown con scritta diversa da value (key)
    def employees(self):
        emp1= self._model.getEmployeers()
        listaEmployees = []
        for employ in emp1:
            listaEmployees.append(ft.dropdown.Option(key=str(employ.Id), text=str(employ)))
        self._view._nomi.options = listaEmployees
        self._view.update_page()



#costumer genera nodi
    def GeneraNodi(self, e):
        if self._view._ddGenre.value is None:                                                   #controllo se l'utente non ha selezionato nulla
            self._view.txt_result.controls.append(ft.Text("Selezionare una data di inizio"))
            self._view.update_page()
            return
        if self._view._ddArtist.value is None:                                                  #controllo se l'utente non ha selezionato nulla
            self._view.txt_result.controls.append(ft.Text("Selezionare una data di fine"))
            self._view.update_page()
            return
        if self._view._nomi.value is None:                                                      #controllo se l'utente non ha selezionato nulla
            self._view.txt_result.controls.append(ft.Text("Selezionare un employ"))
            self._view.update_page()
            return

        dataInizio = int(self._view._ddGenre.value)  #registro valori
        datafine = int(self._view._ddArtist.value)
        employ = int(self._view._nomi.value)

        dictionarycostumer =self._model.getCostumers(employ, dataInizio, datafine)               #li passo alla funzione

#prendo i valori dei nodi e degli archi
        numeroDiNodi = self._model.getNumeroNodi()
        numeroDiArchi = self._model.getNumeroArchi()

#prima di inserire valori ricordarsi di pulire il drodown
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))

        self._view.txt_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))      #stampo numero di Nodi
        self._view.txt_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))    #stampo numero di Archi

        self._view.txt_result.controls.append(ft.Text(f"i costumer sono:"))

        if dictionarycostumer is None:                                                            #controllo che la funzione non sia nulla
            self._view.txt_result.controls.append(ft.Text(f"non ci sono Costumer"))
        else:
            for i in dictionarycostumer:                                                          #stampo tutti i costumer
                self._view.txt_result.controls.append(ft.Text(f"{dictionarycostumer[i]}"))

            self._view.txt_result.controls.append(ft.Text(f""))


#stampo i top five
            architopfive = self._model.getTopFive()                                                 #prendo gli archi
            self._view.txt_result.controls.append(ft.Text(f"I 5 archi con peso maggiore sono:"))
            for arco in architopfive:
                nome1 = arco[0].getNameCostumer()                                                   #primo nodo
                nome2 = arco[1].getSurnameCostumer()                                                #secondo nodo
                peso = arco[2]["weight"]                                                            #peso

                self._view.txt_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))   #stampo

            self._view.txt_result.controls.append(ft.Text(f""))

# per le componenti connesse del grafo
        numeroComponenti, componenteMinore = self._model.getInfoComponenti()
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse del grafo sono: {numeroComponenti}"))
        self._view.txt_result.controls.append(ft.Text(f"I nodi della componente connessa minore sono:"))
        for nodo in componenteMinore:
            self._view.txt_result.controls.append(ft.Text(f"nome: {nodo.getNameCostumer()}, cognome: {nodo.getSurnameCostumer()}, Azienda: {nodo.getAzienda()}"))

        self._view.update_page()



    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass
