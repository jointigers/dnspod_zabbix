#coding=utf-8
import json
import urllib
import urllib2
import sys
dnsurl="https://dnsapi.cn/Record.List"
user="e.com"
passwd="~"
domainid="26856323"

zabbixurl="http://10.185.30.222:8081/api_jsonrpc.php"
zabbixuser="xxx"
zabbixpass="xxx"

def addheader(request):
    header = {"Content-Type": "application/json"}
    for key in header:
        request.add_header(key,header[key])
    return request

def loginzabbix(zurl):
    #header = {"Content-Type": "application/json"}
    a =json.dumps( { 'jsonrpc': '2.0', 'method': 'user.login', 'params': { 'user':zabbixuser , 'password' : zabbixpass}, 'id' : 0})
    request=urllib2.Request(zurl,a)
    request=addheader(request)
    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        print "Auth Failed, Please Check Your Name And Password:",e.code
        sys.exit(3)
    else:
        response = json.loads(result.read())
        result.close()
        auth=response['result']
        return auth
        
def createitem(auth,name,key,hostid,type,value_type,interfaceid,applicationsid,delay):
    createitemjson=json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "method": "item.create",
                            "params": {
                                "name": name,
                                "key_": key,
                                "hostid": hostid,
                                "type": type,
                                "value_type": value_type,
                                "interfaceid":interfaceid ,
                                "applications": [
                                    applicationsid
                                ],
                                "delay": delay
                            },
                            "auth": auth,
                            "id": 0
                         }
                    )
    request = urllib2.Request(zabbixurl,createitemjson)
    request=addheader(request)
    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        print "Auth Failed, Please Check Your Name And Password:",e.code
        sys.exit(3)
    else:
        response = json.loads(result.read())
        result.close()
        itemid=response['result']['itemids'][0]
        return itemid
def creaehost(ip,port,groupid,templateid):
    creaehostjson=json.dumps(
                             { 
                                "jsonrpc": "2.0",
                                "method": "host.create",
                                "params": {
                                    "host": ip,
                                    "interfaces": [
                                        {
                                            "type": 1,
                                            "main": 1,
                                            "useip": 1,
                                            "ip": ip,
                                            "dns": "",
                                            "port": port
                                        }
                                    ],
                                    "groups": [
                                        {
                                            "groupid": groupid
                                        }
                                    ],
                                    "templates": [
                                        {
                                            "templateid": templateid
                                        }
                                    ],
                                    
                                },
                                "auth": auth,
                                "id": 0
                              
                              }
                             )
    request = urllib2.Request(zabbixurl,creaehostjson)
    request=addheader(request)
    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        print "Auth Failed, Please Check Your Name And Password:",e.code
        sys.exit(3)
    else:
        response = json.loads(result.read())
        result.close()
        #hostid=response['result']['hostids'][0]
        return response
    
def createtiger(auth,description,expression):
    createtigerjson=json.dumps(
                                {
                                    "jsonrpc": "2.0",
                                    "method": "trigger.create",
                                    "params": {
                                        "description": description,
                                        "expression": expression,

                                    },
                                    "auth": auth,
                                    "id": 0
                                }
                               )
    request = urllib2.Request(zabbixurl,createtigerjson)
    request=addheader(request)
    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        print "Auth Failed, Please Check Your Name And Password:",e.code
        sys.exit(3)
    else:
        response = json.loads(result.read())
        result.close()
        tigerid=response['result']['triggerids'][0] 
        return tigerid
        
def itemexits():
    c="xx"
def tigerexits():
    d="xxx"
        
def GetRecordList(dnsurl,user,passwd,domainid):
    postDict = {
        "login_email":user,
        "login_password":passwd,
        "format":"json",
        "domain_id":domainid
    }
    postData = urllib.urlencode(postDict);
    response = urllib2.Request(dnsurl, postData)
    resp = urllib2.urlopen(response).read()
    reqcon = json.loads(resp)
    return reqcon


