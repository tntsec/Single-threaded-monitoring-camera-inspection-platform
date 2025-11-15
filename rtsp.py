import cv2,os,json,time,requests,codecs
from func_timeout import func_set_timeout
from multiprocessing import Process


@func_set_timeout(5)
def dayin():
    video1 = "rtsp://"+rtspconfig['name']+":"+rtspconfig['password']+"@"+rtspconfig['ip']+rtsp_config[rtspconfig['brand']]
    cap = cv2.VideoCapture(video1)  # 使用整数，此处打开的本地摄像头
    while 1:
        ret, frame = cap.read()
        if ret == False:  # 若没有帧返回，则重新刷新rtsp视频流
            continue
        else:
            break;
    # cv2.imshow("capture",frame)
    cv2.imwrite(nowdir+"\\"+rtspconfig['ip']+".jpeg", frame)
    cap.release()
    return rtspconfig['hostname']+"保存成功"

def get_config():
    config = json.loads(open("C:\\jiankong\\rtsp.json", encoding='utf-8').read())
    return config

def post_weixin(stats):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=用自己的'
    body = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": "监控摄像头自动巡检",
                    "description": stats,
                    "url": "90apt.com",
                    "picurl": "https://www.hikvision.com/content/dam/hikvision/cn/product/network-camera/fixed-ipc/%E7%BB%8F%E9%94%80%E7%B3%BB%E5%88%97/%E7%BB%8F%E9%94%80%E7%B3%BB%E5%88%97%E5%AF%BC%E8%88%AA%E7%9B%AE%E5%BD%95.jpg"
                }
            ]
        }}
    response = requests.post(url, json=body)
    print(response.text)
    print(response.status_code)


total = 0
fail = 0
weixindata = ""
rtsp_config = get_config()
print(rtsp_config)
#path1=os.path.abspath('.')
path1=("C:\\jiankong\\")
nowtime = time.strftime("%Y%m%d", time.localtime())
try:
    os.mkdir(path1 + "\\" + nowtime)
except:
    None
nowdir = (path1 + "\\" + nowtime)

for rtspconfig in rtsp_config['rtsp']:
    total = total + 1
    try:
        dayin()
    except:
        weixindata = weixindata + (rtspconfig['hostname']+" "+rtspconfig['ip']+" 网络或账号密码错误\n")
        fail = fail + 1
weixinpost = "总计巡检:"+str(total)+"台"+"，故障摄像头："+str(fail)+"台\n"+weixindata
post_weixin(weixinpost)
flog = codecs.open(nowdir+"\\"+nowtime+".log", 'w',encoding='utf-8')
flog.write(weixinpost)
flog.close()
