import random
import requests
import json
import time
import Email
import module.red as red
import module.weibo as weibo
import module.tiktok as tiktok
import module.database as database


FILE_PATH = ''  # this is the path where you want to save the file
FILE_TIKTOK_USER_INFO = 'tiktok_user_info.txt'
FILE_WEIBO_USER_INFO = 'weibo_user_info.txt'
FILE_RED_USER_INFO = 'red_user_info.txt'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
COOKIE_TIKTOK = ""  # this is tiktok cookie, you can get it from browser devtools
COOKIE_WEIBO = ""  # this is weibo cookie, you can get it from browser devtools


HEADERS_TIKTOK = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE_TIKTOK,
    "Referer" : "https://www.douyin.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive"
}

URL_TIKTOK = "https://www.douyin.com/aweme/v1/web/user/profile/other/?device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&source=channel_pc_web&sec_user_id=MS4wLjABAAAAWxLpO0Q437qGFpnEKBIIaU5-xOj2yAhH3MNJi-AUY04&personal_center_strategy=1&profile_other_record_enable=1&land_to=1&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&cpu_core_num=12&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=138.0.0.0&browser_online=true&engine_name=Blink&engine_version=138.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7421552512153306650&uifid=edf0d417f427c69b9e8dcf334ec311738f5d7ef487ab7a4043d6c18231e232a4109a12adc1c3f7f26fa2b018a176235714142f663feeb21098188bf4013ef366563741f139de2078c9fe5c5a9e16e2b0c7d1fa1e6624a6be9bdcdcb270eaa660f92d81e5155ac350e039912a6ddffd03617a15174e734d88135a7a0ab96909e4333c0f699250832af144f04604d513c7b0a65888de3d30b6af5a78714ceff2af&msToken=4Eo8HNYtL2peOvUDjOFaQpg6ZeJz0KAfoIGpEGYHC0KVmfb04Dbkn3wd5Uk9yHupq8vBsluRFdRWwJPAz4dgmDMgtp62iGV1HYSPdcR4_5cD4BP77JMcPfnUI02p5hCcvT7Rc4PxZMHhdUNBo_ktOLUuKFUxbOC3G80vyMT3K6RSLJxkALH3dcvs&a_bogus=d70VhFyjDN8jFV%2Ft8CrSSI3UItoMNsWywaTxbe3PtNFDGXFOfmNjhPbDbowjAdVlumBTkoV7PfMMbEncKzUzZFnkqmpvS%2FwfK4AVnX0L0qwgblXkgNfQCL0q7JtbWOvETAofJIUlIt5P2x%2F4D1akUQ-y7AkJsYkpOqr6dn4aT9tDgFs9FrF%2FuxbdNXzrQOo59D%3D%3D&verifyFp=verify_mbs1oaak_WY03Wp9U_cfBg_4bEJ_Aei1_JI2G1u9OeiAN&fp=verify_mbs1oaak_WY03Wp9U_cfBg_4bEJ_Aei1_JI2G1u9OeiAN&x-secsdk-web-expire=1751728405145&x-secsdk-web-signature=65b6e804e9c82d8be4115c27e02aa650"
# Example: "https://www.douyin.com/web/api/v2/user/info/?user

HEADERS_WEIBO = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE_WEIBO,
    "Referer": "https://weibo.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive"
}
USER_ID = "1669879400"
URL_WEIBO_HOME = "https://weibo.com/ajax/profile/info?uid=" + USER_ID

db = database.DataBase()
weibo_info = weibo.getWeiboInfo()


def time_stamp():
    time_stamp = time.time()
    local_time = time.localtime(time_stamp)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return str_time

def file_writer(filename, data):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(data + '\n')

