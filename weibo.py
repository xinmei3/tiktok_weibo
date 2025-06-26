import random
import requests
import json
import time
from database import DataBase
import Email

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
COOKIE_WEIBO = ""  # this is weibo cookie, you can get it from browser devtools

HEADERS_WEIBO = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE_WEIBO,
    "Referer": "https://weibo.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive"
}

URL_WEIBO_HOME = "https://weibo.com/ajax/profile/info?uid="


def weibo():
    try:
        time.sleep(random.randint(10, 20))  # 随机等待10到20秒
        response = requests.get(URL_WEIBO_HOME, headers=HEADERS_WEIBO)
        response_json = json.loads(response.text)

        weibo_info_xiang = response_json['data']['user']
        likes_received_all = weibo_info_xiang["status_total_counter"]["total_cnt_format"]
        comments_received = int(weibo_info_xiang["status_total_counter"]["comment_cnt"])
        likes_received = int(weibo_info_xiang["status_total_counter"]["like_cnt"])
        followers_count = weibo_info_xiang["followers_count"]
        friends_count = weibo_info_xiang["friends_count"]
        statuses_count = weibo_info_xiang["statuses_count"]
        
        user_info = {
            "likes_received_all": likes_received_all,  # 总获赞数
            "comments_received": comments_received,    # 评论量
            "likes_received": likes_received,          # 获赞数
            "followers_count": followers_count,        # 粉丝数
            "friends_count": friends_count,            # 关注数
            "statuses_count": statuses_count,          # 微博数
        }
        return user_info
    except Exception as e:
        print(f"获取用户信息失败: {e}")

        return None


if __name__ == "__main__":
    user_info = weibo()
    if user_info:
        print("微博用户信息获取成功:")
        print(user_info)
    else:
        print("微博用户信息获取失败")
