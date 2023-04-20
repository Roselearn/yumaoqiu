import datetime
import smtplib
import time
from email.mime.text import MIMEText
import urllib3
urllib3.disable_warnings()
import requests
import re
import urllib3
urllib3.disable_warnings()
session = requests.session()
session.trust_env = False
import ddddocr
import calendar
proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8888'

}
def send_mail(title, content):
    mail_host = 'smtp.qq.com'
    mail_user = '2858856216'
    mail_pass = 'tvismrphwvlzdeah'
    sender = '2858856216@qq.com'
    receivers = ['2304090644@qq.com']
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误

def getCSRF(session,url):
    url_homepage = url
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/poss/lgttoken.jsp?dest=ISS',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = session.get(url = url_homepage,headers = headers,verify=False)
    CSRF = re.search('input type="hidden" name="CSRFToken" value="(.*?)" />', r.text).group(1)
    return CSRF
CSRF = getCSRF(session,url='https://www40.polyu.edu.hk/poss/secure/login/loginhome.do')
print(CSRF)
def login(session,CSRF):
    url_login = 'https://www40.polyu.edu.hk/poss/j_security_check'
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/poss/secure/login/loginhome.do',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Origin':'https://www40.polyu.edu.hk'
    }
    data = {
        'otheruser':'N',
        'j_username':'22048817g',
        'j_password':'Rose996926',
        'buttonAction':'loginButton',
        'CSRFToken': CSRF
    }
    r= session.post(url = url_login,headers = headers,data = data,verify=False)
    print('login11111111111111111111111111111111')


def login_captcha(session,t,captcha,CSRF):
    url_login = 'https://www40.polyu.edu.hk/poss/j_security_check'
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/poss/secure/login/loginhomeerror.do',
        'displayCaptcha':'true',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Origin':'https://www40.polyu.edu.hk'
    }
    data = {
        'otheruser':'N',
        'j_username':'22048817g',
        'j_password':'Rose996926',
        'buttonAction':'loginButton',
        'BDC_VCID_validBookCaptcha':t,
        'BDC_BackWorkaround_validBookCaptcha':'1',
        'captchaCode':captcha,
        'CSRFToken':CSRF
    }
    r= session.post(url = url_login,headers = headers,data = data,verify=False)
    print('login22222222222222222222222222222')
    return r



def search(session,date,CSRF):
    url_badmintion = 'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/timetable.json?CSRFToken='+CSRF
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book.do',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Origin':'https://www40.polyu.edu.hk',
    }
    data  ={
        'CSRFToken':CSRF,
        'fbUserId':'426815',
        'bookType':'INDV',
        'dataSetId':'18',
        'actvId':'2',
        'searchDate':date,
        'ctrId':'',
        'facilityId':'',
        'showCourtAreaDetails':'true'
    }
    r = session.post(url = url_badmintion,headers = headers, data = data,verify=False)
    return r

