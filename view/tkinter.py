from tkinter import *
import model

class View:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()

        self.widget2 = Frame(master)
        self.widget2["pady"] = 20
        self.widget2.pack()

        self.widget3 = Frame(master)
        self.widget3["pady"] = 10
        self.widget3.pack()
        
        self.relatorio = Button(self.widget1, width=50, bg="#ccc")
        self.relatorio["text"] = "Gerar Relatório de Unidades mais Procuradas"
        self.relatorio["command"] = self.gerarRelatorio
        self.relatorio.pack()

        self.msg1 = Label(self.widget2, text="Informe suas coordenandas").pack()
        self.msg2 = Label(self.widget2, text="Latitude: ").pack()

        self.latitude = Entry(self.widget2)
        self.latitude.pack()
        
        self.msg3 = Label(self.widget2, text="Longitude: ").pack()

        self.longitude = Entry(self.widget2)
        self.longitude.pack()
        
        self.procurar = Button(self.widget2, bg="#ccc", text="Procurar")
        self.procurar["command"] = self.procurarUnidade        
        self.procurar.pack()

        self.msg3 = Label(self.widget3, text="Unidade de saúde mais próxima").pack()

        self.result = Text(self.widget3, width=45, height=5)
        self.result.pack()

    def gerarRelatorio():
        pass

    def procurarUnidade(self):
        longitude = self.getLongitude()
        latitude = self.getLatitude()
        netdata = model.NetDataModel()
        unitHealth = netdata.searchNearUnitHealth(longitude, latitude)
        self.show(unitHealth)

    def show(self, unSaude):
        if unSaude:
            self.result.delete('1.0', END)
            self.result.insert('1.0', unSaude.nome)

    def getLongitude(self):
        try:
            return float(self.longitude.get())
        except:
            return 0.0

    def getLatitude(self):
        try:
            return float(self.latitude.get())
        except:
            return 0.0
    
root = Tk()
View(root)
root.mainloop()
