#TestModel
from model.model import Model
myModel = Model()
myModel.creaGrafo("Metal")
Nnodes = myModel.getNumeroNodi()
print(f"numero dei nodi pari a: {Nnodes}")
myModel.anni2023_2025()
for i in myModel.anni2023_2025():
    print(i)
for i in myModel.getEmployeers():
    print(i)
print(myModel.getCostumers(3))
