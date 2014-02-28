#!/usr/bin/python
#
# This is a python script to read text from a .txt file, import contacts from csv file and send email personally to the enlisted contacts

__author__ = 'Lokesh A. Ravindranathan'
__date__ = '02-10-2014'
__license__ = 'GPL'
__copyright__ = 'Copyright 2014'
__email__ = 'lokesh.amarnath@gmail.com'

import sys,getopt,getpass
import atom
import gdata.contacts.data, gdata.contacts.client
import smtplib 

def smtpemaillogin(username,password):
  server = smtplib.SMTP('smtp.gmail.com:587')  
  server.starttls()  
  server.login(username,password);  
  return server;

def sendemail(server,user,toaddrs,msg):
  server.sendmail(user,toaddrs,msg);

def smtpemaillogout(server):
  server.quit();
  
def print_datemin_query_results(gd_client):
  updated_min = '2008-01-01'
  query = gdata.contacts.client.ContactsQuery()
  query.updated_min = updated_min
  query.max_results = 10000
  feed = gd_client.GetContacts(q = query)
  for contact in feed.entry:
#Assumption is the first contact has a default name and is correct
    if (isinstance(contact.name, type(feed.entry[0].name))):
      print contact.name.full_name.text
      
      if (len(contact.email)):
        print contact.email[0].address
        
#Name of the contact is same as the email address
        if(contact.name.full_name.text==contact.email[0].address):
          contactnamechange = raw_input('Do you wish to change the name of the contact? Type any character for yes or defaults to no');
          if contactnamechange:
            contactname = raw_input('Enter the name of the person');

      else:
        print 'No contact id found'


def main():

    try:
	opts, args = getopt.getopt(sys.argv[1:],'',['user=','pw='])

    except getopt.error,msg:
	print 'python test_email.py --user [username] --pw [password]'
	sys.exit(2)

    user = ''
    pwd  = ''

    for option, arg in opts:
	if option == 'user':
	    user = arg
	elif option == '--pw':
	    pwd = arg

    while not user:
	user = raw_input('Please enter your username: ')

    while not pwd:
        pwd = getpass.getpass()
	if not pwd:
	    print 'Password cannot be blank.'

    client = gdata.contacts.client.ContactsClient(source='testApp-v1')
    client.ClientLogin(user, pwd, client.source);
    
    print_datemin_query_results(client);
    server = smtpemaillogin(user,pwd);

    toaddrs = 'rla.2138@gmail.com';
    msg = 'This is a test message';
    sendemail(server,user,toaddrs,msg);
    
    smtpemaillogout(server);


if __name__ == '__main__':
    main()

