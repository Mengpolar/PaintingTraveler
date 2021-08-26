import json
import time
import requests


config = None

# 读取配置文件 config.json
def get_config():
    try:
        with open('hlr.json', 'r') as f:
            config = json.load(f)
    except:
        config = {}

    return config


# 写日志 log
def log(status, log_data):
    today = time.strftime("%Y%m%d", (time.localtime()))
    with open('log/'+today, 'a') as f:
        now = time.strftime("%Y.%m.%d %H:%M:%S", (time.localtime()))
        if status:
            f.write('[+] ' + now + ' ' + log_data + '\n')
        else:
            f.write('[-] ' + now + ' ' + log_data + '\n')

    return


def daily_check():
    for i in config:
        bind_id = i['bindId']
        if not bind_id:
            continue
        
        headers = {
            "Host": "ums.tc.netease.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
        }
        url = 'http://ums.tc.netease.com/g99/h5/bind/sign_in?bindId={}'.format(bind_id)
        req = requests.get(url, headers=headers, timeout=10)

        req_dict = json.loads(req.text)
        # {"result":[2],"succ":true}
        # {"code":"already.signin","succ":false,"message":"今天已经签到过啦，明天再来吧"}
        if req_dict["succ"]:
            log(True, "时空中的绘旅人 {} 签到成功".format(i['name']))
        if not req_dict["succ"]:
            log(False, "时空中的绘旅人 {} {}".format(i['name'], req_dict["message"]))


while True:
    config = get_config()

    # 晚上23-早上9 不运行(免打扰)
    hour = int(time.strftime("%H", (time.localtime())))
    if hour>=23 or hour<9:
        time.sleep(3600) # 休眠1小时
        continue

    # 查看是否存在配置文件
    if not config:
        time.sleep(60) # 休眠1分钟
        continue

    today = time.strftime("%Y%m%d", (time.localtime()))
    today_log = ''
    try:
        with open('log/'+today, 'r') as f:
            today_log = f.read()
    except:
        today_log = ''
    
    if today_log:
        # 今天已经运行过了，明天再运行吧(防喝茶)
        time.sleep(600) # 休眠10分钟
        continue

    # 签到
    try:
        daily_check()
    except:
        pass

    time.sleep(600) # 休眠10分钟