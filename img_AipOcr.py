from aip import AipOcr  # 引入百度文字识别模块

# 百度智能云文字识别接口（免费）
APPID = ""
APIKEY = ""
SECRETKEY = ""

OCR = AipOcr(APPID, APIKEY, SECRETKEY)  # 创建文字识别

with open(r'在此替换目标图片路径', 'rb') as f:
    img = f.read()  # 读取目标图片

data = OCR.basicGeneral(img)  # 识别图片文字 tpye(data)=dict

contents = (data['words_result'])

# s = [i['words'] for i in contents]
# print(''.join(s))  # 以段落的形式打印图片所有文字

for i in contents:
    print(i['words'])  # 遍历打印所有行文字

