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

URL_TIKTOK = ""  # this is tiktok user info api, you can get it from browser devtools
# Example: "https://www.douyin.com/web/api/v2/user/info/?user

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