from dataclasses import dataclass


@dataclass
class cantante:
    ArtistId: int
    Name: str
    def __hash__(self):
        return hash(self.ArtistId)
    def __eq__(self, other):
        return self.ArtistId == other.ArtistId
    def __str__(self):
        return f"Nome: {self.Name}, IdArtista: {self.ArtistId}"
    def getName(self):
        return self.Name
    def getIdArtista(self):
        return self.ArtistId