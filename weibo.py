import random
import requests
import json
import time
from database import DataBase
import Email


db = DataBase()

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
        use_info_db = db.search_weibo()
        # print(user_info_tuple[:-1], use_info_db[1:-1])
        if user_info_tuple[:-1] == use_info_db[1:-1]:
            print("weibo数据未变化，跳过写入")
        else:
            db.insert_weibo(user_info_tuple)
            print("weibo数据已更新，写入数据库", user_info_tuple)
            Email.send_email(subject="微博用户信息更新", content=user_info)

        with open('weibo_user_info.txt', 'a', encoding='utf-8') as f:
            f.write(user_info + '\n')
    except (requests.RequestException, json.JSONDecodeError) as e:
        print("请求或解析失败:", e)
        Email.send_email(subject="微博请求或解析失败", content=str(e))
        exit()
