import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getallgenre()
        genreDD = []
        for g in genres:
            genreDD.append(ft.dropdown.Option(g))
        self._view._ddGenre.options= genreDD
        self._view.update_page()


    def handleCreaGrafo(self, e):
        genereSelezionato = self._view._ddGenre.value

        if genereSelezionato is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere"))
            self._view.update_page()
            return

        self._model.creaGrafo(genereSelezionato)
        numeroDiNodi = self._model.getNumeroNodi()
        numeroDiArchi = self._model.getNumeroArchi()
        artistaConMaggioreInfluenza = self._model.getArtistaMaggioreInfluenza()
        architopfive = self._model.getTopFive()



        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Il numero di nodi: {numeroDiNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Il numero di archi: {numeroDiArchi}"))
        self._view.txt_result.controls.append(ft.Text(f"l'artista con più influenza è:{artistaConMaggioreInfluenza.getName()}"))
        self._view.txt_result.controls.append(ft.Text(f"gli artisti più influenti sono:"))
        for arco in architopfive:
            nome1 = arco[0].getName()
            nome2 = arco[1].getName()
            peso = arco[2]["weight"]
            self._view.txt_result.controls.append(ft.Text(f"{nome1}---->{nome2}  (peso:{peso})"))

        self._view.update_page()


    def handleCammino(self,e):
        pass