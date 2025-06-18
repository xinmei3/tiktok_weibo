import random
import requests
import json
import time
from database import DataBase
import Email


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

URL_TIKTOK = "https://www.douyin.com/aweme/v1/web/user/profile/other/?device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&source=channel_pc_web&sec_user_id=MS4wLjABAAAAHpssvF9y7F9lx-CAY8EKmdMnUTHkcNiT6EKXgX3iXh0&personal_center_strategy=1&profile_other_record_enable=1&land_to=1&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&cpu_core_num=12&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=136.0.0.0&browser_online=true&engine_name=Blink&engine_version=136.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7421552512153306650&uifid=edf0d417f427c69b9e8dcf334ec311738f5d7ef487ab7a4043d6c18231e232a4109a12adc1c3f7f26fa2b018a176235714142f663feeb21098188bf4013ef366563741f139de2078c9fe5c5a9e16e2b0c7d1fa1e6624a6be9bdcdcb270eaa660f92d81e5155ac350e039912a6ddffd03617a15174e734d88135a7a0ab96909e4333c0f699250832af144f04604d513c7b0a65888de3d30b6af5a78714ceff2af&msToken=wkPUW3u6KKDxYGuTb_OKFVNZf13yClKwJsDaxbQ4yWMmi80pVaotb-ZqM_Q21250NCrmP4QPps3_y3C-wn9ZREAw5F7eEL_cwcrNrC5alP3-AmN6vkAMsL5OBD2vGtOpQJ6soLKlN7-s4M7crs2bkP71MnQ1Yx5GTvHuEtQUnD0P3EiMCd_ebtE%3D&a_bogus=OJ4RhF7Edd%2FVcd%2FtYKjWHW2UWHDlNTWyZaTxRr3T7PY1G1Ma4mP5oaakroqOQ5o8ampTiKI7jVF%2FYEnc%2FGXiZFrpwmkDS%2FXbGsVCVUmo8qhpGPi23HfmCXUFqXsK85GNa559il7V8UrLZfx-wqQL%2FQVSeKYC5QShQZOyk%2FYCY9G6ZMLADpcaPBGpEXrn01cX&verifyFp=verify_m98o1t5a_8ntZgkr9_RCtL_4tqm_8c5s_zREsXpAbujws&fp=verify_m98o1t5a_8ntZgkr9_RCtL_4tqm_8c5s_zREsXpAbujws"

HEADERS_WEIBO = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE_WEIBO,
    "Referer": "https://weibo.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive"
}

URL_WEIBO_HOME = "https://weibo.com/ajax/profile/info?uid="

database = DataBase()


def time_stamp():
    time_stamp = time.time()
    local_time = time.localtime(time_stamp)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return str_time

def weibo():
    try:
        time.sleep(random.randint(10, 20))  # 随机等待10到20秒
        response = requests.get(URL_WEIBO_HOME, headers=HEADERS_WEIBO)
        response_json = json.loads(response.text)

        str_time = time_stamp()
        weibo_info_xiang = response_json['data']['user']
        likes_received_all = weibo_info_xiang["status_total_counter"]["total_cnt_format"]
        comments_received = int(weibo_info_xiang["status_total_counter"]["comment_cnt"])
        likes_received = int(weibo_info_xiang["status_total_counter"]["like_cnt"])
        followers_count = weibo_info_xiang["followers_count"]
        friends_count = weibo_info_xiang["friends_count"]
        statuses_count = weibo_info_xiang["statuses_count"]
        
        user_info = "时间：{}\t总获赞数：{}\t评论量：{}\t获赞数：{}\t粉丝数：{}\t关注数：{}\t微博数：{}".format(
            str_time,
            likes_received_all,
            comments_received,
            likes_received,
            followers_count,
            friends_count,
            statuses_count,
        )
        print(user_info)
        user_info_tuple = (likes_received_all, comments_received, likes_received, followers_count, friends_count, statuses_count, str_time)
        use_info_db = database.search_weibo()
        # print(user_info_tuple[:-1], use_info_db[1:-1])
        if user_info_tuple[:-1] == use_info_db[1:-1]:
            print("weibo数据未变化，跳过写入")
        else:
            database.insert_weibo(user_info_tuple)
            print("weibo数据已更新，写入数据库", user_info_tuple)
            Email.send_email(subject="微博用户信息更新", content=user_info)

        with open('weibo_user_info.txt', 'a', encoding='utf-8') as f:
            f.write(user_info + '\n')
    except (requests.RequestException, json.JSONDecodeError) as e:
        print("请求或解析失败:", e)
        Email.send_email(subject="微博请求或解析失败", content=str(e))
        exit()


def tiktok():
    try:
        time.sleep(random.randint(10, 20))  # 随机等待10到20秒
        respones = requests.get(URL_TIKTOK, headers=HEADERS_TIKTOK, timeout=10)
        response_json = json.loads(respones.text)
    
        str_time = time_stamp()
        tiktok_user_info = response_json["user"]
        follower_count = tiktok_user_info["follower_count"]  # 粉丝数
        following_count = tiktok_user_info["following_count"] # 关注数
        total_favorited = tiktok_user_info["total_favorited"] # 获赞数
        aweme_count = tiktok_user_info["aweme_count"] # 作品数
        favoriting_count = tiktok_user_info["favoriting_count"] # 喜欢作品数
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
 
        with open('tiktok_user_info.txt', 'a', encoding='utf-8') as f:
            f.write(user_info + '\n')
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print("请求或解析失败:", e)
        Email.send_email(subject="TikTok请求或解析失败", content=str(e))
        exit()


if __name__ == "__main__":
    tiktok()
    weibo()