a. Permettere all’utente di scegliere da un menù a tendina un anno tra tutti i possibili anni in cui 
ci sono stati avvistamenti (ordinati in senso CRESCENTE).
b. Popolare il menù a tendina Stato con tutti i possibili stati, prese dalla colonna “state” del db, 
relative agli avvistamenti nell’anno considerato (ordinati alfabeticamente). Il testo nel menu a tendina deve visualizzare
il nome esteso dello stato, preso dalla colonna “Name” del db relativa agli stati.
c. Facendo click sul bottone Crea Grafo, creare un grafo i cui vertici siano tutti gli avvistamenti presenti nella 
tabella “sighting” che siano avvenuti nell’anno selezionato dall’utente e nello stato indicato.
Il grafo è un grafo semplice, non-orientato, ed un arco fra due avvistamenti esiste se e solo se tali avvistamenti 
hanno la stessa Forma (colonna “shape” del db) e sono avvenuti ad una distanza inferiore a 100km.
Per calcolare la distanza in km tra due avvistamenti utilizzare il metodo distance_HV già fornito nella classe Sighting.
d. Stampare il numero di componenti connesse. Inoltre, identificare la componente connessa di dimensione maggiore,
e stamparne i nodi – includendo il dettaglio della città in cui è avvenuto l’avvistamento e la data.
