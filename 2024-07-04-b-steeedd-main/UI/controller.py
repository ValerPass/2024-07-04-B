import warnings

import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._chosenState = None

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        anno = self._view.ddyear.value
        if anno is None:
            self._view.txt_result1.controls.append(ft.Text("Per creare un grafo devi prima selezionare un anno dal menù a tendina!"))
            warnings.warn("Per creare un grafo devi prima selezionare un anno dal menù a tendina!")
            self._view.update_page()
            return

        if self._chosenState is None:
            self._view.txt_result1.controls.append(ft.Text("Per creare un grafo devi prima selezionare uno stato dal menù a tendina!"))
            warnings.warn("Per creare un grafo devi prima selezionare uno stato dal menù a tendina!")
            self._view.update_page()
            return

        self._model.buildGraph(anno, self._chosenState)
        nN, nE = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nN}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nE}"))

        numConnComp = self._model.getNumConnComp()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {numConnComp} componenti connesse."))

        bestConnComp, lenght = self._model.getBestConnComp()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {lenght} nodi."))
        for n in bestConnComp:
            self._view.txt_result1.controls.append(ft.Text(f"{n}"))

        self._view.btn_path.disabled = False

        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        path, score = self._model.getBestPath()
        self._view.txt_result2.controls.append(ft.Text(f"Il cammino trovato ha totalizzato {score} punti."))
        self._view.txt_result2.controls.append(ft.Text(f"Il cammino è il seguente:"))
        for n in path:
            self._view.txt_result2.controls.append(ft.Text(f"{n} - duration: {n.duration} secondi."))

        self._view.update_page()


    def fillDDYears(self):
        years = self._model.getYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

    def disablePath(self, e):
        self._view.btn_path.disabled = True
        self._view.update_page()

    def fillDDStates(self, e):
        self._view.btn_path.disabled = True
        self._chosenState = None
        self._view.ddstate.value = None
        self._view.ddstate.options = []
        anno = self._view.ddyear.value
        if anno is None:
            self._view.ddstate.options = []
            return

        states = self._model.getStates(anno)
        for s in states:
            self._view.ddstate.options.append(ft.dropdown.Option(
                data=s,
                text=s,
                on_click=self.readDDState
            ))

        self._view.update_page()

    def readDDState(self, e):
        if e.control.data is None:
            self._chosenState = None
        else:
            self._chosenState = e.control.data




