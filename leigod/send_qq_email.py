import smtplib
from email.mime.text import MIMEText  # 发送文本
from email.mime.multipart import MIMEMultipart  # 生成多个部分的邮件体
from email.mime.image import MIMEImage  # 发送图片


def send_126_email():
    # 邮件内容设置
    message = MIMEText('你好呀，王思聪~~~', 'plain', 'utf-8')
    # 邮件标题设置

    message['Subject'] = '来自CSDN的问候'

    # 发件人信息
    message['From'] = sender

    # 收件人信息
    message['To'] = receivers[0]

    # 通过授权码,登录邮箱,并发送邮件
    try:
        server = smtplib.SMTP('smtp.126.com')  # 配置126邮箱的smtp服务器地址
        server.login(sender, password)
        server.sendmail(sender, receivers, message.as_string())
        print('发送成功')
        server.quit()

    except smtplib.SMTPException as e:
        print('error', e)


def send_qq_email(sender, receivers, password, email_title):
    # 构建邮件的主体对象
    body = '''
    '你tm忘记关雷神加速器了'
    '''
    msg = MIMEMultipart()
    content = MIMEText(body, 'html', 'utf-8')  # plain以文本形式发送,html以html格式发送
    msg['Subject'] = 'hello world'  # 文章标题
    msg['From'] = sender  # 发送人
    msg['To'] = receivers  # 收信人
    qqcode = 'jhudegkjxxubbhbe'
    msg.attach(content)  # 把邮件内容拼接到msg里面
    # 建立与邮件服务器的连接并发送邮件,qq要发多封，sleep
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 实例化 基于ssl,则smtplib.SMTP_SSL
        smtpObj.login(user=sender, password=qqcode)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
        print('邮件发送成功')
    except:
        print('邮件发送失败')


if __name__ == '__main__':
    # 配置邮箱信息
    sender = '173216244@qq.com'  # 发件人的地址
    password = 'jhudegkjxxubbhbe'  # 此处是我们刚刚在邮箱中获取的授权码
    receivers = ['173216244@qq.com', '3438065837@qq.com']  # 邮件接受方邮箱地址，可以配置多个，实现群发
    email_title = 'hello world'  # 文章标题

    send_qq_email(sender, receivers[0], password, email_title)
