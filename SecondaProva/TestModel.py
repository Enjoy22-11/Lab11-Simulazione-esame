#test model
from model.model import Model
myModel = Model()
myModel.creaGrafo("MPEG audio file")
Nnodes = myModel.getNumeroNodi()
Narchi = myModel.getNumeroArchi()
print(f"numero dei nodi pari a: {Nnodes} e {Narchi} archi")
