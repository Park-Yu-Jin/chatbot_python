import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd
from PyKakao import DaumSearch
from PyKakao import KoGPT
import json
import urllib3
import base64
import wave
import pyaudio
from datetime import datetime
from urllib.request import urlopen

# api 검색
def search_job(a) :
    DB_CODE_SARAMIN = sqlite3.connect('C:/Users/gvti-000003/Desktop/DB Browser for SQLite/chatDB.db')
    DF_CODE = pd.read_sql("SELECT * FROM SARAMIN_CODE", DB_CODE_SARAMIN)
    sarmain_code = DF_CODE.set_index('NAME').T.to_dict()
    url_code = sarmain_code[a[0]]["CODE"]
    job_url = urlopen("https://oapi.saramin.co.kr/job-search?access-key=EEwRgLhOUhzxGYR7Io8PWu18yfwJsMbqW5hIc7e3vIheMLTP4sndG&bbs_gb=0&loc_cd=" + str(url_code) + "&count=110")
    result = BeautifulSoup(job_url,"html.parser")

    soup = json.loads(str(result))

    soup_2 = soup['jobs']['job']

    SELECT_DIC = {}
    SELECT_DIC.setdefault('url')
    SELECT_DIC.setdefault('company')
    SELECT_DIC.setdefault('position')
    SELECT_DIC.setdefault('location')
    SELECT_DIC.setdefault('experience')
    LIST_URL = []
    LIST_COMPANY = []
    LIST_POSITION = []
    LIST_LOCATION = []
    LIST_EXPERIENCE = []


    for i in range(len(soup_2)) :
        
        LIST_URL.append(soup_2[i]['url'])    
        LIST_COMPANY.append(soup_2[i]['company']['detail']['name'])
        LIST_POSITION.append(soup_2[i]['position']['title'])
        LIST_LOCATION.append(soup_2[i]['position']['location']['name'])
        LIST_EXPERIENCE.append(soup_2[i]['position']['experience-level']['name'])

        
    SELECT_DIC.update(url=LIST_URL)
    SELECT_DIC.update(company=LIST_COMPANY)
    SELECT_DIC.update(position=LIST_POSITION)
    SELECT_DIC.update(location=LIST_LOCATION)
    SELECT_DIC.update(experience=LIST_EXPERIENCE)

    DF_JOB = pd.DataFrame(SELECT_DIC)
    conn = sqlite3.connect('C:/Users/gvti-000003/Desktop/DB Browser for SQLite/chatDB.db')
    DF_JOB.to_sql('saramin', conn, if_exists='replace') 
    
    DB_JOB = pd.read_sql("SELECT * FROM saramin", DB_CODE_SARAMIN)
    DIC_JOB = DB_JOB.set_index('index').T.to_dict()
    print(DIC_JOB)
    
    return DIC_JOB
    
    
    
    
def search_edu(a) : #hrdbet
    time = datetime.today().strftime("%Y%m%d")
    DB_CODE_HRD = sqlite3.connect('C:/Users/gvti-000003/Desktop/DB Browser for SQLite/chatDB.db')
    DF_CODE = pd.read_sql("SELECT * FROM HRD_CODE", DB_CODE_HRD)
    LIST_HRD_CODE = DF_CODE.set_index('NAME').T.to_dict()
    print(LIST_HRD_CODE)

    url_code = LIST_HRD_CODE[a[0]]["CODE"]
    url_coed1 = str(url_code)[0:2]
    url_edu = "https://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=XML&authKey=HE20B1ChYQcpjDRrocNUmw77ctVvlkh5&pageNum=1&pageSize=100&srchTraStDt=" + time + "&srchTraEndDt=" + time +"&outType=1&sort=ASC&sortCol=TRNG_BGDE&"+ "srchTraArea1=" + url_coed1 + "&srchTraArea2=" + str(url_code)
    result = requests.get(url_edu).text
    soup_edu = BeautifulSoup(result,'lxml')
    items = soup_edu.find_all("address")
    items2 = soup_edu.find_all("title")
    items3 = soup_edu.find_all("traintarget")
    items4 = soup_edu.find_all("subtitle")
    items5 = soup_edu.find_all("titlelink")
    LIST_ADDRESS = []
    LSIT_TITLE = []
    LIST_TRAINTARGET = []
    LIST_SUBTITLE = []
    LIST_URL = []
    for i in items:
        LIST_ADDRESS.append(i.text)
    for i in items2:
        LSIT_TITLE.append(i.text)
    for i in items3:
        LIST_TRAINTARGET.append(i.text) 
    for i in items4:
        LIST_SUBTITLE.append(i.text)    
    for i in items5:
        LIST_URL.append(i.text)   
    
    HRD_DIC = {}
    HRD_DIC.setdefault('ADDRESS')
    HRD_DIC.setdefault('TITLE')
    HRD_DIC.setdefault('TRAINTAGET')
    HRD_DIC.setdefault('SUBTITLE')
    HRD_DIC.setdefault('URL')
    HRD_DIC.update(ADDRESS=LIST_ADDRESS)
    HRD_DIC.update(TITLE=LSIT_TITLE)
    HRD_DIC.update(TRAINTAGET=LIST_TRAINTARGET)
    HRD_DIC.update(SUBTITLE=LIST_SUBTITLE)
    HRD_DIC.update(URL=LIST_URL)

    DF_EDU = pd.DataFrame(HRD_DIC)
    conn = sqlite3.connect('C:/Users/gvti-000003/Desktop/DB Browser for SQLite/chatDB.db')
    DF_EDU.to_sql('HRD', conn, if_exists='replace')  

    DB_EDU = pd.read_sql("SELECT * FROM HRD", DB_CODE_HRD)
    DIC_EDU = DB_EDU.set_index('index').T.to_dict()
    print(DIC_EDU)

    return DIC_EDU
    

