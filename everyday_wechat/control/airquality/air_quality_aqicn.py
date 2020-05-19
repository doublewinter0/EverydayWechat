# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-09-30 17:58
Introduction: 获取空气质量
官网：http://aqicn.org/here/

"""

import requests
import json

# token，申请地址：http://aqicn.org/data-platform/token/#/
AQICN_TOKEN = 'ba06296716d308e8cff6da4351c45dba0244d063'

AIR_STATUS_DICT = {
    50: '优',
    100: '良',
    150: '轻度污染',
    200: '中度污染',
    300: '重度污染',
    3000: '严重污染'
}


def get_air_quality(city):
    """
    通过城市名获取空气质量
    官网：http://aqicn.org/here/
    token 申请地址：http://aqicn.org/data-platform/token/#/
    :param city: 城市
    :return:
    """

    if not city or not city.strip():
        return
    print('获取 {} 的空气质量...'.format(city))
    city_id = __get_city_id__(city[0:2])
    if not city:
        return None
    try:
        url = f'http://api.waqi.info/feed/@{city_id}/?token={AQICN_TOKEN}'
        resp = requests.get(url)
        if resp.status_code == 200:
            # print(resp.text)
            content_dict = resp.json()
            if content_dict.get('status') == 'ok':
                data_dict = content_dict['data']
                aqi = data_dict['aqi']
                air_status = '严重污染'
                for key in sorted(AIR_STATUS_DICT):
                    if key >= aqi:
                        air_status = AIR_STATUS_DICT[key]
                        break
                aqi_info = '{city} PM2.5：{aqi} {air_status}'.format(city=city, aqi=aqi, air_status=air_status)
                # print(aqi_info)
                return aqi_info
            else:
                print('获取空气质量失败:{}'.format(content_dict['data']))
                return None
        print('获取空气质量失败。')
    except Exception as exception:
        print(str(exception))
    return None


def __get_city_id__(city_keyword):
    url = f'https://api.waqi.info/search/?token={AQICN_TOKEN}&keyword={city_keyword}'
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return json.loads(resp.content)["data"][0]["uid"]
    except Exception as exp:
        print(str(exp))
        return None


if __name__ == '__main__':
    city = '长沙'
    dd = get_air_quality(city)
    print(dd)

    __get_city_id__("神木")

