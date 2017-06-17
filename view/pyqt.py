from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from dao import *
import model

latitude = -13.024123
longitude = -50.6792927

maphtml = """
<!DOCTYPE html>
<html>
  <head>
    <style>
       #map {{
        height: 100%;
        width: 60%;
       }}
       html, body {{
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
      }}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      function initMap() {{
        var uluru = {{lat: {lat}, lng: {lon}}};
        var map = new google.maps.Map(document.getElementById('map'), {{
          zoom: 4,
          center: uluru
        }});
      }}
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAb1YqoLx0LC2GECyyOXhbCe2kDo8zRyCY&callback=initMap">
    </script>
  </body>
  </html>""".format(lat=latitude,lon=longitude)

class View(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])
        self.window = QWidget()
        self.window.setWindowTitle("LP3");

        self.latitude = QLineEdit()
        self.latitude.setPlaceholderText("Latitude")
        self.longitude = QLineEdit()
        self.longitude.setPlaceholderText("Longitude")
        self.search = QPushButton("Procurar")
        self.search.clicked.connect(self.procurarUnidade)
        self.searchAll = QPushButton("Gerar Relatório de Unidades mais Procuradas")
        self.searchAll.clicked.connect(self.procurarUnidades)

        self.web = QWebView(self.window)
        self.web.setMinimumSize(1200,500)
        self.web.page().mainFrame().addToJavaScriptWindowObject('self', self)
        self.web.setHtml(maphtml)

        #self.text = QTextEdit(self.window)

        self.layout = QVBoxLayout(self.window)
        #self.layout.addWidget(self.text)
        self.layout.addWidget(self.latitude)
        self.layout.addWidget(self.longitude)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.searchAll)
        self.layout.addWidget(self.web)

        self.window.show()
        self.exec_()

    def show(self, unSaude):
        if unSaude:
            maphtml = """
              <!DOCTYPE html>
              <html>
                <head>
                  <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                  <meta charset="utf-8">
                  <title>Info windows</title>
                  <style>
                    /* Always set the map height explicitly to define the size of the div
                     * element that contains the map. */
                    #map {{
                      height: 100%;
                      width: 60%;
                    }}
                    /* Optional: Makes the sample page fill the window. */
                    html, body {{
                      height: 100%;
                      width: 100%;
                      margin: 0;
                      padding: 0;
                    }}
                  </style>
                </head>
                <body>
                  <div id="map"></div>
                  <script>

                    // This example displays a marker at the center of Australia.
                    // When the user clicks the marker, an info window opens.

                    function initMap() {{
                      var uluru = {{lat: {lat}, lng: {lon}}};
                      var map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 12,
                        center: uluru
                      }});

                      var contentString = '<div id="content">'+
                          '<div id="siteNotice">'+
                          '</div>'+
                          '<h4 id="firstHeading" class="firstHeading">{nome}</h4>'+
                          '</div>';

                      var infowindow = new google.maps.InfoWindow({{
                        content: contentString
                      }});

                      var marker = new google.maps.Marker({{
                        position: uluru,
                        map: map,
                        title: '{nome}'
                      }});
                      marker.addListener('click', function() {{
                        infowindow.open(map, marker);
                      }});
                    }}
                  </script>
                  <script async defer
                  src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAb1YqoLx0LC2GECyyOXhbCe2kDo8zRyCY&callback=initMap">
                  </script>
                </body>
              </html>
            """.format(lat=unSaude.latitude,lon=unSaude.longitude,nome=unSaude.nome)
            self.web.setHtml(maphtml)
            print(unSaude.longitude)
            print(unSaude.latitude)

    def showAll(self, unidades):
        lista = ''
        for lin in unidades:
            for col in lin:
                lista += col + ','
            lista += '<br/>'

    def procurarUnidade(self):
        longitude = self.getLongitude()
        latitude = self.getLatitude()
        print(longitude)
        print(latitude)
        netdata = model.NetDataModel()
        unitHealth = netdata.searchNearUnitHealth(longitude, latitude)
        self.show(unitHealth)
        UnidadeDeSaudeDAO.insert(unitHealth)

    def procurarUnidades(self):
        netdata = model.NetDataModel()
        unitHealth = netdata.searchAllUnitHealth()
        self.showAll(unitHealth)
        units = UnidadeDeSaudeDAO.searchAll()
        self.showAll(units)
        
    def getLongitude(self):
        try:
            return float(self.longitude.text())
        except:
            return 0.0

    def getLatitude(self):
        try:
            return float(self.latitude.text())
        except:
            return 0.0

    @pyqtSlot(float, float, int)
    def polygoncomplete(self, lat, lng, i):
        if i == 0:
            self.text.clear()
        self.text.append("Point #{} ({}, {})".format(i, lat, lng))
