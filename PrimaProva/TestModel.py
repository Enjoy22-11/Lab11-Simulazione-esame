#Test model
from model.model import Model
myModel = Model()
myModel.creaGrafo("Metal")
Nnodes = myModel.getNumeroNodi()
print(f"numero dei nodi pari a: {Nnodes}")
