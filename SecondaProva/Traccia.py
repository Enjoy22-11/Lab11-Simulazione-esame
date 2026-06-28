#traccia
from dataclasses import dataclass

#dataclass
@dataclass
class Traccia:
    TrackId : int
    Name : str
    Bytes : int

#da mettere sempre dataclass
    def __hash__(self):
        return hash(self.TrackId)
    def __eq__(self, other):
        return self.TrackId == other.TrackId
    def __str__(self):
        return f"Traccia: {self.Name}, Id: {self.TrackId} (Bytes: {self.Bytes})"


    def dammiMB(self):
        return int(self.Bytes/1048576)

    def setMB(self, MB):
        self.Bytes = MB

    def getName(self):
        return self.Name
