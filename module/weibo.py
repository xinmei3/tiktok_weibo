import json
import requests
from pprint import pprint


REFERER_WEIBO = "https://weibo.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
CONNECTION_KEEP_ALIVE = "keep-alive"

HEADERS_WEIBO = {
    "User-Agent": USER_AGENT,
    "Cookie": "SINAGLOBAL=5172920912928.578.1727964718316; XSRF-TOKEN=CXWIsRLWyXTPlRSJRqWCRCwL; _s_tentry=weibo.com; Apache=5392044330354.525.1751900668418; ULV=1751900668471:60:4:1:5392044330354.525.1751900668418:1751697578435; WBPSESS=CtdwwwCyKWEc2EnGhvgdz08FSQGbJtHve5paM47jkDgYO1BS7ihKbRXsJFBLAyPc37-IJ9ospXhFNwS6Y6TjGA9B51Lx9aGvQZAufuM7jvMTS2FXj558hczGbQLCcA7bPVfpj7udtI9tkiu8phcS2Q==; PC_TOKEN=770f04c11b; ALF=1754493293; SUB=_2A25Fb5Q9DeRhGeVP7FMW8i3Pzj6IHXVmBKn1rDV8PUJbkNANLUntkW1NTPTpcwJUAid-Jz2YBzGWqmy2DFb59cUN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4VRKkCD0umBECsWzgziLV5JpX5KMhUgL.FoepS02Neoe0SKz2dJLoIpfki--fiKnNiKL2i--Ni-2Ei-2Ni--ci-zpi-27P7tt",
    "Referer": REFERER_WEIBO,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": CONNECTION_KEEP_ALIVE
}

USER_ID = "1669879400"
URL_WEIBO_HOME = "https://weibo.com/ajax/profile/info?uid=1669879400"

class getWeiboInfo:
    def __init__(self):
        self.url = URL_WEIBO_HOME
        self.headers = HEADERS_WEIBO
        self.followers_count = None
        self.friends_count = None
    
    def get_fans_data(self, user_id):
        url = "https://weibo.com/ajax/friendships/friends?relate=fans&page={}&uid={}&type=all&newFollowerCount=0"
        user_id = USER_ID
        response = requests.get(url.format(1, user_id), headers=HEADERS_WEIBO)
        response_json = json.loads(response.text)
        fans_info = response_json['users']            # 获取第一页的粉丝列表
        fans_count = response_json['total_number']    # 获取总粉丝数
        for num in range(2, (fans_count // 20) + 2):
            response = requests.get(url.format(num, user_id), headers=HEADERS_WEIBO)
            response_json = json.loads(response.text)
            fans_info.extend(response_json['users'])

        return fans_info, fans_count

    def get_follower_data(self, user_id):
        url = "https://weibo.com/ajax/friendships/friends?page={}&uid={}"
        user_id = USER_ID
        response = requests.get(url.format(1, user_id), headers=HEADERS_WEIBO)
        response_json = json.loads(response.text)
        followers_info = response_json['users']            # 获取第一页的关注列表
        followers_count = response_json['total_number']    # 获取总关注数
        for num in range(2, (followers_count // 20) + 2):
            response = requests.get(url.format(num, user_id), headers=HEADERS_WEIBO)
            response_json = json.loads(response.text)
            followers_info.extend(response_json['users'])

        return followers_info, followers_count

    def get_weibo_user_info(self):
        response = requests.get(URL_WEIBO_HOME, headers=HEADERS_WEIBO)
        if response.status_code != 200:
            print(f"获取用户信息失败，状态码: {response.status_code}")
            return None
        if not response.text:
            print("获取用户信息失败，响应内容为空")
            return None

        try:
            response_json = json.loads(response.text)
        except json.JSONDecodeError:
            print("获取用户信息失败，JSON解析错误")
            return None

        weibo_info_xiang = response_json['data']['user']
        nickname = weibo_info_xiang["screen_name"]                                             # 昵称
        signature = weibo_info_xiang["description"]                                            # 简介
        likes_received_all = weibo_info_xiang["status_total_counter"]["total_cnt_format"]      # 转评赞
        comments_received = weibo_info_xiang["status_total_counter"]["comment_cnt"]       # 累计评论量
        likes_received = weibo_info_xiang["status_total_counter"]["like_cnt"]             # 累计获赞
        followers_count = weibo_info_xiang["followers_count"]                                  # 粉丝
        friends_count = weibo_info_xiang["friends_count"]                                      # 关注
        statuses_count = weibo_info_xiang["statuses_count"]                                    # 微博数

        user_info = {
            "昵称"       : nickname,
            "简介"       : signature,
            "转评赞"     : likes_received_all,
            "累计评论量" : comments_received,
            "累计获赞"   : likes_received,
            "粉丝数"     : followers_count,
            "关注数"     : friends_count,
            "微博数"     : statuses_count
        }
        return user_info


if __name__ == "__main__":
    weibo_info = getWeiboInfo()
    user_info = weibo_info.get_weibo_user_info()
    follower_data, followers_count = weibo_info.get_follower_data(USER_ID)
    # fans_data, followers_count = weibo_info.get_fans_data(USER_ID)
    if user_info:
        print(f"昵称: {user_info['昵称']}")
        print(f"简介: {user_info['简介']}")
        print(f"总获赞数: {user_info['转评赞']}")
        print(f"评论量: {user_info['累计评论量']}")
        print(f"获赞数: {user_info['累计获赞']}")
        print(f"粉丝数: {user_info['粉丝数']}")
        print(f"关注数: {user_info['关注数']}")
        print(f"微博数: {user_info['微博数']}")
    else:
        print("未能获取用户信息")
    # with open('weibo_user_follower_info.json', 'w', encoding='utf-8') as f:
    #     json.dump(follower_data, f, ensure_ascii=False, indent=4)
    for idx, item in enumerate(follower_data):
        print(f"{idx}, 昵称: {item['screen_name']}, \t主页链接: https://weibo.com/u/{item['id']}, 关注数: {item['followers_count']}, 粉丝数: {item['friends_count']}")
