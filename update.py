# encoding: utf-8
#!/usr/bin/python

import MySQLdb
import MySQLdb.cursors
import time
import rrdtool
import re, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(BASE_DIR,'rrdb')
def task():
    starttime=int(time.time())
    conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="nagios",port=int(3306),charset="utf8",                                                                                                                             cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    #sql_groups = "select alias from nagios_hostgroups"
    sql_hosts = "select alias from nagios_hosts"
    cursor.execute(sql_hosts)
    results = cursor.fetchall()
    #services = ['est tcp', 'Total Processes', 'Memory usage', 'Root Partition', 'Load', 'PING','Network eth0']
    for host in results:
        h = host['alias'].encode("utf-8")
        s1=s2=s3=s4=s5=s6=s7=s8=0
        #for service in services:
            #sql_services = "select A.end_time, A.output, B.display_name from nagios_servicechecks as A, nagios_services as B, nagios_hosts as C                                                                  where C.alias='%s' and B.display_name='%s' and A.service_object_id=B.service_object_id and                                                                                           B.host_object_id=C.host_object_id order by A.end_time desc limit 1" % (h, service)
        sql = "select a.alias,b.display_name,c.output,c.last_check from nagios_hosts as a, nagios_services as b, nagios_servicestatus as c where a.host_object_id=b.host_object_id and b.service_object_id=c.service_object_id and a.alias='%s'" % (h)
        cursor.execute(sql)
        data = cursor.fetchall()
        if data:
            for rec in data:
                output = rec['output']
                last_check = rec['last_check']
                display_name = rec['display_name'].encode("utf-8")
                items = re.findall('[0-9]+|[0-9]+.[0-9]+|[0-9]+%', output)
                ss1 = "".join(items[0:1]).encode("utf-8")
                ss2 = "".join(items[1:2]).encode("utf-8")
                ss3 = "".join(items[2:3]).encode("utf-8")
                if display_name == 'est tcp':
                    s1 = ss1
                elif display_name == 'Total Processes':
                    s2 = ss1
                elif display_name == 'Memory usage':
                    s3 = ss3.split('%')[0]
                elif display_name == 'Root Partition':
                    s4 = ss2.split('%')[0]
                elif display_name == 'Load':
                    s5 = str(ss2)
                elif display_name == 'PING':
                    s6 = ss1.split('%')[0]
                elif display_name == 'Network eth0':
                    s7 = ss1
                    s8 = ss2
                else:
                    pass
            #print '----',display_name,'-----',output,'++++++','ss1:',ss1,'ss2:',ss2,'ss3:',ss3,'est tcp:',s1,'total process:',s2,'memory:',s3,'root partition:',s4,'load:',s5,'ping:',s6,'eth0_rx/tx:',s7,'/',s8
            #print '----------',str(h),'---','est tcp:',s1,'total process:',s2,'memory:',s3,'root partition:',s4,'load:',s5,'ping:',s6,'eth0_rx/tx:',s7,'/',s8
        #print '----------',str(h),'---',output,'----',end_time
        update=rrdtool.updatev(DIR+'/'+h+'.rrd','%s:%s:%s:%s:%s:%s:%s:%s:%s' % (str(starttime),s1,s2,s3,s4,s5,s6,s7,s8))
       # print update
    cursor.close()
#def timer(n):
#    while True: 
#        #print time.strftime('%Y-%m-%d %X',time.localtime()) 
#        task() 
#        time.sleep(n) 
 
if __name__ == '__main__':
    task() 
    #timer(10) 
