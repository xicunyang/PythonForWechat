# 导入微信的接口包
import itchat
import os
import random
from PIL import Image
import math
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud


def login():
    """
    登录模块
    :return:
    """
    # 微信登录
    itchat.auto_login(hotReload=True)


def get_head_image():
    """
    获取头像到本地
    :return:
    """
    # 获取到所有好友
    friends = itchat.get_friends(update=True);
    print(type(friends))
    print(itchat.get_friends())
    # 获取到所有好友的个数
    friendsNum = len(friends)

    # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)
    # 组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
    for count, f in enumerate(friends):
        # 保留两位小数，并已  55.57%  的形式打印
        print(str(round(count / friendsNum * 100, 2)) + "%")
        # 根据用户名获取头像
        img = itchat.get_head_img(f["UserName"])

        if f["RemarkName"] != "":
            name = f["RemarkName"]
        else:
            name = f["NickName"]
        # 保存头像
        fOpen = open("img/" + name + ".jpg", "wb")
        fOpen.write(img)
        fOpen.close()


def create_big_image():
    """
    将获取到的头像进行拼接大图
    :return:
    """
    x = 0
    y = 0
    # 将文件夹中的文件保存到变量--list中
    # ['&amp;.jpg', '1379守望台.jpg', '15  韩语   尹霞.jpg', '16物电孙悦.jpg']
    images = os.listdir("img")
    # 将顺序打乱
    random.shuffle(images)
    # 创建1080*1080尺寸的图片来存放头像照片
    newImg = Image.new("RGBA", (1080, 1080))
    # 使用math.sqrt来计算长宽
    width = int(math.sqrt(1080 * 1080 / len(images)))
    # 计算有几行
    lineNum = int(1080 / width)
    # 遍历
    for i in images:
        # 打开图片
        img = Image.open("img/" + i)
        # 缩小图片  ANTIALIAS --> 抗锯齿  平滑
        img = img.resize((width, width), Image.ANTIALIAS)
        # (x * width, y * width)  是坐标  paste 粘在一起的意思
        newImg.paste(img, (x * width, y * width))
        # 向后移一位
        x += 1
        # x到了最后了
        if x > lineNum:
            # x回到初始
            x = 0
            # 另起一行
            y += 1
    # 保存图片
    newImg.save("all.png")


def collect_sex():
    """
    手机好友的性别--制作词云图
    :return:
    """
    friends = itchat.get_friends(update=True)
    print(friends)
    # 先声明一个性别空字典
    sex = dict()
    for f in friends:
        if f["Sex"] == 1:
            # 男   这个0我猜是默认值  没有man的时候  取到0  有man的时候  取到该值
            # 很优秀  学习这样设置值
            sex["man"] = sex.get("man", 0) + 1
        elif f["Sex"] == 2:
            # 女
            sex["women"] = sex.get("women", 0) + 1
        else:
            sex["unknown"] = sex.get("unknown", 0) + 1
    print(sex)

    for i, key in enumerate(sex):
        # 制作柱状图
        plt.bar(key, sex[key])
    # 展示图
    plt.show()


def get_signature():
    """
    获取用户的个性签名
    :return:
    """
    friends = itchat.get_friends(update=True)
    file = open("sign/sign.txt", "a", encoding="UTF-8")
    for f in friends:
        signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        # 正则匹配
        rec = re.compile("1f\d+\w*|[<>/=]")
        signature = rec.sub("", signature)
        file.write(signature + "\n")


def create_word_cloud():
    """
    制作词云图的方法
    :return:
    """
    text = open("sign/sign.txt", encoding="UTF-8").read()
    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，window在C:\Windows\Fonts\下，mac下可选/System/Library/Fonts/PingFang.ttc 字体
        font_path='/System/Library/Fonts/PingFang.ttc',
        height=1500,
        width=1500,
        # 设置字体最大值
        max_font_size=60,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=30,
    )
    # 生成词云  generate  生成的意思
    myWord = wc.generate(text)
    plt.imshow(myWord)
    plt.axis("off")
    plt.show()
    wc.to_file("sign/word_cloud.png")


if __name__ == '__main__':
    # create_big_image()
    # login()
    create_big_image()
