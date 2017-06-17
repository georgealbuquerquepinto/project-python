from dao.banco import *
from model import *

class UnidadeDeSaudeDAO:
    def __init__(self):
        self.connection = createConnection()

    def insert(self, unitHealth):
        cursor = self.connection.cursor()		
        sql = 'INSERT INTO unidades(codigo, nome) VALUES (%s, %s)' % (unitHealth.cnes, unitHealth.nome)
        l = self.cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def searchAll(self):
        cursor = self.connection.cursor()
        sql = "SELECT count(*) AS num_vezes, codigo, nome FROM unidades GROUP BY codigo ORDER BY num_vezes DESC"
        cursor.execute(sql)
        result = []
        for row in cursor.fetchall():
            l = [row[1], row[2], row[3]]
            result.append(l)
        cursor.close()
        return result
