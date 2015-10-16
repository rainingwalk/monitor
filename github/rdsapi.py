#!/usr/bin/python

import pprint
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
import createsub
import rrdtool

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

#def query_instance(region_id, PERIODTIME):
#	REGION_ID = region_id
#	os.environ["TZ"] = "UTC"
#	time.tzset()
#	ISOTIMEFORMAT='%Y-%m-%dT%XZ'
#	One_Minutes_Ago = datetime.datetime.now() - datetime.timedelta(minutes = 1)
#	ONE_MINUTES_AGO = One_Minutes_Ago.strftime("%Y-%m-%dT%H:%M:%SZ")
#	FORMAT = "JSON"
#	VERSION = "2015-04-20"
#	SIGNATURE_METHOD = "HMAC-SHA1"
#	TIME_STAMP = time.strftime( ISOTIMEFORMAT, time.localtime() )
#	#TIME_STAMP = ONE_MINUTES_AGO
#	SIGNATURE_VERSION = "1.0"
#	SIGNATURE_NONCE = str(uuid.uuid4())
#	REGION_ID = "cn"
#	ACTION = "DescribeMetricDatum"
#	NAME_SPACE = "acs/rds"
#	#METRIC_NAME = "vm.TcpCount"
#	#START_TIME = SIX_MINUTES_AGO
#	END_TIME = ONE_MINUTES_AGO
#	#DIMENSIONS = "{instanceId:'i-23ieuu51a'}"
#	#INSTANCE_ID = 'i-258k8ytc1'
#	PERIOD = "5m"
#	STATISTICS = "Average"
#	NEXT_TOKEN = 1
#	MAX_RESULTS = 100
#	cfg_path = os.path.join(os.getenv('HOME', '/root/'), '.aliyun.cfg')
#	cp = ConfigParser()
#	MINUTES_AGO = datetime.datetime.now() - datetime.timedelta(minutes = PERIODTIME)
#	SIX_MINUTES_AGO = MINUTES_AGO.strftime("%Y-%m-%dT%H:%M:%SZ")
#	
#	if os.path.exists(cfg_path):
#	    cp.read(cfg_path)
#	else:
#	    cp.read('/etc/aliyun.cfg')
#	
#	if cp.has_section('default') and cp.has_option('default', 'access_key_id'):
#	    access_key_id=cp.get('default', 'access_key_id')
#	    secret_access_key=cp.get('default', 'secret_access_key')
#	else:
#	    raise Error("Could not find credentials.")
#	encoding = sys.stdin.encoding
#	f = {
#	    'Format' : FORMAT,
#	    'Version' : VERSION,
#	    'AccessKeyId' : access_key_id,
#	    'SignatureMethod' : SIGNATURE_METHOD,
#	    'Timestamp' : TIME_STAMP,
#	    'SignatureVersion' : SIGNATURE_VERSION,
#	    'SignatureNonce' : SIGNATURE_NONCE,
#	    'RegionId' : REGION_ID,
#	    'Action' : ACTION,
#	    'PageSize' : 100
#	    }
#	sf = sorted(f.iteritems(), key=itemgetter(0))
#	bstring1 = urllib.urlencode(sf).replace('+', '%20').replace('%7E', '~').replace('*', '%2A')
#	canonicalized_query_string = '&'.join(['%s=%s' % (percent_encode(k, encoding),
#	                                                  percent_encode(v, encoding))
#	                                       for k, v in sf])
#	string_to_sign = 'GET&%2F&' + percent_encode(canonicalized_query_string, encoding)
#	h = hmac.new(secret_access_key + '&', string_to_sign, hashlib.sha1)
#	signature = base64.b64encode(h.digest())
#	url = "https://rds.aliyuncs.com/?" + bstring1 + "&Signature=" + signature
#	return url

def query_data(METRIC_NAME, DIMENSIONS, PERIODTIME):
	os.environ["TZ"] = "UTC"
	time.tzset()
	ISOTIMEFORMAT='%Y-%m-%dT%XZ'
	One_Minutes_Ago = datetime.datetime.now() - datetime.timedelta(minutes = 1)
	ONE_MINUTES_AGO = One_Minutes_Ago.strftime("%Y-%m-%dT%H:%M:%SZ")
	FORMAT = "JSON"
	VERSION = "2015-04-20"
	SIGNATURE_METHOD = "HMAC-SHA1"
	TIME_STAMP = time.strftime( ISOTIMEFORMAT, time.localtime() )
	#TIME_STAMP = ONE_MINUTES_AGO
	SIGNATURE_VERSION = "1.0"
	SIGNATURE_NONCE = str(uuid.uuid4())
	REGION_ID = "cn"
	ACTION = "DescribeMetricDatum"
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
	MINUTES_AGO = datetime.datetime.now() - datetime.timedelta(minutes = PERIODTIME)
	SIX_MINUTES_AGO = MINUTES_AGO.strftime("%Y-%m-%dT%H:%M:%SZ")
	
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
		'RegionId' : REGION_ID, 
		'Action' : ACTION, 
		'Namespace' : NAME_SPACE, 
		'MetricName' : METRIC_NAME, 
		'StartTime' : SIX_MINUTES_AGO, 
		'EndTime' : END_TIME, 
		'Dimensions' : DIMENSIONS, 
	#	'InstanceId' : INSTANCE_ID, 
		'Period' : PERIOD, 
		'Statistics' : STATISTICS, 
	#	'NextToken' : NEXT_TOKEN, 
		'Length' : MAX_RESULTS 
		}
	
	sf = sorted(f.iteritems(), key=itemgetter(0))
	
	bstring1 = urllib.urlencode(sf).replace('+', '%20').replace('%7E', '~').replace('*', '%2A')
	
	
	canonicalized_query_string = '&'.join(['%s=%s' % (percent_encode(k, encoding),
	                                                  percent_encode(v, encoding))
	                                       for k, v in sf])
	
	string_to_sign = 'GET&%2F&' + percent_encode(canonicalized_query_string, encoding)
	
#	return string_to_sign
	
	h = hmac.new(secret_access_key + '&', string_to_sign, hashlib.sha1)
	signature = base64.b64encode(h.digest())
	
	url = "http://metrics.aliyuncs.com/?" + bstring1 + "&Signature=" + signature
	
	return url
	
