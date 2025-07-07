import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json


user_id = ''  # 替换为你的用户ID
max_id = None
URL_RED = ""

HEADER_RED = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',  # 替换为你的User-Agent
    'Cookie': 'abRequestId=d73583d2-86f3-5e76-aa0a-6c61bd8330f6; a1=19319b5c06aem8zq1z7vao3nnc0jf0t6x6whei01250000374805; webId=101d894b99c69a3cd926c5ecf0cc2e64; gid=yjqyjD2fyWC2yjqyjD2S8K38K0d6YuAyuWh0EyJlqIIS8x28Vi89Kd888qW4Y82880Y802iD; web_session=040069b0c5241412b4ad3f7585354b0fe2f1a6; x-user-id-creator.xiaohongshu.com=61b1675c000000001000e4fb; customerClientId=478402480106079; acw_tc=0a00dcd917508604776493403e1c66c7b1862455b93c40ff234eaccc37dc16; websectiga=f47eda31ec99545da40c2f731f0630efd2b0959e1dd10d5fedac3dce0bd1e04d; sec_poison_id=725c5d71-312f-4ae1-a56f-d08134d364f6; webBuild=4.68.0; xsecappid=xhs-pc-web; loadts=1750860510515',
    'Referer': 'https://www.xiaohongshu.com/',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}


def get_red_user_info():
    try:
        response = requests.get(URL_RED, headers=HEADER_RED)
        soup = BeautifulSoup(response.text, 'html.parser')

        script = soup.find_all('script')[-1]

        state = str(script).replace('<script>', '').replace('</script>', '')
        state_with_script = state.replace('window.__INITIAL_STATE__=', '')
        state_with_script = state_with_script.replace('undefined', 'null')

        red_user_data = json.loads(state_with_script)

        basicInfo = red_user_data['user']['userPageData']['basicInfo']
        nickname = basicInfo['nickname'] # 用户昵称
        user_id = basicInfo['redId'] # 小红书号
        ip_location = basicInfo['ipLocation'] # IP位置
        description = basicInfo['desc']  # 用户简介

        interactions = red_user_data['user']['userPageData']['interactions']
        follows = 0
        fans = 0
        interaction = 0
        for item in interactions:
            if item['type'] == 'follows':
                follows = int(item['count'])
            elif item['type'] == 'fans':
                fans = int(item['count'])
            elif item['type'] == 'interaction':
                interaction = int(item['count'])

        user_info = {
            'nickname': nickname,
            'user_id': user_id,
            'ip_location': ip_location,
            'description': description,
            'follows': follows,
            'fans': fans,
            'interaction': interaction
        }
        return user_info
    except Exception as e:
        print(f"获取用户信息失败: {e}")

        return None


if __name__ == "__main__":
    user_info = get_red_user_info()
    print(f"用户昵称: {user_info['nickname']}")
    print(f"用户ID: {user_info['user_id']}")
    print(f"IP位置: {user_info['ip_location']}")
    print(f"用户简介: {user_info['description']}")
    print(f"关注数: {user_info['follows']}")
    print(f"粉丝数: {user_info['fans']}")
    print(f"互动数: {user_info['interaction']}")
