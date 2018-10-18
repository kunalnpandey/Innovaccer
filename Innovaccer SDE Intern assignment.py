# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 02:05:27 2018

@author: Kunal N Pandey
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 21:46:59 2018

@author: Kunal N Pandey
"""
import pandas as pd
import numpy as np
import mysql.connector
from bs4 import BeautifulSoup
from requests import get
import time
import smtplib
import datetime
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="mydatabase" #mydatabase is the name of the database under  local host
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE INFO (id INT AUTO_INCREMENT PRIMARY KEY, Email VARCHAR(255), TVSeries VARCHAR(255))")
E=input("Email:") #taking the Email address
S=list(map(str, input("TV Series:").split(','))) #Taking the list of TV series
sql = "INSERT INTO INFO (Email, TVSeries) VALUES (%s, %s)"
l=len(S)
for i in range(0,l):
    val = (E,S[i])
    mycursor.execute(sql, val)
mydb.commit()
mycursor = mydb.cursor()
sql = "SELECT TVSeries FROM INFO WHERE Email = %s "   #selecting all Tv series requested by a particular user from the database
adr=(E,)
mycursor.execute(sql,adr)

myresult = mycursor.fetchall()
message=""  #to store the status and name of the series which is to be send through email
for x in myresult:
    s=""
    for i in range(len(x)):
        s=s+""+x[i]
    s=s+"+Tv+Series+imdb"   #search query
    url1="https://in.search.yahoo.com/search?p="+"+"+s   #search query in the format of yahoo search 
    
    
    response1=get(url1)    #Searching on Yahoo the Tv Series Query
    #print(response1.text[:1000])      ----to get overview of the page
    url2=""      #To store the url of the search result
    html_soup1 = BeautifulSoup(response1.text, 'lxml')
    for link in html_soup1.find_all('a',href=True): #finding all the link on the search result page
        z="www.imdb.com"
        if z in link['href']:  #Checking if the link contains imdb.com . If it is true then the most relevelant link is this only and this link is stored in the url2
            url2=link['href']
            break
    
    
    #now opening the link stored in url2
    response2=get(url2)
    html_soup2 = BeautifulSoup(response2.text, 'lxml')
    url3="https://www.imdb.com"
    search_containers = html_soup2.find('div', class_ = 'seasons-and-year-nav')
    link=search_containers.find('a',href=True) #finding the first link in search Container
    url3=url3+link['href']  #url3 is the link to the page which contains information about episodes and seasons
    
    k=0
    first_series=""
    response=get(url3)
    html_soup = BeautifulSoup(response.text, 'lxml')
    #print(url3)
    odd_movie_containers = html_soup.find_all('div', class_ = 'list_item odd')
    even_movie_containers = html_soup.find_all('div', class_ = 'list_item even')
    #print("Length of odd_movie_containers=",len(odd_movie_containers))
    #print("Length of even_movie_containers=",len(even_movie_containers))
    index_odd=0    #to iterate through odd_movie_containers
    index_even=0   #to iterate through even_movie_containers
    index=0
    #creating a dictionary for the months
    dic={"Jan.":"01","Feb.":"02","Mar.":"03","Apr.":"04","May.":"05","May":"05","Jun.":"06","Jul.":"07","Aug.":"08","Sep.":"09","Oct.":"10","Nov.":"11","Dec.":"12"}
    name=str(x)
    name=name[2:len(name)-3]
    message=message+"TV Series : "+name+"\n"  #storing TV series Name
    
    #Creating a while loop to chck the episode as they are arranged in the ascending order
    #The loop will stop when it finds the next air date
    
    
    while(index<len(odd_movie_containers)+len(even_movie_containers)):
        date=""
        if((index+1)%2!=0 & index_odd<len(odd_movie_containers)):
            first_series=odd_movie_containers[index_odd]
            first_year = first_series.find('div', class_ = 'airdate')
            date=str(first_year.text)
            index_odd=index_odd+1
        elif((index+1)%2==0 & index_even<len(even_movie_containers)):
            first_series=even_movie_containers[index_even]
            first_year = first_series.find('div', class_ = 'airdate')
            date=str(first_year.text)
            index_even=index_even+1
        date=date.strip()
        #print("index no=",index,x,"Date=",date)
        #message=message+"TV Series : "+name+"\n"  #storing TV series Name
        if(len(date)==0):
            message=message+"Status: All the seasons are finished and no further details are available"+"\n\n"
            break
        else:
            if(len(date)>12):
                date=date[-12:]
            actual_date=date
            if(len(date)==12):
                s=date[3:7]   #to identify the alphabetical month name numerical value in its corresponding dictionary table
                date1=date[0]+date[1]+"/"+dic[s]+"/"+date[8:]
                date=date1
            elif(len(date)==11):          #i.e dd component of date has only one element
                s=date[3:6]
                if(s=="May"):
                    date=date[0]+date[1]+"/"+dic[s]+"/"+date[7:]
                else:
                    date="0"+date      # to compare it with other date
                    s=date[3:7]
                    date=date[0]+date[1]+"/"+dic[s]+"/"+date[8:]
            elif(len(date)==10):
                s=date[2:5]
                date="0"+date[0]+"/"+dic[s]+"/"+date[6:]
            elif(len(date)==4):           #i.e only year is available
                date="01/01/"+date      #to compare it with other date
            
            new_date = time.strptime(date, "%d/%m/%Y")
            present_date=str(time.strftime("%d/%m/%Y"))  #present date in dd/mm/yyyy format
            present_date=time.strptime(present_date,"%d/%m/%Y")
            ##if(present_date>new_date):
                #message=message+"Status: All the seasons are finished and no further details are available"+"\n\n"  # storing the status of the series
            if(new_date>=present_date):
                if(len(actual_date)==4):
                    message=message+"Status: The next season begins in "+str(actual_date)+"\n\n\n"
                    break
                else:
                    message=message+"Status: Next episode airs on 20"+date[8:]+"-"+date[3:5]+"-"+date[0:2]+"\n\n"
                    break
        index=index+1             #loop counter
        
    if(index==len(odd_movie_containers)+len(even_movie_containers)):   #if there is no date such available air date for the series
        message=message+"Status: All the seasons are finished and no further details are available"+"\n\n"
            
                
            
    
#Now Code for sending an email to the user regarding their TV Series episode status
#Content to be send to the respective user is stored in message variable

present_date=str(time.strftime("%d/%m/%Y"))     #present date in dd/mm/yyyy format
present_date=time.strptime(present_date,"%d/%m/%Y")
            
print("\nStatus as checked on date:",datetime.datetime.today().strftime('%Y-%m-%d'),"\n\n")
print(message)            #Shows the content of the message

"""
#Program code to send the message through Gmail
#creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("Sender Email address", "Sender Password")   
s.sendmail("sender_email_id", "receiver_email_id", message) 
  
# terminating the session 
s.quit() 
"""
#program code to sendmail on localhost server
sender = 'host@fromdomain.com'
receivers = [E]

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message)         
    print("Email Sent Successfully..!!!")
except ConnectionRefusedError:
    print("Error: Unable to send email\n")
    
    