#def make_booking(session, date, CSRF,):
def get_t(session ,CSRF,date,facilityId,startDateTime,endDateTime):
    url1 = 'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book_submit.do'
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_ntce/ntce.do',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    #r3 = session.get(url = url1,headers = headers,verify=False)

    url_make_book_do = 'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book.do?fbUserId=426815&bookType=INDV&dataSetId=18&actvId=2&searchDate=27+Feb+2023&ctrId=&facilityId='
    headers1 = {
        'Host':'www40.polyu.edu.hk',
        'Referer': 'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book.do?fbUserId=426815&bookType=INDV&dataSetId=18&actvId=2&searchDate=27+Feb+2023&ctrId=&facilityId=',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Origin':'https://www40.polyu.edu.hk',
    }
    data1  ={
        'extlPtyDclrId':'',
        'dataSetId':'18',
        'actvId':'2',
        'onBehalfOfFbUserId':'',
        'byPassQuota':'false',
        'byPassChrgSchm':'false',
        'byPassBookingDaysLimit':'false',
        'repeatOccurrence':'false',
        'grpFacilityIds':'',
        'searchFormString':'fbUserId=426815&bookType=INDV&dataSetId=18&actvId=2&searchDate=27+Feb+2023&ctrId=&facilityId=',
        'boMakeBookFacilities[0].ctrId':'',
        'boMakeBookFacilities[0].facilityId':'234',
        'boMakeBookFacilities[0].startDateTime':'27 Feb 2023 07:30',
        'boMakeBookFacilities[0].endDateTime':'27 Feb 2023 08:30',
        'CSRFToken':CSRF }

    #No.4 BMT04
    #date 30 Feb 2023
    """
    30+Feb+2023
    30 Feb 2023 08:30
    30 Feb 2023 09:30
    """
    date_format = date.replace(' ', '+')
    date_time_format_start = date + ' ' + startDateTime
    date_time_format_end = date + ' ' + endDateTime

    data2  ={
        'extlPtyDclrId':'',
        'dataSetId':'18',
        'actvId':'2',
        'onBehalfOfFbUserId':'',
        'byPassQuota':'false',
        'byPassChrgSchm':'false',
        'byPassBookingDaysLimit':'false',
        'repeatOccurrence':'false',
        'grpFacilityIds':'',
        'searchFormString':f'fbUserId=426815&bookType=INDV&dataSetId=18&actvId=2&searchDate={date_format}&ctrId=&facilityId=',
        'boMakeBookFacilities[0].ctrId':'',
        'boMakeBookFacilities[0].facilityId':{facilityId},
        'boMakeBookFacilities[0].startDateTime': {date_time_format_start},
        'boMakeBookFacilities[0].endDateTime': {date_time_format_end},
        'CSRFToken':CSRF }

  #  r1 = session.post(url = url_make_book_do, data = data1, headers = headers1, verify=False)
    r1 = session.post(url=url_make_book_do, data=data2, headers=headers1, verify=False)
    #r2 = session.get(url=url1,headers=headers)
    t = re.search('c=validBookCaptcha&amp;t=(.*?)"', r1.text).group(1)
    ctrId = re.search('ctrId" type="hidden" value="(.*?)"', r1.text).group(1)
    centerName = re.search('centerName" type="hidden" value="(.*?)"', r1.text).group(1)
    facilityId = re.search('facilityId" type="hidden" value="(.*?)"', r1.text).group(1)
    facilityName = re.search('facilityName" type="hidden" value="(.*?)"', r1.text).group(1)
    startDateTime = re.search('startDateTime" value="(.*?)"', r1.text).group(1)
    endDateTime = re.search('endDateTime" value="(.*?)"', r1.text).group(1)
    return t,ctrId,centerName,facilityId,facilityName,startDateTime,endDateTime


def get_t_login(session):

    url_make_book_do = 'https://www40.polyu.edu.hk/poss/secure/login/loginhomeerror.do'
    headers1 = {
        'Host':'www40.polyu.edu.hk',
        'Referer': 'https://www40.polyu.edu.hk/poss/secure/login/loginhomeerror.do',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    r1 = session.get(url=url_make_book_do, headers=headers1, verify=False)
    print(r1)
    print(r1.text)
    t = re.search('c=validBookCaptcha&amp;t=(.*?)"', r1.text).group(1)
    return t

def get_captcha(t,session):
    url = 'https://www40.polyu.edu.hk/starspossfbstud/botdetectcaptcha?get=image&c=validBookCaptcha&t='+t
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book_submit.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

    }
    res = session.get(url = url,headers = headers)
    index = 0
    img_name = str(index + 1) + '.jpg'
    with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(res.content)
        file.flush()
    file.close()  # 关闭文件
    print('第%d张图片下载完成' % (index + 1))

def get_captcha_login(t,session):
    url = 'https://www40.polyu.edu.hk/poss/botdetectcaptcha?get=image&c=validBookCaptcha&t='+t
    headers = {
        'Referer':'https://www40.polyu.edu.hk/poss/secure/login/loginhomeerror.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

    }
    res = session.get(url = url,headers = headers)
    index = 1
    img_name = str(index + 1) + '.jpg'
    with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
        file.write(res.content)
        file.flush()
    file.close()  # 关闭文件
    print('第%d张图片下载完成' % (index + 1))

