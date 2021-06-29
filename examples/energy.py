from datetime import datetime
from py_collector import Scheduler, Manager, Collector
try:
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
except:
    raise ImportError('Please install requests, BeautifulSoup4, and pandas to run this example')

class Energy(Collector):
    start_time = datetime.now()#to start immediatly

    scheduler = Scheduler(minutes=1, #every minute
                        count=2, #try 3 times
                        separator=2, #two seconds between tries
                        start_time = start_time)
    first_run = True
    last_update = None

    def upload(self):
        ''' Runs on schedule, and will only run if is_new 
            returns true'''
        df = pd.read_html(self.get_site.text)[0]
        title = 'ercot_dam_clearing_'+self.last_update.strftime('%m_%d_%Y')+'.csv'
        file = open(title,'w')
        df.to_csv(file)

    def is_new(self):
        '''Evaluates if the data should be uploaded,
        if it only returns True, then it will just upload 
        on schedule.'''
        if self.first_run:
            #first run load whatever is there
            self.first_run = False
            self.last_update = self.get_last_changed()
            return True
        else:
            #if it has changed since we last updated, download
            last_changed = self.get_last_changed()
            if self.last_update < last_changed:
                self.last_update = last_changed
                return True
            else:
                return False

    def get_site(self):
        return requests.get('http://www.ercot.com/content/cdr/html/actual_loads_of_forecast_zones')

    def soup(self):
        r = self.get_site()
        return BeautifulSoup(r.text,'html.parser')

    def get_last_changed(self):
        soup = self.soup()
        last_change = soup.find('div',attrs={'class':'schedTime rightAlign'})
        last_change = last_change.text.split('Time:')[1].lstrip()
        return datetime.strptime(last_change,'%b %d, %Y %H:%M')

if __name__ =='__main__':
    Energy().monitor()