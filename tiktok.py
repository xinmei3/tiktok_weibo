import requests
import json


URL_TIKTOK = "https://www.douyin.com/aweme/v1/web/user/profile/other/?device_platform=webapp&aid=6383&channel=channel_pc_web&publish_video_strategy_type=2&source=channel_pc_web&sec_user_id=MS4wLjABAAAAHpssvF9y7F9lx-CAY8EKmdMnUTHkcNiT6EKXgX3iXh0&personal_center_strategy=1&profile_other_record_enable=1&land_to=1&update_version_code=170400&pc_client_type=1&pc_libra_divert=Windows&support_h265=1&support_dash=1&cpu_core_num=12&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=136.0.0.0&browser_online=true&engine_name=Blink&engine_version=136.0.0.0&os_name=Windows&os_version=10&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7421552512153306650&uifid=edf0d417f427c69b9e8dcf334ec311738f5d7ef487ab7a4043d6c18231e232a4109a12adc1c3f7f26fa2b018a176235714142f663feeb21098188bf4013ef366563741f139de2078c9fe5c5a9e16e2b0c7d1fa1e6624a6be9bdcdcb270eaa660f92d81e5155ac350e039912a6ddffd03617a15174e734d88135a7a0ab96909e4333c0f699250832af144f04604d513c7b0a65888de3d30b6af5a78714ceff2af&msToken=wkPUW3u6KKDxYGuTb_OKFVNZf13yClKwJsDaxbQ4yWMmi80pVaotb-ZqM_Q21250NCrmP4QPps3_y3C-wn9ZREAw5F7eEL_cwcrNrC5alP3-AmN6vkAMsL5OBD2vGtOpQJ6soLKlN7-s4M7crs2bkP71MnQ1Yx5GTvHuEtQUnD0P3EiMCd_ebtE%3D&a_bogus=OJ4RhF7Edd%2FVcd%2FtYKjWHW2UWHDlNTWyZaTxRr3T7PY1G1Ma4mP5oaakroqOQ5o8ampTiKI7jVF%2FYEnc%2FGXiZFrpwmkDS%2FXbGsVCVUmo8qhpGPi23HfmCXUFqXsK85GNa559il7V8UrLZfx-wqQL%2FQVSeKYC5QShQZOyk%2FYCY9G6ZMLADpcaPBGpEXrn01cX&verifyFp=verify_m98o1t5a_8ntZgkr9_RCtL_4tqm_8c5s_zREsXpAbujws&fp=verify_m98o1t5a_8ntZgkr9_RCtL_4tqm_8c5s_zREsXpAbujws"


