import re
import time

def is_phone_number(ph_num):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    if re.match(phone_pat, ph_num):
        return True
    else:
        return False

def get_current_date():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def is_mail_addr(mail):
    # 以数字或字母开头，@前仅含小写字母或数字，@后为xxx. com/net/gov/
    mail_pat = re.compile(r'^[a-z0-9][a-z0-9]{4,19}@[a-zA-Z0-9]{2,8}.[com|gov|net]')
    if re.match(mail_pat, mail):
        return True
    else:
        return False

def is_password_valid(password):
    p = re.compile(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,15}$')
    if re.match(p, password):
        return True
    else:
        return False


