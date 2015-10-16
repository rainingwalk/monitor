#!/usr/bin/python

"""
acs/ecs 	vm.CPUUtilization 	Percent 	instanceId 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.DiskIORead 	Kilobytes/Second 	instanceId,diskname 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.DiskIOWrite 	Kilobytes/Second 	instanceId,diskname 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.DiskUtilization 	Percent 	instanceId,mountpoint 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.InternetNetworkRX 	Kilobits/Second 	instanceId,netname 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.InternetNetworkTX 	Kilobits/Second 	instanceId,netname 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.LoadAverage 	None 	instanceId,period 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.MemoryUtilization 	Percent 	instanceId 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.VirtualMemoryUtilization 	Percent 	instanceId 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.TcpCount 	Count 	instanceId,state 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.ProcessCount 	Count 	instanceId 	5m,15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.Process.number 	Count 	instanceId,processName 	15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.Process.memory 	Kilobytes 	instanceId,processName 	15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
acs/ecs 	vm.Process.cpu 	Percent 	instanceId,processName 	15m,30m,1h,1d 	Average,Sum,SampleCount,Maximum,Minimum
"""

import os
import requests 
import urllib
import hmac
import hashlib
from operator import itemgetter
import time
import datetime
import random
import json
import base64
import sys
import uuid
from pprint import pprint
from ConfigParser import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def percent_encode(request, encoding=None):

    try:
        s = unicode(request, encoding)
    except TypeError:
        if not isinstance(request, unicode):
            # We accept int etc. types as well
            s = unicode(request)
        else:
            s = request

    res = urllib.quote(
        s.encode('utf8'),
        safe='~')
    return res


def query_instance(region_id):
	REGION_ID = region_id
	os.environ["TZ"] = "UTC"
	time.tzset()
	ISOTIMEFORMAT='%Y-%m-%dT%XZ'
	One_Minutes_Ago = datetime.datetime.now() - datetime.timedelta(minutes = 1)
	ONE_MINUTES_AGO = One_Minutes_Ago.strftime("%Y-%m-%dT%H:%M:%SZ")
	Six_Minutes_Ago = datetime.datetime.now() - datetime.timedelta(minutes = 6)
	SIX_MINUTES_AGO = Six_Minutes_Ago.strftime("%Y-%m-%dT%H:%M:%SZ")
	FORMAT = "JSON"
	VERSION = "2014-08-15"
	SIGNATURE_METHOD = "HMAC-SHA1"
	TIME_STAMP = time.strftime( ISOTIMEFORMAT, time.localtime() )
	#TIME_STAMP = ONE_MINUTES_AGO
	SIGNATURE_VERSION = "1.0"
	SIGNATURE_NONCE = str(uuid.uuid4())
	#REGION_ID = sys.argv[1]
	ACTION = "DescribeDBInstances"
	DBINSTANCEID = 'rds5061ck6ytcaq08t4b'
	NAME_SPACE = "acs/rds"
	#METRIC_NAME = "vm.TcpCount"
	#START_TIME = SIX_MINUTES_AGO
	END_TIME = ONE_MINUTES_AGO
	#DIMENSIONS = "{instanceId:'i-23ieuu51a'}"
	#INSTANCE_ID = 'i-258k8ytc1'
	PERIOD = "5m"
	STATISTICS = "Average"
	NEXT_TOKEN = 1
	MAX_RESULTS = 100
	cfg_path = os.path.join(os.getenv('HOME', '/root/'), '.aliyun.cfg')
	cp = ConfigParser()
	if os.path.exists(cfg_path):
	    cp.read(cfg_path)
	else:
	    cp.read('/etc/aliyun.cfg')
	
	if cp.has_section('default') and cp.has_option('default', 'access_key_id'):
	    access_key_id=cp.get('default', 'access_key_id')
	    secret_access_key=cp.get('default', 'secret_access_key')
	else:
	    raise Error("Could not find credentials.")
	encoding = sys.stdin.encoding

	f = { 
		'Format' : FORMAT, 
		'Version' : VERSION, 
		'AccessKeyId' : access_key_id, 
		'SignatureMethod' : SIGNATURE_METHOD, 
		'Timestamp' : TIME_STAMP, 
		'SignatureVersion' : SIGNATURE_VERSION, 
		'SignatureNonce' : SIGNATURE_NONCE, 
#		'DBInstanceId' : DBINSTANCEID,
#		'RegionId' : REGION_ID, 
		'RegionId' : REGION_ID, 
		'Action' : ACTION, 
#		'TotalRecordCount' : 50000,
#		'Namespace' : NAME_SPACE, 
#		'MetricName' : METRIC_NAME, 
#		'StartTime' : SIX_MINUTES_AGO, 
#		'EndTime' : END_TIME,
		'PageSize' : 100
#		'PageNumber' : 1 
#		'Dimensions' : DIMENSIONS, 
#		'InstanceId' : INSTANCE_ID, 
#		'Period' : PERIOD, 
#		'Statistics' : STATISTICS, 
#		'NextToken' : NEXT_TOKEN, 
#		'Length' : MAX_RESULTS 
		}
	sf = sorted(f.iteritems(), key=itemgetter(0))
	bstring1 = urllib.urlencode(sf).replace('+', '%20').replace('%7E', '~').replace('*', '%2A')
	canonicalized_query_string = '&'.join(['%s=%s' % (percent_encode(k, encoding),
	                                                  percent_encode(v, encoding))
	                                       for k, v in sf])
	string_to_sign = 'GET&%2F&' + percent_encode(canonicalized_query_string, encoding)
	h = hmac.new(secret_access_key + '&', string_to_sign, hashlib.sha1)
	signature = base64.b64encode(h.digest())
	url = "https://rds.aliyuncs.com/?" + bstring1 + "&Signature=" + signature
	return url

def get_instance(region):
	region_id = "cn-%s" % region
	idfile = open(os.path.join(BASE_DIR, region_id +'.id'), 'w')
	MaxAllowRetryNumber = 2
	for tries in range(MaxAllowRetryNumber + 1):
		url = str(query_instance(region_id))
		apidata = requests.get(url)
		content = apidata.content
		resp_content = json.loads(content)
		if 'Items' in resp_content and resp_content["Items"]['DBInstance']:
			for items in resp_content["Items"]['DBInstance']:
				if items['DBInstanceDescription']:
					content = "%s,%s\n" % (items['DBInstanceId'],items['DBInstanceDescription'])
				else:
					content = "%s,%s\n" % (items['DBInstanceId'],items['DBInstanceId'])
				idfile.write(content)
			break
		else:
			print "Retry %s for %s ..." % (idfile, tries)
			continue
			if tries == MaxAllowRetryNumber:
				print "!!! Failed To Update %s ..." % (idfile)
			

	idfile.close()

if __name__ == '__main__':
	print "-"*25,"Beijing"
	get_instance('beijing')
	#time.sleep(5)
	#print "-"*25,"hangzhou"
	#get_instance('hangzhou')
