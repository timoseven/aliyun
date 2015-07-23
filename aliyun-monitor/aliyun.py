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
#SIGNATURE_NONCE = str(uuid.uuid4()) 
REGION_ID = "cn"
ACTION = "DescribeMetricDatum"
NAME_SPACE = "acs/ecs"
METRIC_NAME = "vm.TcpCount" 
#START_TIME = SIX_MINUTES_AGO 
END_TIME = ONE_MINUTES_AGO 
DIMENSIONS = "{instanceId:'i-23ieuu51a'}"
INSTANCE_ID = 'i-258k8ytc1'
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


def query_data():

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
	
	#u = urllib.urlopen("%s" % url)
	###
	#data = json.loads(u.read().decode('utf-8')) 
	#pprint(data)



#def read_list(monitor_list, vm_list):

vlist = open('/home/timo/test/python/vm_list', 'r')

done = 0

while not done:
	vm = vlist.readline().strip('\n')
	if(vm != ''):
		DIMENSIONS = "{instanceId:'" + vm + "'}"
#		print(DIMENSIONS)
		mlist = open('/home/timo/test/python/monitor_list', 'r')
		for ms in mlist:
			fields = ms.split("\t")
			METRIC_NAME = fields[0].strip('\n')
			PERIOD = fields[1].strip('\n') + 'm'
			print(PERIOD)
			PERIODTIME = int(fields[1]) + 1
			MINUTES_AGO = datetime.datetime.now() - datetime.timedelta(minutes = PERIODTIME)
			SIX_MINUTES_AGO = MINUTES_AGO.strftime("%Y-%m-%dT%H:%M:%SZ")
			SIGNATURE_NONCE = str(uuid.uuid4())
			print(query_data())
		mlist.close()
	else:
		done = 1
vlist.close()



#if __name__ == '__main__':
#	read_list ('/home/timo/test/python/monitor_list','/home/timo/test/python/vm_list')
