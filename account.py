
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
#!/usr/bin/env python
#---------------------------------------------------------
# Name          :- checkUsrAccount_Expiry.py v 0.1 Copyleft (c) 
# Pupose        :- To check the user account expire status in Linux, unix, BSD etc
# Author        :- Vinod Katuwa
# Created       :- 12 Aug 20115
# Version       :- 0.1
# License       :- free
#---------------------------------------------------------
 
# Report `checkUsrAccount_Expiry.py` bugs to vinod.katuwa12@gmail.com
 
import re
import socket
import smtplib
import datetime
 
#---------------------------------------------------------
# Specify Mail Login Credencial
#---------------------------------------------------------
host_name = socket.gethostname()
sender = 'your_mail_id@gmail.com'
password = 'yourpassword'
recipient = 'vinod.katuwa12@gmail.com'   # set admin email ID
subject = 'Account Expiry Details of {!r}'.format(host_name)
min_days = 20   # set min days
 
#---------------------------------------------------------
# Specify SMTP Server
#---------------------------------------------------------
server = 'smtp.gmail.com'
port = 587
 
#---------------------------------------------------------
body1 = "{:<8s} :: {:<2n} days || Last date :: {:3s}"
body2 = "{:<8s} :: Expired on {:3s}"
msg = []
 
#---------------------------------------------------------
# Sent Mail
#---------------------------------------------------------
def mailIt(body):
        body = "" + 'rn
'.join(body) + ""
        headers = ["From: " + sender,
                    "Subject: " + subject,
                    "To: " + recipient,
                    "MIME-Version: 1.0",
                    "Content-Type: text/html"]
        headers = "rn".join(headers)
        session = smtplib.SMTP(server, port)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(sender, password)
        print "nnSending Mail..."
        session.sendmail(sender, recipient, headers + "rnrn" + body)
        print "Sent Successfullly !!"
        session.quit()
 
total_expired_users = 0
total_expring_users = 0
expr_list = {}
 
#---------------------------------------------------------
#  Convert Unix timestamp to Readable Date/time
#---------------------------------------------------------
def convUnixTime(t):
        return datetime.datetime.fromtimestamp(t*60*60*24)
 
#---------------------------------------------------------
# Read shadow file and check for account expriry
#---------------------------------------------------------
with open( "/etc/shadow" ) as shadow:
        for aLine in shadow:
                filed = aLine.split(":")
                Ac = filed[7]
                try:
                        Ac = int(Ac)
                        exprdate = convUnixTime(Ac)
                        Ac=1+( exprdate - datetime.datetime.today()).days
                        l=[Ac,exprdate]
                except ValueError:
                        pass
                else:
                        if Ac <= min_days:
                                expr_list[filed[0]]=l
                        if Ac <= 0:
                                total_expired_users += 1
                        else:
                                total_expring_users += 1
 
#---------------------------------------------------------
# Check Account Expry days and format it Properly Output
#---------------------------------------------------------
def AccountExprDetails():
        msg = []
        t1 = total_expired_users
        t2 = total_expring_users
        if t1 != 0:
                msg.append("====>>Following {!r} Account has been Expired".format(t1))
                index = t1
        else:
                index = -1
        for usr,days in expr_list.iteritems():
                dt=str(days[1])
                if   days[0] <= 0:
                        msg.insert(1,body2.format(usr,dt))
                elif days[0] <= min_days:
                        msg.extend([body1.format(usr,days[0],dt)])
        if t2 != 0:
                msg.insert(index+1,"====>>Following {0} Account will be Expire in {1} Days".format(t2,min_days))
        return msg
 
msg = AccountExprDetails()
 
if __name__ == "__main__":
       if len(msg):
                print 'n'.join(msg)
                mailIt(msg)
       else:
                print "No User Account has been Expire"
