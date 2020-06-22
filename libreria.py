import os, time, sys, mysql.connector, rm, random
from array import *
from sqlalchemy import create_engine
from mysql.connector import Error
import mysql.connector

ipdatabase = ''


db = 'bottelegram'
user = '' # nome utente del db
password = '' # Password del db 

def update(tabella, campodamodificare, valoredaimmettere, campoquando, valorequando):
    query = "update " + str(tabella) + " set "+ str(campodamodificare) + " = '" + str(valoredaimmettere) + "' where " + str(campoquando) +"='" + str(valorequando) + "'"
    
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()

def insertdue(tabella, campi, valori):
    sql_select_Query = "insert into " + str(tabella) + "("
    y = 0
    for x in campi:
        sql_select_Query += str(x)
        y+=1
        if len(campi) != y: #serve per dire alla macchina di non aggiungere la virgola all'ultimo elemento
            sql_select_Query += ", "
    
    sql_select_Query += ") values ("
    y = 0
    for x in valori:
        y+=1
        sql_select_Query += "'" + str(x) + "'"
        if len(valori) != y:
            sql_select_Query += ", "

    sql_select_Query += ")"
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    cursor.close()



def selectcondizionato(tabella, campo, valore, campo2):#ritorna un valore di una casella che si specifica
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    query = "select " + str(campo2) + " from " + str(tabella) + " where " + str(campo) + "='" + str(valore) + "';"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    risultato = cursor.rowcount
    cursor.close()
    return records


def selectcondizionatodato(tabella, campo, valore):
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    query = "select * from " + str(tabella) + " where " + str(campo) + "='" + str(valore) + "';"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    risultato = cursor.rowcount
    cursor.close()
    #return risultato
    return records


def select(tabella):
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    query = "select * from " + str(tabella) + " where 1"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    risultato = cursor.rowcount
    cursor.close()
    return risultato


def delete(tabella):
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    sql_select_Query = "DELETE FROM `" + str(tabella) + "` WHERE 1"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    cursor.close()

def deletecondizionato(tabella, campo, valore):
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    sql_select_Query = "DELETE FROM `" + str(tabella) + "` WHERE " + str(campo) + " = '" + str(valore) +"'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    connection.commit()
    cursor.close()

def selectcompleta(tabella):#ritorna un valore di una casella che si specifica
    connection = mysql.connector.connect(host=ipdatabase, database=db, user=user, password=password)
    query = "select * from " + str(tabella) + ";"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    risultato = cursor.rowcount
    cursor.close()
    return records
