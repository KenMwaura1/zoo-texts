from sqlalchemy import Column, String, Integer, Date
from settings import Base


class Text(Base):
    __tablename__ = 'texts'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    statuscode = Column(Integer)
    number = Column(String)
    cost = Column(String)
    status = Column(String)
    messageid = Column(String)
    created_date = Column(Date)

    def __init__(self, message, statuscode, number, cost, status, messageid, created_date):
        self.message = message
        self.statuscode = statuscode
        self.number = number
        self.cost = cost
        self.status = status
        self.messageid = messageid
        self.created_date = created_date
