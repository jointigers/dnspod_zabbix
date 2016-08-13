#coding=utf-8
import json
import urllib
import urllib2
import sys
dnsurl="https://dnsapi.cn/Record.List"
user="e.com"
passwd="~"
domainid="26856323"

zabbixurl="http://zabbix.xxx.net/api_jsonrpc.php"
zabbixuser="adminapi"
zabbixpass="adminapi"

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

            
            
            
    
    
    
    
    