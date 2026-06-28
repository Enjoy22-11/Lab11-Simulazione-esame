#controller
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # inseriamo i generi nel dropdown
    def fillDDGenre(self):
        genres = self._model.getallgenre()
        genreDD = []
        for g in genres:
            genreDD.append(ft.dropdown.Option(g))
        self._view._ddGenre.options = genreDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        # prendo il valore del dropdown
        genereSelezionato = self._view._ddGenre.value
        # verifico non sia nullo
        if genereSelezionato is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere"))
            self._view.update_page()
            return
        # creo il grafo mandando in input il genere selezionato
        self._model.creaGrafo(genereSelezionato)
        # prendo i valori dei nodi e degli archi
        numeroDiNodi = self._model.getNumeroNodi()
        numeroDiArchi = self._model.getNumeroArchi()

        # artista con maggiore influenza
        artistaConMaggioreInfluenza = self._model.getArtistaMaggioreInfluenza()

        # archi top five
        architopfive = self._model.getTopFive()

        # prima di inserire valori ricordarsi di pulire il drodown
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))  # stampo numero di nodi
        self._view.txt_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))  # stampo numero di archi

        self._view.txt_result.controls.append(ft.Text(
            f"l'artista con più influenza è:{artistaConMaggioreInfluenza.getName()}"))  # stampo artista con maggiore influenza

        self._view.txt_result.controls.append(
            ft.Text(f"gli artisti più influenti sono:"))  # stampo artisti piu influenti
        for arco in architopfive:
            nome1 = arco[0].getName()  # primo nodo
            nome2 = arco[1].getName()  # secondo nodo
            peso = arco[2]["weight"]  # peso

            self._view.txt_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))  # stampo

        self._view.update_page()

    def handleCammino(self, e):
        pass
