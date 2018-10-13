# Innovaccer
To solve the above problem I have used a wamp server to act as  a local host.The program is written according to it only.At the starting of the program I have used mysql.connector to connect
to the localhost which will allow us to use the database.I have created a database named "mydatabase".In mydatabase I have created a table by using the create table command only once.
You have to run it for one time only.My info table consists of three table having column name as id(primary key),Email and TVSeries respectively.After that i have accessed the database
and thus found all the TV series name of a particular email id and thus process it one by one.For each TV series I have done a yahoo search with the included string "imdb" and "TV series".
After that with the help of web scrapping I found out the all the links present in the search result page and accessed the first one which has "www.imdb.com" as a substring.Now I moved to 
the series page of IMDB.Now similarly with the help of web scrapping I got the url of the latest season and parsed it with the beautifulSoap by analysing the season number and episode I gather the respective recent date of the Series.Then Compare it with present date and then I stored the 
information which is required in a specified format into a variable named messages.Then again with the help of localhost I was able to send the email to the respective person with their 
messages.I have also included the tempeate code to send gmail in the program comments section
