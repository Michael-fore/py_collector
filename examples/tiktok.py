from py_collector import Scheduler, Manager, Collector
from datetime import datetime
try:
    from pymongo.write_concern import WriteConcern
    from pymodm.connection import connect
    from pymodm import MongoModel, fields
    from bs4 import BeautifulSoup
    import requests
except:
    raise ImportError('Please make sure pymongo, pymodm, bs4,and requests\
        are installed to run this example')

connect("mongodb://localhost:27017/myDatabase", alias="my-app")

class TikTokUser(MongoModel):
    username = fields.CharField()
    followers = fields.CharField()
    likes = fields.CharField()
    following = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'

class TikTok(Collector):
    start_time = datetime.now() 

    scheduler = Scheduler(days=1, #every date
                        count=1, #try 1 times
                        separator=1, #not applicable
                        start_time = start_time) #start now

    def upload(self):
        ''' Runs on schedule, and will only run if is_new 
            returns true'''

        data = self.user_stats('gordonramsayofficial')
        user = TikTokUser.from_document(data)
        user.save()

    def is_new(self):
        '''Evaluates if the data should be uploaded,
        if it only returns True, then it will just upload 
        on schedule.'''
        return True
    
    def user_stats(self,user ='gordonramsayofficial'):
            r = self.user_raw(user)
            soup = BeautifulSoup(r.text,'html.parser')
            info = soup.find('h2',attrs={'class':'count-infos'})
            return {
                'following':info.find('strong',attrs={'title':'Following'}).text,
                'followers':info.find('strong',attrs={'title':'Followers'}).text,
                'likes':info.find('strong',attrs={'title':'Likes'}).text, 
                'username':user
            }

    def user_raw(self, user):
        headers={
            "authority": "m.tiktok.com",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
            "method": "GET",
            "scheme": "https",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": 'gzip, deflate, utf-8',
            "accept-language": "en-US,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1"
            }
        return requests.get(f'https://www.tiktok.com/@{user}?lang=en',headers=headers)
    
    
if __name__ =='__main__':
    TikTok().monitor()