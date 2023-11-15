import json
import requests
import configparser
import os
import hashlib


def get_account_token(uname, passport):
    url = "https://webapi.leigod.com/api/auth/login"
    passport = get_md5(passport)

    payload = "{\"username\":\"" + uname + "\",\"password\":\"" + passport + "\",\"user_type\":\"0\",\"src_channel\":\"guanwang\",\"country_code\":86,\"lang\":\"zh_CN\",\"region_code\":1,\"account_token\":null}"
    headers = {
      'authority': 'webapi.leigod.com',
      'accept': 'application/json, text/plain, */*',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp1 = json.loads(response.text)
    account_token = resp1["data"]["login_info"]["account_token"]
    print("account_token:", account_token)

    return account_token


def pause(account_token):
    url = "https://webapi.leigod.com/api/user/pause"

    payload = json.dumps({
      "account_token": account_token,
      "lang": "zh_CN"
    })
    headers = {
      'authority': 'webapi.leigod.com',
      'accept': 'application/json, text/plain, */*',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp2 = json.loads(response.text)
    print(resp2)
    code = resp2["code"]
    print("code:", code)

    if code == 400803:
        print("本来就在暂停状态！")
    elif code == 0:
        print("成功暂停！")
    else:
        print("未能成功暂停！")


def get_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def if_leigod_is_running():  # 判断雷神加速器是否在后台
    ls = appname.split(',')
    WMI = win32com.client.GetObject('winmgmts:')
    for i in ls:
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name like "%{}%"'.format(i + '.exe'))
        if len(processCodeCov) > 0:
            return '检测到{}'.format(i)
    return False


if __name__ == '__main__':
    proDir = os.path.split(os.path.realpath(__file__))[0]
    configPath = os.path.join(proDir, "config.ini")
    # 读取.ini文件
    conf = configparser.ConfigParser()
    conf.read(configPath, encoding='UTF-8-sig')
    uname = conf.get("config", "uname")
    password = conf.get("config", "password")
    # appname = self.conf.get('config', 'games')
    # sec = int(self.conf.get('config', 'looptime'))
    # update = int(self.conf.get("config", "update"))

    # print('''
    #         ***************************************************\n
    #         *                                                 *\n
    #         *                                                 *\n
    #         *              雷神加速器提醒暂停工具v1.0            *\n
    #         *                     正在运行                     *\n
    #         *                     作者:sjkstroker              *\n
    #         *                                                 *\n
    #         ***************************************************\n
    #         ''')

    account_token = get_account_token(uname, password)
    pause(account_token)