def scan_captcha():
    ocr = ddddocr.DdddOcr()
    with open(r'C:\Users\李博\Desktop\jiaoben\1.jpg', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    print(res)
    return res

def scan_captcha_login():
    ocr = ddddocr.DdddOcr()
    with open(r'C:\Users\李博\Desktop\jiaoben\2.jpg', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    print(res)
    return res



def make_booking(session,Captcha,CSRF,t, ctrId, centerName, facilityId, facilityName, startDateTime, endDateTime,date):
    date_format = date.replace(' ', '+')
    url = 'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book_submit.do'
    headers = {
        'Host':'www40.polyu.edu.hk',
        'Origin':'https://www40.polyu.edu.hk',
        'Referer':'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book_submit.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data1 = {
                'dataSetId':'18',
                'boBookingType.id':'1',
                'boBookingType.value':'INDV',
                'boBookingMode.value':'SPORT',
                'boBookingMode.id':'1',
                'userRefNum':'',
                'fbUserId':'426815',
                'grpFacilityIds':'',
                'repeatOccurrence':'false',
                'startDate':'',
                'startTime':'',
                'endDate':'',
                'endTime':'',
                'dayOfWeeks':'',
                'functionsAvailable':'false',
                'brcdNo':'',
                'phone':'',
                'onBehalfOfFbUserId':'',
                'byPassQuota':'false',
                'byPassChrgSchm':'false',
                'byPassBookingDaysLimit':'false',
                'searchFormString': f'fbUserId=426815&bookType=INDV&dataSetId=18&actvId=2&searchDate={date_format}&ctrId={ctrId}&facilityId=',
                'extlPtyDclrId':'',
                'boMakeBookFacilities[0].ctrId': ctrId,
                'boMakeBookFacilities[0].centerName': centerName,
                'boMakeBookFacilities[0].facilityId' : facilityId,
                'boMakeBookFacilities[0].facilityName': facilityName,
                'boMakeBookFacilities[0].startDateTime': startDateTime,
                'boMakeBookFacilities[0].endDateTime': endDateTime,
                'BDC_VCID_validBookCaptcha':t,
                'BDC_BackWorkaround_validBookCaptcha':'1',
                'captchaCode':Captcha,
                'declare':'on',
                'CSRFToken':CSRF
    }
    data2 = {
        'dataSetId': '18',
        'boBookingType.id': '1',
        'boBookingType.value': 'INDV',
        'boBookingMode.value': 'SPORT',
        'boBookingMode.id': '1',
        'userRefNum': '',
        'fbUserId': '426815',
        'grpFacilityIds': '',
        'repeatOccurrence': 'false',
        'startDate': '',
        'startTime': '',
        'endDate': '',
        'endTime': '',
        'dayOfWeeks': '',
        'functionsAvailable': 'false',
        'brcdNo': '',
        'phone': '',
        'onBehalfOfFbUserId': '',
        'byPassQuota': 'false',
        'byPassChrgSchm': 'false',
        'byPassBookingDaysLimit': 'false',
        'searchFormString': 'fbUserId=426815&bookType=INDV&dataSetId=18&actvId=2&searchDate=27+Feb+2023&ctrId=&facilityId=',
        'extlPtyDclrId': '',
        'boMakeBookFacilities[0].ctrId': '103',
        'boMakeBookFacilities[0].centerName': 'Block X',
        'boMakeBookFacilities[0].facilityId': '234',
        'boMakeBookFacilities[0].facilityName': 'Badminton Court No.14',
        'boMakeBookFacilities[0].startDateTime': '27 Feb 2023 07:30',
        'boMakeBookFacilities[0].endDateTime': '27 Feb 2023 08:30',
        'BDC_VCID_validBookCaptcha': t,
        'BDC_BackWorkaround_validBookCaptcha': '1',
        'captchaCode': Captcha,
        'declare': 'on',
        'CSRFToken': CSRF
    }
    res = session.post(url = url,headers = headers, data = data1, verify = False)
    return res

chang = []
from_time = []
toTime = []
facilityIds = []
def search_court(session,CSRF):
    for i in range(10):
        title = []
        now = datetime.datetime.now()
        day_plus = now + datetime.timedelta(days=7)
        day = day_plus.day
        month = day_plus.month
        month = calendar.month_abbr[month]
        year = day_plus.year
        day_now = str(day) + ' ' + str(month) + ' ' + str(year)
        print(day_now)
        r = search(session, date = day_now,CSRF = CSRF) #只有这个date
        r = r.json()
        t = r['data']['timeSlotColumns']

        for changzi in t:
            chang = changzi['facilityAlias']
            for time1 in changzi['timeSlots']:
                facilityIds = str(time1['facilityIds'])
                facilityIds = facilityIds.replace('[', '')
                facilityIds = facilityIds.replace(']', '')
                from_time = time1['fromTime']
                toTime = time1['toTime']
                if time1['occupiedFacilityIds']:
                    occupy = False
                else:
                    occupy = True
                if occupy:
                    title.append(str(chang)+ '     '+  str(from_time) + '       '+ str(toTime)+'       '+str(occupy) +'       '+str(facilityIds))
                    content = title[-1]
                    #send_mail(title,content)
                    print(title[-1])
                   # if from_time == '15:30' or from_time == '14:30' or from_time == '13:30':
                    if from_time == '13:30':
                        print('yesyesyes')
                        return title,day_now
        time.sleep(0.5)
    #BMT 04 id=1 05 id=2 06 id=3


nowa = datetime.datetime.now()
time1 = str(nowa.date())+' 08:25:58.000000'
print(time1)
while True:
    now11 = str(datetime.datetime.now())
    if now11 >= time1:
        print('time to login')
        break
    else:
        time.sleep(1)
        continue

CSRF = getCSRF(session,url='https://www40.polyu.edu.hk/poss/secure/login/loginhome.do')
print(CSRF)
for i in range(8):#try 5 times
    try:
        login(session,CSRF)
        CSRF = getCSRF(session, url='https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book.do')
        print(CSRF)
        title, day_now = search_court(session, CSRF)
        chang, from_time, toTime, occupy, facilityIds = title[-1].split('     ')
        print('success1111')
        print(chang, from_time, toTime, occupy, facilityIds)
        break
    except Exception as e:
        print(e)
        time.sleep(3)
        print(f'failed{i}')
        if i >= 2:
            for _ in range(3):
                t = get_t_login(session)
                captcha = get_captcha_login(t, session)
                Captcha = scan_captcha_login()
                print(t)
                res11 = login_captcha(session,t=t,captcha='123',CSRF=CSRF)
                try:
                    if re.search('To continue, please Sign In.', res11.text):
                        print('found')
                        continue
                    else:
                        break
                except:
                    break
            break
        pass

CSRF = getCSRF(session, url='https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book.do')
print(CSRF)
title,day_now = search_court(session, CSRF)
chang,from_time,toTime,occupy,facilityIds = title[-1].split('     ')
print('success1111')
print(chang,from_time,toTime,occupy,facilityIds)


nowb = datetime.datetime.now()
time2 = str(nowb.date())+' 08:29:59.500000'
print(time2)
while True:
    now11 = str(datetime.datetime.now())
    if now11 >= time2:
        print('time to make booking!')
        break
    else:
        continue

for i in range(3): #try n times
    # facilityIds = '5'
    # from_time = '08:30'
    # toTime = '09:30'

    t, ctrId, centerName, facilityId, facilityName, startDateTime, endDateTime = get_t(session = session,CSRF=CSRF,date = day_now,facilityId=facilityIds,startDateTime=from_time,endDateTime=toTime)
    print(t, ctrId, centerName, facilityId, facilityName, startDateTime, endDateTime)
    captcha = get_captcha(t,session)
    Captcha = scan_captcha()
    res = make_booking(session,Captcha=Captcha,CSRF = CSRF,t = t,ctrId = ctrId,centerName = centerName, facilityId=facilityId,facilityName=facilityName,startDateTime=startDateTime,endDateTime=endDateTime,date=day_now)
    try:
        re.search('You have successfully confirmed the booking of the following facility', res.text)
        print('success!!!!!!!')
        time.sleep(0.5)
    except:
        print('faileddddd')
        continue
        time.sleep(0.5)

for i in range(1): #try n times
    # facilityIds = '5'
    # from_time = '08:30'
    # toTime = '09:30'
    title, day_now = search_court(session, CSRF)
    chang, from_time, toTime, occupy, facilityIds = title[-1].split('     ')
    t, ctrId, centerName, facilityId, facilityName, startDateTime, endDateTime = get_t(session = session,CSRF=CSRF,date = day_now,facilityId=facilityIds,startDateTime=from_time,endDateTime=toTime)
    print(t, ctrId, centerName, facilityId, facilityName, startDateTime, endDateTime)
    captcha = get_captcha(t,session)
    Captcha = scan_captcha()
    res = make_booking(session,Captcha=Captcha,CSRF = CSRF,t = t,ctrId = ctrId,centerName = centerName, facilityId=facilityId,facilityName=facilityName,startDateTime=startDateTime,endDateTime=endDateTime,date=day_now)
    try:
        re.search('You have successfully confirmed the booking of the following facility', res.text)
        print('success!!!!!!!')
        break
    except:
        print('faileddddd')
        title, day_now = search_court(session, CSRF)
        chang, from_time, toTime, occupy, facilityIds = title[-1].split('     ')
        print('success1111')
        print(chang, from_time, toTime, occupy, facilityIds)
        time.sleep(5)
