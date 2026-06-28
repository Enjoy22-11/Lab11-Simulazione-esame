#DAO
from database.DB_connect import DBConnect
from model.cantante import cantante


class DAO():
    def __init__(self):
        pass

#cerco i generi musicali, no parametri
    @staticmethod
    def getGenereMusicale():
        conn =DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select name, genreId
                   from genre"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["name"])
        cursor.close()
        conn.close()
        return result

#ottengo gli artisti, con parametro (genere)
    @staticmethod
    def getMusician(nomeGenere):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct a2.Name, a2.ArtistId
                   from track as t, genre as g, album as a, artist as a2
                   where g.GenreId = t.GenreId and t.AlbumId=a.AlbumId and a.ArtistId = a2.ArtistId
                   and g.Name = %s"""
        cursor.execute(query,(nomeGenere,))
        for row in cursor:
            result.append(cantante(**row))
        cursor.close()
        conn.close()
        return result

#Metto la base per gli archi, no paramteri (ATTENZIONE USO DI DIZIONARIO associazione di valore a lista)
    @staticmethod
    def getBaseArchi():
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """select distinct i2.CustomerId, a.ArtistId
                   from invoiceline as i1, invoice as i2, track as t, album as a
                   where i2.InvoiceId = i1.InvoiceId and i1.TrackId = t.TrackId and a.AlbumId = t.AlbumId """
        cursor.execute(query)
        for row in cursor:
            idCostumer = row["CustomerId"]
            idArtist = row["ArtistId"]
            if idCostumer not in result:
                result[idCostumer] = []
            result[idCostumer].append(idArtist)
        cursor.close()
        conn.close()
        return result

#Metto la base per i pesi, no paramteri (ATTENZIONE USO DI DIZIONARIO)

    @staticmethod
    def getPopolarita():
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId, count(a.ArtistId ) as popolarita
                   from invoiceline as i1, track as t, album as a
                   where a.AlbumId  = t.AlbumId and t.TrackId = i1.TrackId
                   group by a.ArtistId"""
        cursor.execute(query)
        for row in cursor:
            idArtist = row["ArtistId"]
            popolarita = row["popolarita"]
            result[idArtist]=popolarita
        cursor.close()
        conn.close()
        return result
