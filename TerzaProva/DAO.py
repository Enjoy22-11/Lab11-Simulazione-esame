#DAO

from database.DB_connect import DBConnect
from model.Costumer import Costumer
from model.Employee import Employee, Employee


class DAO():
    def __init__(self):
        pass

#trovo impiegati, nessun parametro da passare
    @staticmethod
    def getEmployees():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select e.EmployeeId as Id, e.FirstName as Name, e.LastName as Surname
                from employee as e """
        cursor.execute(query)
        for row in cursor:
            result.append(Employee(**row))
        cursor.close()
        conn.close()
        return result

#trovo nodi Passando un parametro
    @staticmethod
    def getNodi(EmployeeId):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select c.CustomerId as IdC, i.InvoiceDate as data, c.FirstName as Name, c.LastName as Surname, c.Company as azienda, c.Email as email
                   from customer as c, employee as e, invoice as i
                   where c.SupportRepId = e.EmployeeId
                   and e.EmployeeId = %s
                   and i.CustomerId = c.CustomerId"""
        cursor.execute(query, (EmployeeId,))
        for row in cursor:
            result.append(Costumer(**row))
        cursor.close()
        conn.close()
        return result

#trovo archi con il loro peso, no parametri
    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select i1.CustomerId as ID1, i2.CustomerId as ID2, sum((il1.UnitPrice*il1.Quantity)+(il2.UnitPrice*il2.Quantity)) as peso
                   from invoice as i1, invoiceline as il1, track as t1, invoice as i2, invoiceline as il2, track as t2
                   where t1.AlbumId = t2.AlbumId
                   and i1.CustomerId < i2.CustomerId
                   and il1.TrackId = t1.TrackId
                   and il2.TrackId = t2.TrackId
                   and i1.InvoiceId = il1.InvoiceId
                   and i2.InvoiceId = il2.InvoiceId
                   group by i1.CustomerId, i2.CustomerId"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["ID1"], row["ID2"], row["peso"]))
        cursor.close()
        conn.close()
        return result
