#Employee
from dataclasses import dataclass

#dataclass
@dataclass
class Employee:
    Id: int
    Name: str
    Surname: str
#da mettere sempre dataclass

    def __hash__(self):
        return hash(self.Id)

    def __eq__(self, other):
        return self.Id == other.Id

    def __str__(self):
        return f" {self.Name} {self.Surname} (ID: {self.Id})"




    def getId(self):
        return self.Id
