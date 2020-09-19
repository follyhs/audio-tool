#i/bin/env python
#-*-coding:utf-8-*-
#2020/07/21
import sys
import json
import uuid
import time
import random
import string
import jsonpointer
import jsonpatch
import base64
import redis
import pymysql

sys.path.append('gen-py')
sys.path.append('/opt/bin/thrift')


#from thrift.Thrift import TType, TMessageType, TException, TApplicationException
#from thrift import Thrift
#from thrift.transport import TSocket
#from thrift.transport import TTransport
#from thrift.protocol  import TBinaryProtocol
#from genpython.prediction import Predictor
#from genpython.prediction.ttypes import *


'''def reqId():
    reuuid = uuid.uuid1()
    requestId = str(reuuid)
    return requestId.translate(None,'-')
'''

class RequestKeyWords(object):
    
    
    '''ROBOT_LIBRARY_SCOPE = 'Global' '''

    def __init__(self, host, port, data, type, serviceId, org, operation, tags):
        self.host = host
        self.port = int(port)
        self.org = org
        self.serviceId = serviceId
        self.type = type
        self.data = data
        #if operation != None:
            #self.operation = set(operation)
        #else：
            #self.operation = operation
        self.operation = operation
        #print self.operation
        self.tags = tags

    def reqId(self):
        reuuid = uuid.uuid1()
        requestId = str(reuuid)
        return requestId.translate(None,'-')

    def _reqdata(self):
        request = PredictRequest()
        request.requestId = self.reqId()
        request.serviceId = self.serviceId
        request.type = self.type
        request.organization = self.org
        request.appId = 'default_appId'
        request.eventId = 'default_eventId'
        request.tokenId = 'default_tokenId'
        request.timestamp = int(time.time())
        request.data = self.data.encode('utf-8')
        request.operation = self.operation
        request.tags = self.tags
        #print request
        return request

    def client(self):
        transport = TSocket.TSocket(self.host,self.port)
        transport = TTransport.TFramedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Predictor.Client(protocol)
        transport.open()
        try :
            
            result = client.predict(self._reqdata())
            print ("requestdata",self._reqdata())
            if result !=None:
                re_dict = {}
                #detail = result.detail.decode('utf-8')
                detail = result.detail
                re_dict["detail"] = json.loads(detail)
                re_dict["score"] = result.score
                re_dict["riskLevel"] = result.riskLevel
                re_dict["requestId"] = str(self.reqId())
                return re_dict    
        except PredictException as ex:

            ex_dict = {}
            ex_dict["resquestId"] = self.reqId()
            #ex_dict["code"] = ex.code
            ex_dict["message"] = ex.message
            #print "requestId = %s,code = %s,reslut = %s" %(reqId(),ex.code,ex.message)
            return ex_dict
        except TApplicationException as e:
            print ("requset err",e)
        except :
            s = sys.exc_info()
            print ("err %s happened line is %d" %(s[1],s[2].tb_lineno))

def thrift_request(ip, port, data, type = 'default_type', serviceId = 'POST_TEXT', org = 'IkzxwQ4vofwwvFqC8ir2', operation = None, tags = None):
    '''
    Set thrift request:
    
    Example:
    |${result} |thrift request |127.0.0.1 |8003 |{"XXX":"XX"} |AD |POST_TEXT |IkzxwQ4vofwwvFqC8ir2| write |tags|
    |${result} |thrift request |127.0.0.1 |8003 |{} |
    '''
    try:
        re_dict = {}
        request = RequestKeyWords(ip, port, data, type, serviceId, org, operation, tags)
        result = request.client()
        #str =  json.loads(json.dumps(result))
        return result

    except:

        s = sys.exc_info()
        return "error is %d line: %s" %(s[2].tb_lineno,s[1])


def ConvertToSet(plist):
    if (plist != None) and isinstance(plist,list):
        return set(plist)


def get_json_value(json_string,json_pointer):
    """
    Get the target node of the JSON document `json_string` specified by `json_pointer`.
    
    Example:
    | ${result}=       | Get Json Value   | {"foo": {"bar": [1,2,3]}} | /foo/bar |
    | Should Be Equal  | ${result}        | [1, 2, 3]                 |          |
    
    """
    value = json.dumps(jsonpointer.resolve_pointer(json_string, json_pointer)).encode('utf-8').decode('unicode_escape')
    return value

def Base64Fun(f):

    f = open(f,'rb')
    imgBase64 = base64.b64encode(f.read())
    f.close()
    return imgBase64

def Base64Str(f):

    f = open(f,'rb')
    imgBase64 = base64.encodestring(f.read())
    f.close()
    return imgBase64

def Rhgetall(keys,ip='10.66.121.171', port = '6379', passwd = 'crs-huhkvgpi:shumei123'):
    
    pool = redis.ConnectionPool(host = ip, port = port, password = passwd)
    r = redis.Redis(connection_pool = pool)
    return r.hgetall(keys)

def Rsmembers(keys,ip='10.66.121.171', port = '6379', passwd = 'crs-huhkvgpi:shumei123'):

    pool = redis.ConnectionPool(host = ip, port = port, password = passwd)
    r = redis.Redis(connection_pool = pool)
    return r.smembers(keys)

def Rttl(keys,ip='10.66.121.171', port = '6379', passwd = 'crs-huhkvgpi:shumei123'):

    pool = redis.ConnectionPool(host = ip, port = port, password = passwd)
    r = redis.Redis(connection_pool = pool)
    return r.ttl(keys)

def sotrByKey(array, key):

    array.sort(key = lambda x:x[key],reverse=True)
    return array

def get_mysqlvalue(host,db,sql):
       
        conn = pymysql.connect(host=host, port=3306, user='root', passwd='shumeitest2018', db=db, charset='utf8')
        cursor = conn.cursor()
        rowNums = cursor.execute(sql)
        conn.commit()
        value=cursor.fetchone()
        return value
def readfile(file):                                               
    with open(file,'r+') as f:            
        data =f.read()                                                                                                                                                                 
        str = ''.join(data)               
        return str     

if __name__ == '__main__':
    
    try:
        if (len(sys.argv) != 7):
            print ("Usge:<ip><port><type><serviceId><org><data>")
            pass
        else:
            ip = sys.argv[1]
            port = sys.argv[2]
            type = sys.argv[3]
            serviceId = sys.argv[4]
            org = sys.argv[5]
            data = sys.argv[6]
            print ("------call---------------------------")
            request = RequestKeyWords(ip,port,type,serviceId,org,data)
            result = request.client()
            print (result)
            print ("----------get value------------------------")
            print (get_json_value(result,'/detail/credit'))
            print (type(get_json_value(result,'/detail/credit')))
    except IndexError as e:
        print (e)
    except:
        s = sys.exc_info()
        print (" %s, happened line is %d" %(s[1],s[2].tb_lineno))


        


