# 1. 实现关闭雷神加速器功能
# 2. 实现每晚定时12点运行程序
# 3. 发送邮箱告知

import json
import requests
import hashlib
import smtplib
from email.mime.text import MIMEText  # 发送文本
from email.mime.multipart import MIMEMultipart  # 生成多个部分的邮件体


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


def pause(account_token, password_email):
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
    code = resp2["code"]

    # 配置邮箱信息
    sender = '173216244@qq.com'  # 发件人的地址
    receivers = ['173216244@qq.com', '2788076733@qq.com']  # 邮件接受方邮箱地址，可以配置多个，实现群发

    if code == 400803:
        # print("本来就在暂停状态！")
        send_qq_email(sender, receivers[0], password_email, email_title='本来就在暂停状态！', email_body='')
    elif code == 0:
        # print("成功暂停！正在发送邮件中……")
        send_qq_email(sender, receivers[0], password_email, email_title='小b又忘了关雷神是吧', email_body='')
    else:
        # print("未能成功暂停！")
        send_qq_email(sender, receivers[0], password_email, email_title='出问题了，怪闷', email_body='')


def get_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def send_qq_email(sender, receivers, password_email, email_title, email_body):
    # 构建邮件的主体对象
    body = email_body
    msg = MIMEMultipart()
    content = MIMEText(body, 'html', 'utf-8')  # plain以文本形式发送,html以html格式发送
    msg['Subject'] = email_title  # 文章标题
    msg['From'] = sender  # 发送人
    msg['To'] = receivers  # 收信人
    msg.attach(content)  # 把邮件内容拼接到msg里面
    # 建立与邮件服务器的连接并发送邮件,qq要发多封，sleep
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 实例化 基于ssl,则smtplib.SMTP_SSL
        smtpObj.login(user=sender, password=password_email)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
        print('邮件发送成功')
    except:
        print('邮件发送失败')


def main_handler(event, context):
    # 配置雷神加速器账号信息
    uname = "13775062601"
    password = "sjkjw173216244"
    password_email = "jhudegkjxxubbhbe"

    # 获取雷神token
    account_token = get_account_token(uname, password)

    # 暂停雷神加速器
    pause(account_token, password_email)

