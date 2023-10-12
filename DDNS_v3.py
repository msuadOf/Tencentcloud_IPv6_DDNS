import json
import sys
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models
from urllib import request 
from urllib import error
import load_config
import os
#################### 修改以下位置即可 ##########################
SecretKey = {
    "SecretId": 'xxxxx',        # SecretId
    "secretKey": 'xxxxx'        # secretKey
}
(SecretKey["SecretId"],SecretKey["secretKey"])=load_config.getKey(str(os.path.dirname(os.path.abspath(__file__))) +"/"+"key.yaml")
params = {
    "Domain": "02f.cc",      # 域名，例如：baidu.com
    "Subdomain": 'v6'          # 子域名，例如：www
}
###############################################################

import re

import socket
def getipv6():
    host_ipv6=[]
    ips=socket.getaddrinfo(socket.gethostname(),80)
    for ip in ips:
        if ip[4][0].startswith('24'):
    #2408 中国联通
    #2409 中国移动
    #240e 中国电信
    #        print(ip[4][0])
            host_ipv6.append(ip[4][0])
    return host_ipv6




def getIPv6Address():
    output = os.popen("ipconfig /all").read()
    # print(output)
    result = re.findall(r"IPv6 地址 . . . . . . . . . . . . : ([a-f0-9:]*::[a-f0-9:]*)", output, re.I)
    return result[0]

def get_ip():
    # 获取IP地址
    try:
        #IPv6 = str(request.urlopen("https://api6.ipify.org").read().decode('utf8'))
        IPv6=getipv6()[1]
        if IPv6:
            print("获取IPv6成功,",IPv6)
            return IPv6
        else:
            print("获取IPv6失败,请查询是否支持IPV6",)
            sys.exit()
    except TimeoutError:
        print("获取IPv6超时,请查询是否支持IPV6",)
        sys.exit()
    except error.URLError:
        print("获取IPv6连接错误,请查询是否支持IPV6",)
        sys.exit()
        
try:
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential(SecretKey["SecretId"], SecretKey["secretKey"])
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "dnspod.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = dnspod_client.DnspodClient(cred, "", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.DescribeRecordListRequest()
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个DescribeRecordListResponse的实例，与请求对象对应
    resp = client.DescribeRecordList(req)
   
    #获取记录ID和LINE参数
    recordid = resp.RecordList[0].RecordId
    recordline = resp.RecordList[0].Line

    #获取本机IPV6dizhi
    IPv6 = get_ip()

    #参数赋值
    update_paparams = {
        "Domain": params["Domain"],
        "SubDomain": params["Subdomain"],
        "RecordId": recordid,
        "RecordLine": recordline,
        "Value": IPv6,
    }
    
    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.ModifyDynamicDNSRequest()
    req.from_json_string(json.dumps(update_paparams))
    print("====实例化一个请求对象,每个接口都会对应一个request对象====")

    # 返回的resp是一个ModifyDynamicDNSResponse的实例，与请求对象对应
    resp = client.ModifyDynamicDNS(req)
    
    # 输出json格式的字符串回包
    print(resp.to_json_string())
    print("====exec over====")

except TencentCloudSDKException as err:
    print(err)
