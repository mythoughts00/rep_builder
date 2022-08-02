import pandas as pd
import numpy as np
from datetime import datetime
import platform
import sys
import os
import sql

"""
420434 Sono il numero di log
I robot con il numero seriale che inizia con '1', hanno un lifting tray piu rumoroso
11954 Ha il sensore laterale  sinistro che balla
"""

list_of_robot = ["01147", "01247", "01281", "01329", "01380", "01431", "01537", "01560", "01709", "11948", "11949", "11952", "11953", "11954", "11955", "11956", "11957", "11958", "11959", "11960", "11961", "11962", "11963", "11964", "11966", "11967", "11968", "11970", "11972", "11973", "11974", "11975", "11976", "11978", "11979", "11980", "11981", "11983", "11985", "11987", "11988", "11989", "11991", "11992", "11993", "11994", "11995", "11996", "11997", "11999", "12000", "12001", "12002", "12003", "12005", "12006", "12007", "12008", "12009", "12010", "12011", "12012", "12015", "12016", "12017", "12018", "12019", "12021", "12022", "12023", "12024", "12025", "12026", "12027", "12028", "12029", "12030", "12035", "12036", "12037", "12038", "12039", "12040", "12041", "12042", "12043", "12044", "12045", "12046", "12047", "12048", "12049", "12050", "12059", "12061", "12063", "12064", "12065", "12066", "12067", "12068", "12069", "12070", "12071", "12072", "12073", "12074", "12075", "12078", "12079", "12081", "21002", "21003", "21005", "21008", "21010", "21016", "21019", "21020", "21021", "21022", "21023", "21024", "21025", "21038", "21051", "21060", "21062", "21072", "21075", "21076"]


columns_name = ["Report ID", "Info", "Date", "Robot ID", "Problem", "Solution"]

def main ():
    cur = []
    db = sql.Sql()

    while True:
        action = input("# ")

        if action == "get":
            column_search = input("Search by: info, date, robot_id, problem, solution: [i/d/r/p/s]: ")
            keyword = input("What do you wanna find? ")
            results = db.query(column_search, keyword)            
            db.PrintDatabase(results)

        elif action == "add":
            stmt = build_report(db)
            if stmt != None:
                db.insert(stmt)

        elif action == "read" or action == "l":
            db.PrintDatabase(None)

        elif action == "remain":
            print_remaining(db)

        elif action == "delete":
            delete_report(db)
            pass

        elif action == "cls":
            if platform.system() == "Windows":
                os.system("cls")

            elif platform.system() == "Linux":
                os.system("clear")

        elif action == "elements":
            db.NumberOfElements()

        elif action == "excel":
            filename = input("File name in which you want to export the file: ")
            data = db.GetDatabase()
            db_to_excel(data, filename)
            print("Exported in '" + filename + ".xlsx'")

        elif action == "esci" or action == "q":
            break
        
        else:
            help_instruction()
    return 0
 
def build_report (db):
    report_id = 1
    Date = datetime.now()
    Date = Date.strftime('%d/%m/%Y %H:%M')
    Robot_id = input("Immetti ID del robot in questione: ")

    
    if len(Robot_id) == 5:
        try:
            Robot_id = int(Robot_id)

        except ValueError:
            print("ID del robot non e' un numero intero")
            exit(1)

    else:
        if Robot_id != "-":
            print("ID del robot incorretto. (ID deve essere di 5 cifre)")
            exit(1)

    Info = input("Manutenzione eseguita: Ordinaria o Straordinaria. [O/s] ")
    if Info == "s" or Info == "S":
        Info = "STRAORDINARIO" 
    else:
        Info = "ORDINARIO"

    if Info != "ORDINARIO":
        Problem = input("Descrizione del problema: ")
        Solution = input("Soluzione del problema: ")
    else:
        Problem = "-"
        Solution = maintenance()
        if Solution == None:
            return None

    #report = Report(info=Info, date=Date, robot_ID=Robot_id, problem=Problem, solution=Solution)
    return (Info, Date, Robot_id, Problem, Solution)


def maintenance ():
    action = input("Manutenzione Giornaliera, Settimanale, Mensile, Trimestrale, Semestrale, Annuale? [g/s/m/t/S/a]")
    if action == "g":
        solution = "GIORNALIERO: Controllato che i robot abbiano piu del 50% di batteria"

    elif action == "s":
        solution = "SETTIMANALE: Pulizia della camera superiore"

    elif action == "m":
        solution = "MENSILE: Controllo della carrozzeria, motore di elevamento, LED, Presa di carica. Pulizia del sensore di rilevamento ostacoli"

    elif action == "t":
        solution = "TRIMESTRALE: Pulizia della camera inferiore"

    elif action == "S":
        solution = "SEMESTRALE: Pulizia interna del robot. Controllo delle emergenze e della costa di sicurezza. Controllo che sensore di rilevamento ostacoli funzioni a dovere"

    elif action == "a":
        solution = "ANNUALE: Controllo e ingrassaggio cuscinetto"

    else:
        print("Nessuna delle possibili manutenzioni è stata scelta")
        return

    return solution

def print_remaining (db):
    robot_id = db.sql_to_list("r")
    date = db.sql_to_list("d")
    
    pass

def delete_report (db):
    _id = input("Id of element ind database to delete: ")
    db.delete(_id)

def db_to_excel (data, filename):
    filename = filename + ".xlsx"

    data_list = [to_dict(item) for item in data]
    df = pd.DataFrame(data_list)

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer)
    writer.save()

def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)

    return rtn_dict

def test (db):
   # ret = db.sql_to_list("r")
   db.query("n", "")
    #print(ret)



def help_instruction ():
    print("'get': Search database through pattern.")
    print("'add': Insert new report into database.")
    print("'read' or 'l': Read the whole database.")
    print("'delete': Delete instance from database.")
    print("'elements': Get number of elements in database.")
    print("'cls': Clear screen")
    print("'excel': Export database in excel file")
    print("'q': Quit.")
    print("'help': Show this message.")

main()
