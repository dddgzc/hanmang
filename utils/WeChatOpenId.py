import json,requests,hashlib,random,string
from hanmang import settings

class WeChatOpenId():

    @staticmethod
    def getWeChatOpenId(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code' \
            .format(settings.APP_ID, settings.APP_KEY, code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid

    @staticmethod
    def geneAuthCode( member_info = None ):
        m = hashlib.md5()
        str = "%s-%s"%(member_info.id,member_info.salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt( length = 16 ):
        keylist = [ random.choice( ( string.ascii_letters + string.digits ) ) for i in range( length ) ]
        return ( "".join( keylist ) )