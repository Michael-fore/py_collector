import requests
from py_collector import Scheduler, Manager, Collector
from datetime import datetime
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base
    from sqlalchemy import Column, Integer, Float, DateTime, String
    from sqlalchemy.orm import sessionmaker
except:
    raise ImportError('Please install sqlaqlalchemy!, \n pip install SQLAlchemy')

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class WeatherDataPoint(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    temp = Column(Integer)
    windspeed = Column(String)

#https://api.weather.gov/gridpoints/FWD/59,23/forecast
class Weather(Collector):
    start_time = datetime.now()#to start immediatly
    scheduler = Scheduler(days=1/24, 
                        count=1, 
                        separator=1,
                        start_time = start_time)
    
    def upload(self):
        ''' Runs on schedule, and will only run if is_new 
            returns true'''
        r = requests.get('https://api.weather.gov/gridpoints/FWD/59,23/forecast')
        data = r.json()['properties']['periods']
        points = []
        for i in data:
            data_point = WeatherDataPoint(
                start_date=datetime.fromisoformat(i['startTime']),
                end_date=datetime.fromisoformat(i['endTime']),
                temp=i['temperature'],
                windspeed=i['windSpeed']
            )
            points.append(data_point)

        session.add_all(points)
        session.commit()

    def is_new(self):
        '''Evaluates if the data should be uploaded,
        if it only returns True, then it will just upload 
        on schedule.'''
        return True

if __name__ =='__main__':
    Base.metadata.create_all(engine)
    Weather().monitor()