if __name__=="__main__":
    '''
    dnsjson=GetRecordList(dnsurl,user,passwd,domainid)
    dnsrecord=dnsjson['records']

    for i in dnsrecord:
            type=i["type"]
            name=i["name"]
            value=i["value"]
            enabled=i["enabled"]
            line=i["line"]
            auth=loginzabbix(zabbixurl)
            if name != "@" and line=="默认" and enabled=="1" and name !="api-dev":
                try:
                    itemid=createitem(auth,name+".xxx.com","libexec[check_dig  -l "+name+".xxx.com -H 119.29.29.29  -T "+type+" -a "+value+"]",10169,0,1,59,2022,30)
                except Exception as e:
                    print name+"增加出现异常"
                    continue
                print name+"增加成功"
                tigerstr="{dns:"+"libexec[check_dig  -l "+name+".xxx.com -H 119.29.29.29  -T "+type+" -a "+value+"].count(#3,\"CRITICAL\",\"like\")}>2 or {dns:"+"libexec[check_dig  -l "+name+".xxx.com -H 119.29.29.29  -T "+type+" -a "+value+"].count(#3,\"WARNING\",\"like\")}>2 "
                createtiger(auth,name+".xxx.com"+"解析异常",tigerstr)
    '''
    iplist=["10.11.147.67","10.11.147.67","10.112.32.182","10.112.32.186","10.112.32.99","10.112.33.167","10.112.33.219","10.112.33.219","10.112.33.27","10.112.34.106","10.112.34.156","10.112.34.202","10.112.34.238","10.118.28.96","10.129.28.45","10.129.28.53","10.135.28.212","10.135.28.249","10.135.28.250","10.135.29.192","10.154.28.165","10.154.28.165","10.154.28.165","10.154.28.167","10.154.28.167","10.154.28.168","10.154.29.216","10.154.29.217","10.154.29.224","10.154.29.236","10.154.29.245","10.154.30.41","10.176.28.212","10.176.28.215","10.176.29.225","10.176.29.226","10.176.29.228","10.176.29.229","10.176.29.235","10.176.29.236","10.176.29.249","10.176.29.34","10.176.29.34","10.176.29.40","10.176.29.40","10.176.30.157","10.176.30.157","10.176.30.158","10.176.30.158","10.176.30.159","10.176.30.159","10.176.30.160","10.176.30.160","10.176.30.161","10.176.30.161","10.176.30.162","10.176.30.162","10.182.192.82","10.182.192.82","10.182.192.83","10.182.192.84","10.182.192.84","10.182.192.84","10.185.28.12","10.185.28.131","10.185.28.57","10.185.28.64","10.185.28.68","10.185.28.80","10.185.28.83","10.185.28.84","10.185.29.130","10.185.29.91","10.185.29.91","10.185.30.121","10.185.30.131","10.185.30.134","10.185.30.248","10.185.30.249","10.185.30.249","10.185.30.255","10.185.30.255","10.185.31.138","10.185.31.140","10.185.31.142","10.185.31.1","10.185.31.1","10.185.31.2","10.185.31.2","10.185.31.5","10.185.31.5","10.185.31.6","10.185.31.6","10.185.31.7","10.185.31.7","10.185.31.9","106.39.244.54","115.182.51.74","115.182.51.74","115.182.51.77","115.182.51.77","115.182.94.62","10.154.28.165","10.176.30.157","10.176.30.158","10.176.30.159","10.176.30.160","10.176.30.162","10.176.30.16","10.182.192.82","10.182.192.83","10.182.192.84","10.185.30.248","10.185.30.249","10.185.30.255","10.185.30.255","10.185.31.2","10.185.31.5","10.185.31.6","10.185.31.7","10.185.31.9","10.176.30.157","10.176.30.158","10.176.30.159","10.176.30.160","10.185.30.255","10.185.31.2","10.185.31.5","10.185.31.6","10.185.31.7","10.185.30.248","10.185.31.9","10.176.30.16","10.176.30.162","10.182.192.82","10.182.192.83","10.185.30.249","10.185.30.255","10.154.28.165","10.182.192.84","10.176.29.235","10.154.29.216","10.129.28.59","10.129.28.64","10.185.28.42","10.185.28.44","10.112.32.234","10.112.32.212","10.176.29.34","10.176.28.212 ","10.176.29.243","10.176.28.215","10.176.29.40   ","10.135.28.250","10.135.28.211","10.135.29.69","10.135.29.192","10.154.30.70","10.154.30.75","10.154.30.41","10.154.30.22","10.112.33.28","10.112.33.30","10.112.33.34","10.112.33.27","10.112.34.104","10.112.34.156","10.112.33.23","10.112.34.165","10.112.34.106","10.112.33.167 ","10.112.32.233","10.185.30.61","10.185.30.3","10.185.28.179 ","10.185.29.84","10.185.28.131","10.185.30.140","10.185.29.130 ","10.185.28.42   ","10.118.30.102","10.118.30.90","10.118.30.91   ","10.118.28.96   ","10.118.30.88","10.118.30.87   ","10.129.28.59","10.129.28.132","10.129.28.128","10.129.28.130","10.129.28.121","10.129.28.135","10.129.28.101","10.129.28.64","10.112.33.164","10.112.33.223","10.112.33.87","10.112.33.221","10.112.33.3","10.112.32.170","10.112.32.242","10.112.32.154","10.185.32.11","10.185.32.12","10.185.32.13","10.185.32.14","10.185.32.15","10.185.32.16","10.185.32.17","10.185.32.18","10.185.32.20","10.185.32.21","10.185.32.22","10.185.32.23","10.185.32.24","10.185.32.35","10.185.32.36","10.185.32.37","10.185.32.38","10.112.34.202","10.185.28.83","10.185.29.86","10.112.33.219","10.185.29.91","10.185.29.41","10.185.28.136","10.185.29.145","10.112.33.161","10.185.29.48","10.129.28.253","10.129.29.2","10.129.29.7","10.129.29.12","10.129.29.0","10.129.29.1","10.129.28.249","10.129.29.5","10.129.29.26","10.129.29.10","10.129.29.4","10.129.29.32","10.129.29.38","10.129.28.97","10.129.28.105","10.129.28.92","10.129.28.88","10.129.28.86","10.129.28.83","10.129.28.96","10.129.28.91","10.129.28.95","10.129.28.99","10.129.28.78","10.129.28.84","10.129.28.87","10.129.28.75","10.129.28.76","10.129.28.77","10.129.28.73","10.129.28.74","10.129.28.72","10.129.28.80","10.129.28.89","10.129.28.93","10.129.28.81","10.129.28.106","10.129.28.70","10.129.28.68","10.129.28.79","10.129.28.69","10.129.28.67","10.129.28.118"]
    for i in iplist:
        auth=loginzabbix(zabbixurl)
        print creaehost(i,1025,9,10147)    
            
    
    
    
    
    