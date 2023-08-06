import unittest
from aliyun_sms.sms import Sms

class TestSms(unittest.TestCase):

    def test_send(self):
        sms = Sms("LTAI4G5ZTT3Pn5cUF8f2mjnF","HXFLvaCQNgTfAOXz9fBcUiAxx6xsOg")
        res = sms.sendSms("18561363632","聚辉工业服务","SMS_195221233",{
            "name":"Kevin Kong",
            "result": "成功"
        })
        print(res)

if __name__ == "__main__":
    unittest.main()