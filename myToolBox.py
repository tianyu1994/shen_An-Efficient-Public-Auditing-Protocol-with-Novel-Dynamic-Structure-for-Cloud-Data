import random, string, os, zipfile
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, GT, pair
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def GenRandomSerial(length, Digit=True, Letter=False):
    #生成一个由数字或（和）字符的组成的随机序列
    numOfNum = 0
    numOfLetter = 0
    if Digit == True and Letter == True:
        numOfNum = random.randint(1, length - 1)
        numOfLetter = length - numOfNum
    elif Digit == True:
        numOfNum = length
    elif Letter == True:
        numOfLetter = length
    # 选中 numOfNum 个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    # 选中 numOfLetter 个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    # 打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    # 生成密码
    genPwd = ''.join([i for i in slcChar])
    return genPwd


def getUniqueRandomNum(sum, choice):
    selected = [i for i in range(sum)]
    random.shuffle(selected)
    selected = sorted(selected[:choice])

    return selected

def getChaoticRandomNum(sum, choice):
    selected = [i for i in range(sum)]
    random.shuffle(selected)
    selected = selected[:choice]
    return selected

def ZipFile(source_dir, dst, fliter:list):
    f = zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.split('.')[1] in fliter:
                f.write(os.path.join(dirpath,filename))
    f.close()

def send_mail(to_list, sub, content, attachment):
    mail_user = ''
    mail_postfix = ''
    mail_host = ''
    mail_pass = ''

    me = "AlfredNan" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    att1 = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename=Results.zip'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    msg.attach(att1)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as err:
        print(str(err))
        return False

if __name__ == '__main__':
    mailto_list = ['wqchen@hqu.edu.cn']
    if send_mail(mailto_list, "实验结果", "恭喜获得实验结果", '../Results.zip'):
        print("发送成功")
    else:
        print("发送失败")