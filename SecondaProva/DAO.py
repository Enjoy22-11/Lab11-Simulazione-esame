#DAO
from database.DB_connect import DBConnect
from model.Traccia import Traccia


class DAO():
    def __init__(self):
        pass

#trovo tipi dei media, no parametri
    @staticmethod
    def GetMediaTipo():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select m.Name, m.MediaTypeId
                   from mediatype as m """
        cursor.execute(query)
        for row in cursor:
            result.append(row["Name"])
        cursor.close()
        conn.close()
        return result

#trovo TracceId, tracceNomi e Byte, passo parametro (tipoFile)
    @staticmethod
    def get_track(tipo_file):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.TrackId, t.Name, t.Bytes
                   from mediatype as m, track as t
                   where m.MediaTypeId = t.MediaTypeId and m.Name = %s """
        cursor.execute(query,(tipo_file,))
        for row in cursor:
            result.append(Traccia(**row))
        cursor.close()
        conn.close()
        return result


#trovo archi con il loro peso, no parametri (uso delle tuple top)
    @staticmethod
    def getNodiePeso():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select i1.TrackId as ID1, i2.TrackId as ID2, sum(i.Total) as Peso
                   from invoiceline as i1, invoiceline as i2, invoice as i
                   where i1.InvoiceId = i2.InvoiceId
                   and i1.InvoiceId  = i.InvoiceId
                   and i1.TrackId < i2.TrackId
                   group by i1.TrackId, i2.TrackId  """
        cursor.execute(query)
        for row in cursor:
            result.append((row["ID1"], row["ID2"], row["Peso"]))
        cursor.close()
        conn.close()
        return result

