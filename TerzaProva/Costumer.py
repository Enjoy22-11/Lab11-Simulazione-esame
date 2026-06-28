#Costumer
from dataclasses import dataclass

#dataclass
@dataclass
class Costumer:
    IdC: int
    data: str
    Name: str
    Surname: str
    azienda: str
    email: str

#da mettere sempre dataclass
    def __hash__(self):
        return hash(self.IdC)

    def __eq__(self, other):
        return self.IdC == other.IdC

    def __str__(self):
        return f" cliente numero: {self.IdC} nell'azienda: {self.azienda} (email: {self.email})"

#ID
    def getIdC(self):
        return self.IdC
#DATE
    def getData(self):
        return self.data
#Azienda
    def getAzienda(self):
        return self.azienda
#setAzienda
    def setAzienda(self, inputazienda):
        self.azienda =  inputazienda
#email
    def getEmail(self):
        return self.email
#Name
    def getNameCostumer(self):
        return self.Name
#surname
    def getSurnameCostumer(self):
        return self.Surname
