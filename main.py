import random
import requests
import json
import time
import module.Email as Email
import module.red as red
import module.weibo as weibo
import module.tiktok as tiktok
import module.database as database


FILE_PATH = ''  # this is the path where you want to save the file
FILE_TIKTOK_USER_INFO = 'tiktok_user_info.txt'
FILE_WEIBO_USER_INFO = 'weibo_user_info.txt'
FILE_RED_USER_INFO = 'red_user_info.txt'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
COOKIE_TIKTOK = "UIFID_TEMP=edf0d417f427c69b9e8dcf334ec311738f5d7ef487ab7a4043d6c18231e232a4109a12adc1c3f7f26fa2b018a1762357c2147030d2f37cbe71dd62a1f0efb64858788dc82aa484c683b2008a0f453159; hevc_supported=true; xgplayer_user_id=54110199621; fpk1=U2FsdGVkX1+39hdgmbDj6T8ShBekr3lUFPbfPTHsGrngj45fMR/tuRX2Xm26MogEWquBA4iMEZkhIQKSOR0XfA==; fpk2=d94a27a56e6a143d4c900b9014d6ba5d; bd_ticket_guard_client_web_domain=2; UIFID=edf0d417f427c69b9e8dcf334ec311738f5d7ef487ab7a4043d6c18231e232a4109a12adc1c3f7f26fa2b018a176235714142f663feeb21098188bf4013ef366563741f139de2078c9fe5c5a9e16e2b0c7d1fa1e6624a6be9bdcdcb270eaa660f92d81e5155ac350e039912a6ddffd03617a15174e734d88135a7a0ab96909e4333c0f699250832af144f04604d513c7b0a65888de3d30b6af5a78714ceff2af; SelfTabRedDotControl=%5B%5D; store-region=cn-ln; store-region-src=uid; live_use_vvc=%22false%22; xgplayer_device_id=40266552717; is_dash_user=1; my_rd=2; d_ticket=3bfbb5672b9a2898b27d109744e1514afd824; SearchMultiColumnLandingAbVer=1; SEARCH_RESULT_LIST_TYPE=%22multi%22; MONITOR_WEB_ID=c57da653-e729-4937-a49d-6db89a37363b; is_staff_user=false; __security_server_data_status=1; enter_pc_once=1; s_v_web_id=verify_mbs1oaak_WY03Wp9U_cfBg_4bEJ_Aei1_JI2G1u9OeiAN; passport_csrf_token=dfb743f832fed4744c92e6623cfde289; passport_csrf_token_default=dfb743f832fed4744c92e6623cfde289; FOLLOW_RED_POINT_INFO=%221%22; publish_badge_show_info=%221%2C0%2C0%2C1751181454017%22; vdg_s=1; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.598%7D; __security_mc_1_s_sdk_crypt_sdk=2d543bca-4665-80d9; __security_mc_1_s_sdk_cert_key=83e8e4e5-477c-b8c3; strategyABtestKey=%221751697589.445%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA8XJVc6CJRliPpOG1olveDrkTl1vY283zVMz8nu7uOuMBBiOGHT2_r28AdEu4Ygvb%2F1751731200000%2F0%2F1751697594864%2F0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __security_mc_1_s_sdk_sign_data_key_sso=53d2457d-430f-838e; passport_auth_status=b9ef960116749a197c6d4626e53b727b%2C; passport_auth_status_ss=b9ef960116749a197c6d4626e53b727b%2C; _bd_ticket_crypt_doamin=2; passport_assist_user=ClMOu1ed5MNni_AsI2aLPDUsKpeB--9Dosv1_8K8JgL5SUHBs78R5Bi2ehbzRAMyWeG7ybMGgvWDLcKfD_srAD8WpC92KXPzrFhlDsV5hnlHzP7VGBpKCjwAAAAAAAAAAAAATzIoDFr-VJI1MRDqXY55iD-mDoe2EfFgXAXySh25au3LL5j4DGj42pGheREPwO1BsZMQjPP1DRiJr9ZUIAEiAQPuEUQn; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; sid_guard=be785bd8249c09bdc322b74a569c4a75%7C1751698163%7C5184000%7CWed%2C+03-Sep-2025+06%3A49%3A23+GMT; uid_tt=1e43bfdfb936b336654e350afb0fdc5455431b477e10159be43efd5b7df21f47; uid_tt_ss=1e43bfdfb936b336654e350afb0fdc5455431b477e10159be43efd5b7df21f47; sid_tt=be785bd8249c09bdc322b74a569c4a75; sessionid=be785bd8249c09bdc322b74a569c4a75; sessionid_ss=be785bd8249c09bdc322b74a569c4a75; session_tlb_tag=sttt%7C14%7Cvnhb2CScCb3DIrdKVpxKdf_________UbqmpWGOdP60OBcSjtrqQ3c1cKmMmUZkwhh6b2ytSnNA%3D; sid_ucp_v1=1.0.0-KGY1ODQ5YjQ3NjQwMGFmMWFhMTRiYjk0NzVhMzY0MzQxYWQ0ZTZkOGIKIgi8iJSym4H8kGgQ85WjwwYY7zEgDDD85IfBBjgFQPsHSAQaAmxmIiBiZTc4NWJkODI0OWMwOWJkYzMyMmI3NGE1NjljNGE3NQ; ssid_ucp_v1=1.0.0-KGY1ODQ5YjQ3NjQwMGFmMWFhMTRiYjk0NzVhMzY0MzQxYWQ0ZTZkOGIKIgi8iJSym4H8kGgQ85WjwwYY7zEgDDD85IfBBjgFQPsHSAQaAmxmIiBiZTc4NWJkODI0OWMwOWJkYzMyMmI3NGE1NjljNGE3NQ; login_time=1751698150232; __security_mc_1_s_sdk_sign_data_key_web_protect=44b487bb-467c-9f49; _bd_ticket_crypt_cookie=c8a8bc1a91580a275b137eacf37d1516; ttwid=1%7CC4e-ctAMuvxO7ja29TcPNSp5XZENpRGti1rHvoHUfuM%7C1751698165%7C1ca45548102faf86b8dcd9dfbd58f728330e6bd5012c06d8dbeb3c0d52350672; WallpaperGuide=%7B%22showTime%22%3A1751698254932%2C%22closeTime%22%3A0%2C%22showCount%22%3A4%2C%22cursor1%22%3A59%2C%22cursor2%22%3A18%7D; __ac_nonce=06869358f00f77f919603; __ac_signature=_02B4Z6wo00f01yYG3UQAAIDAuGJ91N9dc28mJtnAAKHyGuavt0GwPdayjCit4CpIMy1F2mQjB98EzqU2S-tfQcOqDlWXAmDmjJfZFge0lg3aReYFhTKNm19KQ5NprhaLkqiRfGSUVnl9gc8z5f; dy_swidth=2560; dy_sheight=1440; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2560%2C%5C%22screen_height%5C%22%3A1440%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAyZkTH0g5o-M-mr26gp5tM_ScFLMaY3kPEgipGtKVFxTOSVAvCBKUrDQ4MCGOeQtY%2F1751731200000%2F0%2F0%2F1751726645303%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQjFWYkxlUHkzcVZVOW54ampjTEtuSE9QZStmaVg3dWR3N2p5OU9FOGhqY1I5ZlFvd3puVmVsVTd5aSt2YXVjaGxMT3J1cXVqbUljMWVKVndJaWhISnM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; odin_tt=82380b5b99a8f724064aed8d812cf69a189531d231d611ef85b3949f6c40ca2431ccbc89f82021da8f940cdac3f15e8c37893ee9467e86885d0d388e688f9fed; download_guide=%221%2F20250705%2F0%22; passport_fe_beating_status=false; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22"
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