# encoding: utf-8
#!/usr/bin/python

import MySQLdb
import MySQLdb.cursors
import time
import rrdtool
import re, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(BASE_DIR,'rrdb')
if not os.path.exists(DIR):
    os.mkdir(DIR)
cur_time=str(int(time.time()))
def createdb():
    conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="nagios",port=int(3306),charset="utf8",
                           cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    #sql_groups = "select alias from nagios_hostgroups"
    sql_hosts = "select alias from nagios_hosts"
    cursor.execute(sql_hosts)
    results = cursor.fetchall()
    cursor.close()
    #services = ['Load', 'Memory']
    #services = ['Memory']
    for host in results:
        h = host['alias']
        status=rrdtool.create(str(DIR)+'/'+str(h)+'.rrd','--step','300','--start', cur_time, 
        'DS:est_tcp:GAUGE:600:U:U', 
        'DS:total_processes:GAUGE:600:U:U',         
        'DS:memory_usage:GAUGE:600:U:U',         
        'DS:root_partition:GAUGE:600:U:U',         
        'DS:load_5min:GAUGE:600:U:U',         
        'DS:ping_package_loss:GAUGE:600:U:U',         
        'DS:network_eth0_rx:GAUGE:600:U:U',         
        'DS:network_eth0_tx:GAUGE:600:U:U',         
        'RRA:AVERAGE:0.5:1:600',
        'RRA:AVERAGE:0.5:6:700',
        'RRA:AVERAGE:0.5:24:775',
        'RRA:AVERAGE:0.5:288:797',
        'RRA:MAX:0.5:1:600',
        'RRA:MAX:0.5:6:700',
        'RRA:MAX:0.5:24:775',
        'RRA:MAX:0.5:444:797',
        'RRA:MIN:0.5:1:600',
        'RRA:MIN:0.5:6:700',
        'RRA:MIN:0.5:24:775',
        'RRA:MIN:0.5:444:797')
        if status:
            print rrdtool.error()

if __name__ == '__main__':
    createdb()