HEADERS_TIKTOK = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "Cookie": "UIFID_TEMP=edf0d417f427c69b9e8dcf334ec311738f5d7ef487ab7a4043d6c18231e232a4109a12adc1c3f7f26fa2b018a1762357c2147030d2f37cbe71dd62a1f0efb64858788dc82aa484c683b2008a0f453159; hevc_supported=true; bd_ticket_guard_client_web_domain=2; SelfTabRedDotControl=%5B%5D; store-region=cn-ln; store-region-src=uid; live_use_vvc=%22false%22; is_dash_user=1; my_rd=2; d_ticket=3bfbb5672b9a2898b27d109744e1514afd824; SearchMultiColumnLandingAbVer=1; SEARCH_RESULT_LIST_TYPE=%22multi%22; __security_mc_1_s_sdk_crypt_sdk=14cc0c37-43ba-a2c7; __security_mc_1_s_sdk_cert_key=69b62ff1-4b0a-a83e; is_staff_user=false; __security_mc_1_s_sdk_sign_data_key_sso=d6634e8b-46f0-8b05; __security_server_data_status=1; passport_assist_user=CkFQx2TVKZ_uPHzDZIbhIs90W7txZYFvCfy16wXcsEJS64-vtaU8DeOrRHLh6MN6n53PXNs1WgazgCLgoWIoFU5_VBpKCjwAAAAAAAAAAAAATw_FJCDAi4DHYZxSbL3I--d3CFjmmbFxtIOgoEOPI2QGMruOEsY_oarZACsXhCrPVGAQ2uryDRiJr9ZUIAEiAQP8UACl; n_mh=AGonqdN1QWefaf74AVcq8KIvk_eTXDcyv2DrZj72Ufs; sid_guard=aa33e97055391bdbd68d205d436ef382%7C1748678706%7C5184000%7CWed%2C+30-Jul-2025+08%3A05%3A06+GMT; uid_tt=3126e9573b4781d37a88d40399e8bbf5; uid_tt_ss=3126e9573b4781d37a88d40399e8bbf5; sid_tt=aa33e97055391bdbd68d205d436ef382; sessionid=aa33e97055391bdbd68d205d436ef382; sessionid_ss=aa33e97055391bdbd68d205d436ef382; sid_ucp_v1=1.0.0-KGEzZjMzNTljMzEwYjc3NGMxOTZkYjJkYzk5ODM1MmFjNjc3MzgwNzgKIQiJjaHHns2iAxCy8OrBBhjvMSAMMMic-qwGOAVA-wdIBBoCbGYiIGFhMzNlOTcwNTUzOTFiZGJkNjhkMjA1ZDQzNmVmMzgy; ssid_ucp_v1=1.0.0-KGEzZjMzNTljMzEwYjc3NGMxOTZkYjJkYzk5ODM1MmFjNjc3MzgwNzgKIQiJjaHHns2iAxCy8OrBBhjvMSAMMMic-qwGOAVA-wdIBBoCbGYiIGFhMzNlOTcwNTUzOTFiZGJkNjhkMjA1ZDQzNmVmMzgy; login_time=1748678707055; __security_mc_1_s_sdk_sign_data_key_web_protect=edc31327-4d47-94ee; _bd_ticket_crypt_cookie=9eacb644f047557bd4ce09702da2eb78; download_guide=%223%2F20250606%2F0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.379%7D; enter_pc_once=1; passport_csrf_token=dfb743f832fed4744c92e6623cfde289; passport_csrf_token_default=dfb743f832fed4744c92e6623cfde289; publish_badge_show_info=%220%2C0%2C0%2C1749652086788%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2560%2C%5C%22screen_height%5C%22%3A1440%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; strategyABtestKey=%221749742718.89%22; biz_trace_id=3be6c708; ttwid=1%7CC4e-ctAMuvxO7ja29TcPNSp5XZENpRGti1rHvoHUfuM%7C1749742717%7Cbd90c47458f18666b76f47f8e5e3acfa95f48f2170d4518f8747052550d4831e; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA8XJVc6CJRliPpOG1olveDrkTl1vY283zVMz8nu7uOuMBBiOGHT2_r28AdEu4Ygvb%2F1749744000000%2F0%2F0%2F1749743936484%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA8XJVc6CJRliPpOG1olveDrkTl1vY283zVMz8nu7uOuMBBiOGHT2_r28AdEu4Ygvb%2F1749744000000%2F0%2F1749743336485%2F0%22; odin_tt=6ad1916014d7cf0986bfbb062a15ba4b120a4e979eeb910816f96139945917b7c480bb7cae7e1fcf13472831c617991573cd037802a943181ab2bcdb75505116; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCQjFWYkxlUHkzcVZVOW54ampjTEtuSE9QZStmaVg3dWR3N2p5OU9FOGhqY1I5ZlFvd3puVmVsVTd5aSt2YXVjaGxMT3J1cXVqbUljMWVKVndJaWhISnM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "Referer" : "https://www.douyin.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive"
}

def get_tiktok_user_info():
    try:
        response = requests.get(URL_TIKTOK, headers=HEADERS_TIKTOK, timeout=10)
        response_json = json.loads(response.text)

        tiktok_user_info = response_json["user"]
        nickname =         tiktok_user_info["nickname"]          # 昵称
        unique_id =        tiktok_user_info["unique_id"]         # 抖音号
        follower_count =   tiktok_user_info["follower_count"]    # 粉丝数
        following_count =  tiktok_user_info["following_count"]   # 关注数
        total_favorited =  tiktok_user_info["total_favorited"]   # 获赞数
        aweme_count =      tiktok_user_info["aweme_count"]       # 作品数
        favoriting_count = tiktok_user_info["favoriting_count"]  # 喜欢作品数
        signature =        tiktok_user_info["signature"]         # 签名

        user_info = {
            'nickname': nickname,
            'unique_id': unique_id,
            'follower_count': follower_count,
            'following_count': following_count,
            'total_favorited': total_favorited,
            'aweme_count': aweme_count,
            'favoriting_count': favoriting_count,
            'signature': signature
        }
        print(user_info)
        return user_info

    except Exception as e:
        print(f"获取用户信息失败: {e}")
        return None
    

if __name__ == "__main__":
    user_info = get_tiktok_user_info()
    print("昵称:", user_info['nickname'])
    print("抖音号:", user_info['unique_id'])
    print("粉丝数:", user_info['follower_count'])
    print("关注数:", user_info['following_count'])
    print("获赞数:", user_info['total_favorited'])
    print("作品数:", user_info['aweme_count'])
    print("喜欢作品数:", user_info['favoriting_count'])
    print("签名:", user_info['signature'])