def check_weibo():
    str_time = time_stamp()
    file_name = FILE_PATH + FILE_WEIBO_USER_INFO

    weibo_user_info = weibo_info.get_weibo_user_info()
    user_info_db, user_info_db_dict = db.search_weibo()

    if weibo_user_info is None:
        print("微博用户信息获取失败，跳过写入")
        Email.send_email(subject="微博用户信息获取失败", content="微博用户信息获取失败，请检查网络连接或API是否正常。")
    else:
        user_info = "时间：{}\t昵称：{}\t简介：{}\t转评赞：{}\t累计评论量：{}\t累计获赞：{}\t粉丝数：{}\t关注数：{}\t微博数：{}".format(
            str_time,
            weibo_user_info["昵称"],
            weibo_user_info["简介"],
            weibo_user_info["转评赞"],
            weibo_user_info["累计评论量"],
            weibo_user_info["累计获赞"],
            weibo_user_info["粉丝数"],
            weibo_user_info["关注数"],
            weibo_user_info["微博数"]
        )

        print("weibo用户信息： ", user_info)
        user_info_tuple = (weibo_user_info["昵称"], weibo_user_info["简介"], weibo_user_info["转评赞"], weibo_user_info["累计评论量"], weibo_user_info["累计获赞"], weibo_user_info["粉丝数"], weibo_user_info["关注数"], weibo_user_info["微博数"], str_time)

        if user_info_tuple[:-1] == user_info_db[1:-1]:
            print("weibo数据未变化，跳过写入")
            file_writer(file_name, user_info)
        else:
            if weibo_user_info["关注数"] != user_info_db_dict["关注数"]:  # 如果关注数有变化, 获取关注用户信息
                weibo_follower_info, weibo_follower_count = weibo_info.get_follower_data(USER_ID)
                follower_info = []
                for follower in weibo_follower_info:
                    follower_info.append("昵称：" + follower["screen_name"] + "\t主页链接： https://weibo.com/u/" + str(follower["id"]))
                Email.send_email(subject="微博用户信息更新", content=user_info + "\n关注用户信息：\n" + "\n".join(follower_info))

            elif weibo_user_info["粉丝数"] != user_info_db_dict["粉丝数"]:  # 如果粉丝数有变化, 获取粉丝信息
                weibo_follower_info, weibo_fans_count = weibo_info.get_fans_data(USER_ID)
                fans_info = []
                for fan in weibo_follower_info:
                    fans_info.append("昵称：" + fan["screen_name"] + "\t主页链接： https://weibo.com/u/" + str(fan["id"]))
                Email.send_email(subject="微博用户信息更新", content=user_info + "\n粉丝用户信息：\n" + "\n".join(fans_info))
            else:
                Email.send_email(subject="微博用户信息更新", content=user_info)

            file_writer(file_name, "数据改变    " + user_info)
            print("weibo数据已更新，写入数据库", user_info_tuple)
            db.insert_weibo(user_info_tuple)


def check_tiktok():
    response = requests.get(URL_TIKTOK, headers=HEADERS_TIKTOK, timeout=10)
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return 
    if not response.text:
        print("请求失败，响应内容为空", response.text)
        return
    try:
        response_json = json.loads(response.text)
    except json.JSONDecodeError as e:
        print("JSON解析失败:", e)
        return
    str_time = time_stamp()
    tiktok_user_info = response_json["user"]
    follower_count = tiktok_user_info["follower_count"]           # 粉丝数
    following_count = tiktok_user_info["following_count"]         # 关注数
    total_favorited = tiktok_user_info["total_favorited"]         # 获赞数
    aweme_count = tiktok_user_info["aweme_count"]                 # 作品数
    favoriting_count = tiktok_user_info["favoriting_count"]       # 喜欢作品数
    user_info = "时间：{}\t{}\t粉丝数：{}\t关注数：{}\t获赞数：{}\t作品数：{}\t喜欢作品数：{}".format(
        str_time,
        tiktok_user_info["ip_location"],
        follower_count,
        following_count,
        total_favorited,
        aweme_count,
        favoriting_count
    )
    print(user_info)
    user_info_tuple = (follower_count, following_count, total_favorited, aweme_count, favoriting_count, str_time)
    use_info_db = database.search_tiktok()

    if user_info_tuple[:-1] == use_info_db[1:-1]:
        print("tiktok数据未变化，跳过写入")
    else:
        database.insert_tiktok(user_info_tuple)
        print("tiktok数据已更新，写入数据库", user_info_tuple)
        Email.send_email(subject="TikTok用户信息更新", content=user_info)

    filename = FILE_PATH + FILE_TIKTOK_USER_INFO
    file_writer(filename, user_info)


def check_red():
    str_time = time_stamp()
    file_name = FILE_PATH + FILE_RED_USER_INFO

    red_info = red.get_red_user_info()
    red_user_info_database = database.search_redbook()
    if red_info is None:
        print("小红书用户信息获取失败，跳过写入")
        Email.send_email(subject="小红书用户信息获取失败", content="小红书用户信息获取失败，请检查网络连接或API是否正常。")
        return
    else:
        red_user_info_request = (red_info["user_id"], red_info["nickname"], red_info["ip_location"], red_info["description"], 0, red_info["follows"], red_info["fans"], red_info["interaction"], str_time)
        
        red_user_info = "时间：{}\t账号：{}\t昵称：{}\t位置：{}\t签名：{}\t关注数：{}\t粉丝数：{}\t互动量：{}".format(
                str_time,
                red_info["user_id"],
                red_info["nickname"],
                red_info["ip_location"],
                red_info["description"],
                red_info["follows"],
                red_info["fans"],
                red_info["interaction"]
            )
        print("小红书用户信息：", red_user_info)
        if red_user_info_database[1:-1] == red_user_info_request[:-1]:
            print("小红书数据未变化，跳过写入")
        else:
            print("red数据库信息： ", red_user_info_database[1:-1])
            print("red请求信息： ", red_user_info_request[:-1])
            database.insert_redbook(red_user_info)
            Email.send_email(subject="小红书用户信息更新", content=red_user_info)
            file_writer(file_name, "数据改变    " + red_user_info)


if __name__ == "__main__":
    check_tiktok()
    check_weibo()
    check_red()