from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import json
import pprint
import cssutils
from selenium import webdriver


def get_phone_no(html):
    
 soup = BeautifulSoup(html,'html.parser') #BeautifulSoup_to_get_data 
 style=soup.findAll('style', attrs = {'type' : 'text/css'})
 phone_map={} 
 
 sheet = cssutils.parseString(str(style[len(style)-1].text))
 
 for rule in sheet:
    try:
      if 'before' not in str(rule.selectorText):
       continue
      for property in rule.style:
       name = property.name    
       value = property.value.strip()
       value=ord(value[1])-643073 
       
       if(value==15):
        value=9
     
    # try:
     #  phone_map[rule.selectorText]=map_over[(value)] 
     # except:
      phone_map[rule.selectorText]=value  
    except:
      print('fail')
     
  #extract all the phone no present
 phone_img=soup.findAll('span', attrs = {'class' : 'mobilesv'})
 
 phone_number=""
 phone_number_final=[]
 count_phone_num=0
 
 is_exist_phone={} 
 for phone_img_div in phone_img: 
  try:
   
     if(count_phone_num==11 and phone_number[0]=='0' and phone_number[1]=='1' and phone_number[2]=='1'):
      if(not phone_number in is_exist_phone.values()):
        phone_number_final.append(phone_number)

      is_exist_phone[phone_number]=phone_number
      phone_number=""
      count_phone_num=0
     
     elif(count_phone_num==13):
      if(not phone_number in is_exist_phone.values()) :
        phone_number_final.append(phone_number)
      
      is_exist_phone[phone_number]=phone_number
      phone_number=""
      count_phone_num=0

     for key, value in phone_map.items():
      if str(phone_img_div['class'][1]) in key:
        if(value==16):
         phone_number=phone_number+"+"
         count_phone_num=count_phone_num+1 
         continue
        phone_number=phone_number+str(value)
        count_phone_num=count_phone_num+1 
        break
  except:
    print("")
 
 return phone_number_final
  

#driver func
def getdata(html,phone_number_final) : 
 data={}
 try:  
  soup = BeautifulSoup(html,'html.parser') #BeautifulSoup_to_get_data
  
  title = soup.find('title')
  business_name = soup.find('span', attrs = {'class' : 'fn'}).text 
  rating = soup.find('span', attrs = {'class' : 'value-titles'}).text 
  review_ele = soup.findAll(class_= 'allratingM')
  total_rating_count=soup.find('span', attrs = {'class' : 'votes'})
  long_addr= soup.find('span', attrs = {'id' : 'fulladdress'})
  long_addr=long_addr.find('span', attrs = {'class' : 'lng_add'}).text
  category=soup.findAll(class_= 'lng_als_lst')
  pay_modes = soup.findAll(class_= 'lng_mdpay')
  also_listed=soup.findAll(class_= 'lng_als_lst')
  Year=soup.findAll('ul', attrs = {'class' : 'alstdul'})
  web=soup.findAll('span', attrs = {'class' : 'mreinfp'}) 
 

 #map phone number digits with image id
 # style=soup.findAll('style', attrs = {'type' : 'text/css'})

 except:
   print("Error : Page fromat changed")

 
 data['phone_number']=phone_number_final

 try:
   data['JustDail_business_title']=title.text.strip()
 except:
   data['JustDail_business_title']='None'  

 try:
   data['business_name']=business_name
 except:
   data['business_name']='None'
 #websiite
 try:
   website=web[len(web)-1].findChildren('a', recursive=False)[0].text.strip()
 except:
   website='None'

 #Year_Established
 try:
  Year_Established=Year[len(Year)-1].findChildren("li" , recursive=False)[0].text.strip()
 except:
  Year_Established='None'
 
 #rating
 if(rating):
  try:
   data['total_rating']=rating
  except:
   data['total_rating']='None'
 
 try:
  data['total_rating_count']=total_rating_count.text
 except:
  data['total_rating_count']="None" 

 #long_addr
 if(long_addr):
  try:
   data['long_addr']=long_addr
  except:
   data['long_addr']='None'

 #website_url
 if(website):
  try:
    data['website']=website
  except:
    data['website']='None'
 if(Year_Established):
   try:
     data['Year_Established']=Year_Established
   except:
     data['Year_Established']='None'

  
 #payment_methds
 pay_string=[]
 for pay in pay_modes:
   pay_string.append((pay.text).strip())

 if(pay_string):
   try:
     data['Modes_of_payment']=pay_string
   except:
     data['Modes_of_payment']='None' 

 #catgry
 cat_string=[]
 for cat in category:
  cat_string.append((cat.text).strip())

 if(cat_string):
   try:
     data['category']=cat_string
   except:
     data['category']='None' 

 #also_listed_in
 also_listed_string=[]
 for also_list in also_listed:
   also_listed_string.append((also_list.text).strip())

 if(also_listed_string):
   try:
     data['Also_Listed_in']=also_listed_string
   except:
     data['Also_Listed_in']='None' 
 

 #reviews/rating
 review=[]   # all user_reviews
 for div in review_ele:
    dic={} 
    name=div.find('span', attrs = {'class' : 'rName'})
    user_rating= div.find('span', attrs = {'class' : 'star_m'})
    user_rating_date= div.find('span', attrs = {'class' : 'dtyr'})
    user_review=div.find('p', attrs = {'class' : 'rwopinion2'})
    
    if(name):
     try:
        dic['user_name']=name.text
     except:
         dic['user_name']='None'

    if(user_rating):
     try:
      review_rat= user_rating['aria-label']
      dic['user_rating'] = review_rat[len(review_rat)-1]    
     except:
      dic['user_rating']='0'

    if(user_rating_date):
     try :
      dic['user_rating_date']=user_rating_date['content']
     except:
      dic['user_rating_date']="None"
    if(user_review):
      try:
        dic['user_review']=user_review.text
      except:
        dic['user_review']='None'
    try:
     if(dic):
      review.append(dic)
    except:
     print('Cannot add record')    

 data['reviews']=review
 return data

def get_data(url,print_response=False):
  #import sys
  #sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
  from selenium import webdriver
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  userAgent = 'Safari/537.36'
  #chrome_options.add_argument(f'user-agent={userAgent}')
  chrome_options.add_argument('user-agent=Safari/537.36')
  wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
  wd.get(url)
  phone_no=(get_phone_no(wd.page_source))
  print(phone_no)

  #wait for the page to load -> click on load_more_reviews
  wait = WebDriverWait(wd, 10)
  accept = wait.until(EC.element_to_be_clickable((By.ID, 'rvldr')))
  actions = ActionChains(wd)
 
  while 1:
   try:
    accept.click()  #currently-not-waiting-for-more-reviews-to-load, in order to get all reviews put a statement here to wait for more review to load        
    wait = WebDriverWait(wd, 10)
   except: 
    html = wd.page_source
    wd.quit()
    data=getdata(html,phone_no)
    if(print_response):
     printdataJSON(data)
    break 
  return data 

  #<!--helper func 
def printdataJSON(data):
 data=json.dumps(data,indent=4)
 print(data) 

