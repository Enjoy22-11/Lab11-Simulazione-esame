#controller
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        pass

#inseriamo i tipi di media nel dropdown
    def fillDDmediaType(self):
        mediaTipo = self._model.getallMediaType()
        listamediatipo = []
        for nometipo in mediaTipo:
            listamediatipo.append(ft.dropdown.Option(nometipo))
        self._view._ddGenre.options = listamediatipo
        self._view.update_page()


    def handleCreaGrafo(self, e):
#prendo il valore del dropdown
        tipoMedia = self._view._ddGenre.value
#verifico non sia nullo
        if tipoMedia is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare una tipologia di file multimediale"))
            self._view.update_page()
            return


#prendo i valori dei nodi e degli archi
        self._model.creaGrafo(tipoMedia)
        numeroDiNodi = self._model.getNumeroNodi()
        numeroDiArchi = self._model.getNumeroArchi()


#prima di inserire valori ricordarsi di pulire il drodown
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))       #stampo numero di Nodi
        self._view.txt_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))     #stampo numero di Archi



#stampo i 5 archi con peso maggiore
        architopfive = self._model.getTopFive()                                                     #prendo gli archi
        self._view.txt_result.controls.append(ft.Text(f"I 5 archi con peso maggiore sono:"))
        for arco in architopfive:
            nome1 = arco[0].getName()                                                               #primo nodo
            nome2 = arco[1].getName()                                                               #secondo nodo
            peso = arco[2]["weight"]                                                                #peso

            self._view.txt_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))   #stampo

        self._view.txt_result.controls.append(ft.Text(f""))

# per le componenti connesse del grafo
        numeroComponenti, componenteMaggiore = self._model.getInfoComponenti()                                        #prendo le componenti
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse del grafo sono: {numeroComponenti}"))  #ne stampo il numero
        self._view.txt_result.controls.append(ft.Text(f"La componente maggiore ha {len(componenteMaggiore)} nodi"))   #ne stampo il numero della maggiore
        self._view.txt_result.controls.append(ft.Text(f""))
        self._view.txt_result.controls.append(ft.Text(f"I nodi della componente connessa maggiore sono:"))
        for nodo in componenteMaggiore:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.getName()}"))

        self._view.update_page()






    def handleCammino(self,e):
        pass
