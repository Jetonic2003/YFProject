import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# 创建邮件主体对象
email = MIMEMultipart()
# 设置发件人、收件人和主题
email['From'] = '15327327862@163.com'
email['To'] = '1657712828@qq.com'
email['Subject'] = Header('FBI warning', 'utf-8')
# 添加邮件正文内容
content = """FBI open the door"""
email.attach(MIMEText(content, 'plain', 'utf-8'))
# 创建SMTP_SSL对象（连接邮件服务器）
smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)
# 通过用户名和授权码进行登录
smtp_obj.login('15327327862@163.com', 'UJSNRLCSKVMDHIQR')
# 发送邮件（发件人、收件人、邮件内容（字符串））
smtp_obj.sendmail(
     '15327327862@163.com',
     '1657712828@qq.com',
     email.as_string()
)