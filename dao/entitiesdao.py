from dao.banco import *
from model import *

class UnidadeDeSaudeDAO:
    def __init__(self):
        self.connection = createConnection()

    def insert(self, unitHealth):
        cursor = self.connection.cursor()		
        sql = 'insert into unidades(codigo, nome) values (%s, %s)' % (unitHealth.cnes, unitHealth.nome)
        l = self.cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def searchAll(self):
        cursor = self.connection.cursor()
        sql = "select * from localizacaogeografica"
        cursor.execute(sql)
        result = []
        for row in cursor.fetchall():
            result.append(LocalizacaoGeografica(row[1], row[2]))
        cursor.close()
        return result
