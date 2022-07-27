# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:36:03 2022

@author: DELL
"""
# how to get a secret key
# In your command line >>> access Python >>> then type:

# OS Approach
# import os
# os.urandom(14)

# UUID Approach
# import uuid
# uuid.uuid4().hex

# Secrets [ only for Python 3.6 + ]
#import secrets
# secrets.token_urlsafe(14)
def log(message,status):
    try:
        if args['verbose']==None:
            if status=="e":
                    f.write(format_time() + " -0000 ERROR " + str(message)+"\n")
            elif status=="s":
                    f.write(format_time() + " -0000 SUCCESS " + str(message)+"\n")
            elif status=="n":
                    f.write(format_time() + " -0000 INFO " + str(message)+"\n")
            elif status=="w":
                    f.write(format_time() + " -0000 WARNING " + str(message)+"\n")
            elif status=="d":
                    f.write(format_time() + " -0000 Data " + str(message)+"\n")
        else:
            if status=="e":
                    print(colored(format_time() + " -0000 ERROR " + str(message),'red'))
                    f.write(format_time() + " -0000 ERROR " + str(message)+"\n")
            elif status=="s":
                    print(colored(format_time() + " -0000 SUCCESS " + str(message),'green'))
                    f.write(format_time() + " -0000 SUCCESS " + str(message)+"\n")
            elif status=="n":
                    print(colored(format_time() + " -0000 INFO " + str(message),'white'))
                    f.write(format_time() + " -0000 INFO " + str(message)+"\n")
            elif status=="w":
                    print(colored(format_time() + " -0000 WARNING " + str(message),'yellow'))
                    f.write(format_time() + " -0000 WARNING " + str(message)+"\n")
            elif status=="d":
                    print(colored(format_time() + " -0000 Data " + str(message),'cyan'))
                    f.write(format_time() + " -0000 Data " + str(message)+"\n")
    except (ValueError,IOError) as err:
        log(" - Main() -- Error Occured \n"+str(err),"e")
#ap=argparse.ArgumentParser(prog='Splunk Auto UAM Tool-Kit',description='Splunk UAM Tickets Automation ToolKit')
#ap.add_argument("-r","--run-mode",required=True,help="Running Mode",choices=['User Check','Resolve Ticket'])
#ap.add_argument("-a","--all-ticktes",required=False,help="To Operate All Tickets \n Remark: (-a) over-ride (-i)",action='store_true')
#ap.add_argument("-i","--inc-number",required=False,help="To Operate Specific Ticket",action='store',default="*")
#ap.add_argument("-U","--user",required=False,help="Splunk ADMIN User",default="uam_user")
#ap.add_argument("-H","--host",required=False,help="Splunk Host",default="localhost")
#ap.add_argument("-P","--port",required=False,help="Splunk Port",default="8089")
#ap.add_argument("--version",action='version',version='%(prog)s V-1.0')
#ap.add_argument("-v","--verbose",required=False,help="Print Data Parsed and Logs for more Verbose (-vv)",action='count')


#args=vars(ap.parse_args())

with open ("UAMAuto.log",'a') as f:    
    Func_MAIN(args)
f.close()