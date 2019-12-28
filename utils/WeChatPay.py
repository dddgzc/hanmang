# 生成随机字符串
import hashlib
import time
from hanmang.settings import Mch_id,APP_ID
from bs4 import BeautifulSoup
from apps.users.models import UserProfile
from apps.operations.models import UserOrder

def getNonceStr():
    import random
    data="123456789zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
    nonce_str  = ''.join(random.sample(data , 30))
    return nonce_str

# 生成签名

def paysign(appid, body, mch_id, nonce_str, notify_url, openid, out_trade_no, spbill_create_ip, total_fee):
    ret = {
        "appid": appid,
        "body": body,
        "mch_id": mch_id,
        "nonce_str": nonce_str,
        "notify_url": notify_url,
        "openid": openid,
        "out_trade_no": out_trade_no,
        "spbill_create_ip": spbill_create_ip,
        "total_fee": total_fee,
        "trade_type": 'JSAPI'
    }

    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA, Mch_id)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()


# 生成商品订单号
def getWxPayOrdrID():
    import datetime

    date = datetime.datetime.now()
    # 根据当前系统时间来生成商品订单号。时间精确到微秒
    payOrdrID = date.strftime("%Y%m%d%H%M%S%f")
    return payOrdrID



#获取返回给小程序的paySign
def get_paysign(prepay_id,timeStamp,nonceStr):
    pay_data={
                'appId': APP_ID,
                'nonceStr': nonceStr,
                'package': "prepay_id="+prepay_id,
                'signType': 'MD5',
                'timeStamp':timeStamp
    }
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA,Mch_id)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()


# 获取全部参数信息，封装成xml,传递过来的openid和客户端ip，和价格需要我们自己获取传递进来
def get_bodyData(openid, client_ip, price, course):
    body = 'Mytest'  # 商品描述
    notify_url = 'https://www.baidu.com/'  # 填写支付成功的回调地址，微信确认支付成功会访问这个接口
    nonce_str = getNonceStr()  # 随机字符串
    out_trade_no = getWxPayOrdrID()  # 商户订单号
    price = float(price)*100
    total_fee = str(price)  # 订单价格，单位是 分
    # 获取签名
    sign = paysign(APP_ID, body, Mch_id, nonce_str, notify_url, openid, out_trade_no, client_ip, total_fee)
    # 存储订单信息
    create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    user = UserProfile.objects.get(openid=openid)
    UserOrder(order_desc=body,order_sn=out_trade_no,created_time=create_time,user=user,course=course,pay_price=price).save()

    bodyData = '<xml>'
    bodyData += '<appid>' + APP_ID + '</appid>'  # 小程序ID
    bodyData += '<body>' + body + '</body>'  # 商品描述
    bodyData += '<mch_id>' + Mch_id + '</mch_id>'  # 商户号
    bodyData += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
    bodyData += '<notify_url>' + notify_url + '</notify_url>'  # 支付成功的回调地址
    bodyData += '<openid>' + openid + '</openid>'  # 用户标识
    bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
    bodyData += '<spbill_create_ip>' + client_ip + '</spbill_create_ip>'  # 客户端终端IP
    bodyData += '<total_fee>' + total_fee + '</total_fee>'  # 总金额 单位为分
    bodyData += '<trade_type>JSAPI</trade_type>'  # 交易类型 小程序取值如下：JSAPI

    bodyData += '<sign>' + sign + '</sign>'
    bodyData += '</xml>'

    print(bodyData)

    return bodyData


def xml_to_dict(xml_data):
    """
    xml转换为字典
    :param xml_data:
    :return:
    """
    soup = BeautifulSoup(xml_data, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    # 将 XML 数据转化为 Dict
    data = dict([(item.name, item.text) for item in xml.find_all()])
