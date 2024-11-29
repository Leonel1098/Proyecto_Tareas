import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://halonzo_SQLLogin_1:m11obohszi@GestionTareas.mssql.somee.com/GestionTareas?driver=ODBC+Driver+18+for+SQL+Server'
    # SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sqlserver:Alonzo123@34.132.62.226/GestionTareas?driver=ODBC+Driver+17+for+SQL+Server'
    # SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://hector:Alonzo123@DESKTOP-OV27GS9/GestionTareas?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

from flask_socketio import SocketIO

# Inicializar SocketIO
socketio = SocketIO()