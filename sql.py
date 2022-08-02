from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date 
from sqlalchemy import MetaData
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy import insert

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database

from datetime import datetime
import re

#from xlsxwriter.workbook import Workbook #For conversion from SQLite to Excel

Base = declarative_base()

class Report (Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    info = Column(Text)
    date = Column(Text)
    robot_ID = Column(Integer)
    problem = Column(Text)
    solution = Column(Text)

    def __repr__(self):
        return "(%s, %s, %s, Problem: %s, Solution: %s)" %(self.info, self.date, str(self.robot_ID), self.problem, self.solution)


class Sql ():
    def __init__(self):
        self.report = Report()
        self.engine = create_engine('sqlite:///database.db')
        self.metadata = MetaData()

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    def insert(self, stmt):
        converted_stmt = Report(info=stmt[0], date=stmt[1], robot_ID=stmt[2], problem=stmt[3], solution=stmt[4])
        self.session.add(converted_stmt)
        self.session.commit()
        self.session.flush()

    def query (self, column_search, keyword):
        keyword = self.__reg_exp(keyword)
        i = 0

        if column_search == "n":
            result = self.session.query(Report.id).all()

        elif column_search == "i":
            result = self.session.query(Report).filter(Report.info.like(keyword)).all()

        elif column_search ==  "d":
            result = self.session.query(Report).filter(Report.date.like(keyword)).all()

        elif column_search ==  "r":
            result = self.session.query(Report).filter(Report.robot_ID.like(keyword)).all()

        elif column_search ==  "p":
            result = self.session.query(Report).filter(Report.problem.like(reg)).all()

        elif column_search ==  "s":
            result = self.session.query(Report).filter(Report.solution.like(keyword)).all()

        else:
            print("Not inserted the correct column.")
            return None

        return result

    def __reg_exp(self, string):
        reg = "%" + string + "%"
        return reg
 
    def delete (self, _id):
        to_be_deleted = self.session.get(Report, _id)
        self.session.delete(to_be_deleted)
        self.session.commit()
        self.session.flush()


    def sql_to_list (self, columns_search):
        ret = []
        result = self.__query_column(columns_search)
        for row in result:
            sep = ''
            row = str(row)
            row = list(row)
            row = row[1:6]
            try:
                int(row[0])
                sep = sep.join(row)
                ret.append(sep)
            except ValueError:
                pass

        return ret

    def __query_column (self, column_search):
        ret = []
        if  column_search == "i":
            #result = self.session.query(Report).filter(Report.info == keyword)
            result = self.session.query(Report.info)
        elif column_search ==  "d":
            #result = self.session.query(Report).filter(Report.date == keyword)
            result = self.session.query(Report.date)
        elif column_search ==  "r":
            #result = self.session.query(Report).filter(Report.robot_ID == keyword)
            result = self.session.query(Report.robot_ID).all()
        elif column_search ==  "p":
            #result = self.session.query(Report).filter(Report.problem == keyword)
            result = self.session.query(Report.problem)
        elif column_search ==  "s":
            #result = self.session.query(Report).filter(Report.solution == keyword)
            result = self.session.query(Report.solution)
        return result

    def PrintDatabase (self, result):
        idx = 0
        if result == None:
            result = self.GetDatabase()

        for row in result:
            Id = '[' + str(row.id) + ']'
            print(Id + str(row))
            idx += 1

        return result

    def NumberOfElements (self):
        idx = 0
        result = self.GetDatabase()
        for row in result:
            idx += 1

        print("There are " + str(idx) + " elements")
        return idx


    def GetDatabase (self):
        return self.session.query(Report).all()
