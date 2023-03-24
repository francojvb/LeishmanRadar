class Prediction:
    def __init__(self, date, case):
        self.date   =   date
        self.case   =   case



    def toDBCollection(self):
        return {
            'date':self.date,
            'case': self.case
        } 