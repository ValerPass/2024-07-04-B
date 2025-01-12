import copy
import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._years = DAO.getYears()
        self._graph = nx.Graph()
        self._bestPath = []
        self._bestScore = 0

    def getYears(self):
        return self._years

    def getStates(self, anno):
        states = DAO.getStates(anno)
        return states

    def buildGraph(self, anno, stato):
        self._graph.clear()
        nodes = DAO.getSightingsNodes(anno, stato.id)
        self._graph.add_nodes_from(nodes)
        for n in self._graph.nodes:
            for n2 in self._graph.nodes:
                if not self._graph.has_edge(n, n2) and n != n2:
                    if n.shape == n2.shape and n.distance_HV(n2) < 100:
                        self._graph.add_edge(n, n2)

    def getNumConnComp(self):
        return len(list(nx.connected_components(self._graph)))

    def getBestConnComp(self):
        connectedComponents = list(nx.connected_components(self._graph))
        connectedComponents.sort(key=lambda x: len(x), reverse=True)
        return connectedComponents[0], len(connectedComponents[0])


    def getBestPath(self):
        self._bestPath = []
        self._bestScore = 0
        parziale = []
        for n in self._graph.nodes:
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        if len(parziale) != 1:
            scoreAttuale = self.calcolaScore(parziale)
        else:
            scoreAttuale = 100

        if scoreAttuale > self._bestScore:
            self._bestScore = scoreAttuale
            self._bestPath = copy.deepcopy(parziale)

        lastNode = parziale[-1]
        for neighbor in self._graph.neighbors(lastNode):
            if self.controllo(parziale, neighbor) and neighbor.duration > lastNode.duration:
                parziale.append(neighbor)
                self._ricorsione(parziale)
                parziale.pop()


    def controllo(self, listOfNodes, nodoDaAggiungere):
        # Faccio un controllo per verificare che non ci siano più di due avvistamenti in parziale dello stesso mese
        # dell'avvistamento che sto aggiungendo, perchè nel caso significherebbe che aggiungendo l'avvistamento su cui
        # sto iterando, ci sarebbero più di tre avvistamenti dello stesso mese.
        # Non controllo la presenza di cicli nel cammino o altro perchè, aggiungendo sempre avvistamenti di durata strettamente crescente,
        # è impossibile che si vadano a creare cicli nel cammino, e quindi controllando questa cosa ridurrei l'efficienza dell'algoritmo.
        monthNodo = nodoDaAggiungere.datetime.month
        cnt = 0
        for node in listOfNodes:
            if node.datetime.month == monthNodo:
                cnt+=1

        if cnt > 2:
            return False
        else:
            return True


    def calcolaScore(self, listOfNodes):
        score = 100 * len(listOfNodes)
        for i in range(1, len(listOfNodes)):
            if listOfNodes[i].datetime.month == listOfNodes[i-1].datetime.month:
                score += 200

        return score

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
