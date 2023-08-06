#################################################################
### Title     :     SMTP
### Filename  :     smtp.py
### Created   :     2012
### Author    :     Joel Horowitz
### Type      :     Library
### Summary   :
###
###
#################################################################

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_server, _email, _login, _pw = None, None, None, None
def set_credentials(server,email,login,pw):
    global _login, _pw, _server, _email
    _login = login
    _pw = pw
    _server = server
    _email = email
    print(_server,_email,_login,_pw)
    
def sendHTMLmailwithattachments(sender,to,subject,body,attachments = [], cc = []):
    COMMASPACE = ', '
    
    # Create the container (outer) email message.
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = _email
    if type(to)==str:
        to = [to]
    msg['To'] = COMMASPACE.join(to)
    
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    
    msgText = MIMEText(body, 'html')
    msgAlternative.attach(msgText)
    
    for FileInfo in attachments:
        fp = open(FileInfo['filename'], 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<%s>' % FileInfo['name'])
        msg.attach(msgImage)
    
    try:
        with smtplib.SMTP(_server, 587) as server:
            server.starttls()
            print(f"Logging in as {_login}")
            server.login(_login,_pw)
            server.sendmail(sender, to, msg.as_string())
            server.quit()
        print(f"Email sent to {to}: {subject}")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    email = 'user@domain.com'
    pw = 'blah'
    set_credentials('smtp.gmail.com', email, email, pw)    
    sendHTMLmailwithattachments(email,[recipient],'Test','Body')