def search_ai(a) : #kogpt
    api = DaumSearch(service_key = "4eaad06ff2f678e1d527c6bb5793545a")
    api_2 = KoGPT(service_key = "4eaad06ff2f678e1d527c6bb5793545a")
    REST_API_KEY = '${4eaad06ff2f678e1d527c6bb5793545a}'


    DF_KOGPT = api.search_blog(a, dataframe=True)

    conn = sqlite3.connect('C:/Users/gvti-000003/Desktop/DB Browser for SQLite/chatDB.db')
    DF_KOGPT.to_sql('kogpt', conn, if_exists='replace')
    
    DB_KO = pd.read_sql("SELECT * FROM kogpt", conn)
    DIC_KO = DB_KO.set_index('index').T.to_dict()
    print(DIC_KO)
    return DIC_KO 
    
# 입력 자르기 함수 

def cut(a) :
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"
    accessKey = "5824f2ec-ede3-41f0-8831-4c103abbb2f1"
    analysisCode = "morp"
    

    requestJson = {  
        "argument": {
            "text": a,
            "analysis_code": analysisCode
        }
    }
        
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization" :  accessKey},
        body=json.dumps(requestJson)
    )
    b = eval(str(response.data,"utf-8"))
    print(b)
    #print(a['return_object']['sentence'])
    print(b['return_object']['sentence'][0]['morp'][0]['type'])

    nng_list=[]
    for i in range(len(b['return_object']['sentence'][0]['morp'])) :
        
        if b['return_object']['sentence'][0]['morp'][i]['type'] == "NNG" or "NNP" :
            nng_list.append(b['return_object']['sentence'][0]['morp'][i]['lemma'] )
    
    print(nng_list)   
    return nng_list

def select_city(a):
    
    DB_CITY = sqlite3.connect('C:/Users/gvti-000003/Desktop/DB Browser for SQLite/chatDB.db')
    DIF_CITY = pd.read_sql("SELECT name FROM city", DB_CITY)
    LIST_CITY = DIF_CITY.to_dict('list')
    print(LIST_CITY['name'])

    if len(a) > 1 : 
        filtered_list = [item for item in LIST_CITY['name'] if a in item]
        if filtered_list != None :  
            return filtered_list 
        return ""
    return ""

#음성
def record() : 
    RATE = 16000
    CHUNK = int(RATE / 10)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1 
    RECORD_SECONDS = 5

    with wave.open('output.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print('Recording...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('Done')

        stream.close()
        p.terminate()

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = "5824f2ec-ede3-41f0-8831-4c103abbb2f1"
    audioFilePath = "output.wav"
    languageCode = "korean"

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {    
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    
    sound_text = eval(str(response.data,"utf-8"))
    print(sound_text['return_object']['recognized'])
    sound_text_Result = sound_text['return_object']['recognized']
                    
    return sound_text_Result     