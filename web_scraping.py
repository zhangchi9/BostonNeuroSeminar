import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

# create Pandas dataframe to store the data
talks_columns = ['start','end', 'Speaker(s)','Title','Title_text','url', 'location']
talks = pd.DataFrame(columns = talks_columns)

# bcs mit events 
row = 0
for i in range(3):
    print(i)
    page = requests.get("https://bcs.mit.edu/news-events/events?page="+str(i))
    soup = BeautifulSoup(page.content,'html.parser')
    TalkinfoAll = soup.select("div.node-content")
    for j in range(len(TalkinfoAll)):
        Talkinfo = TalkinfoAll[j]
        
        # find the title and url
        title_tag = Talkinfo.select("h3.node-title")[0].a
        talks.loc[row, 'Title_text'] = title_tag.get_text()
        talks.loc[row, 'url'] = 'https://bcs.mit.edu'+ title_tag['href']
        title = str(title_tag)
        talks.loc[row, 'Title'] = title[0:9]+'https://bcs.mit.edu'+title[9:]
        
        # find the locations 
        subpage = requests.get(talks.loc[row, 'url'])
        subsoup = BeautifulSoup(subpage.content,'html.parser')
        talks.loc[row,'location'] = subsoup.select("var.atc_location")[0].get_text()
        
        # find the speaker info, and speaker url if exists. 
        speaker_tag = Talkinfo.select("div.textformatter-list")
        if len(speaker_tag) != 0:
            talks.loc[row, 'Speaker(s)'] = speaker_tag[0].get_text()
        else:
            talks.loc[row, 'Speaker(s)'] = 'TBA'
            
        # find the datatime and seperate them     
        talks.loc[row, 'start'] = str(datetime.datetime.strptime(Talkinfo.select("var.atc_date_start")[0].get_text(),'%Y/%m/%d %I:%M:%S %p').strftime('%Y-%m-%dT%H:%M:%S'))
        talks.loc[row, 'end'] = str(datetime.datetime.strptime(Talkinfo.select("var.atc_date_end")[0].get_text(),'%Y/%m/%d %I:%M:%S %p').strftime('%Y-%m-%dT%H:%M:%S'))
        row = row + 1

def replace_noon(datetime):
    datetime = datetime.split(" ")
    time = datetime[3]
    if time == 'noon': 
        time = '12:00pm'
        
    return datetime[0]+' '+datetime[1]+' '+datetime[2]+' '+time

# harvard events 
page = requests.get("http://cbs.fas.harvard.edu/resources/events")
soup = BeautifulSoup(page.content,'html.parser')
TalkinfoAll = soup.select("div.view-content")[1]
TalkinfoAll = TalkinfoAll.find_all("div", recursive=False)
for j in range(len(TalkinfoAll)):
        Talkinfo = TalkinfoAll[j]
        
        # find the title and url
        title_tag = Talkinfo.select("h3.featuredtext")[0].a
        talks.loc[row, 'Title_text'] = title_tag.get_text()
        talks.loc[row, 'url'] = 'http://cbs.fas.harvard.edu'+ title_tag['href']
        title = str(title_tag)
        talks.loc[row, 'Title'] = title[0:9]+'http://cbs.fas.harvard.edu/'+title[9:]
        
        # find the locations 
        talks.loc[row,'location'] = list(list(Talkinfo.children)[5].children)[2]
        
        # find the speaker info, and speaker url if exists. 
        talks.loc[row, 'Speaker(s)'] = list(Talkinfo.children)[4]
            
        # find the datatime and seperate them     
        tmp = replace_noon(Talkinfo.select("span.date-display-single")[0].get_text())
        tmp = '2018 '+ tmp
        talks.loc[row, 'start'] = str(datetime.datetime.strptime(tmp, '%Y %a %d %b %I:%M%p').strftime('%Y-%m-%dT%H:%M:%S')) 
        row = row + 1

talks = talks.replace('\n','', regex=True)
talks.end.fillna(talks.start, inplace=True)
for i in range(len(talks)): 
    event = {
   'summary': talks.loc[i, 'Speaker(s)'] +': '+talks.loc[i, 'Title_text'],
   'location': talks.loc[i, 'location'],
   'description': 'For details: link here: '+ talks.loc[i, 'url'],
   'start': {
     'dateTime': talks.loc[i, 'start'],
     'timeZone': 'America/New_York',
   },
   'end': {
     'dateTime': talks.loc[i, 'end'],
     'timeZone': 'America/New_York',
   },
   }
    print('*'*100)
    print(event)
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
      creds = tools.run_flow(flow, store)
      service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    Id = '9eg8v70ea9nmondpdua3ppicrs@group.calendar.google.com'
    event = service.events().insert(calendarId=Id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))