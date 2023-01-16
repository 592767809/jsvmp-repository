# -*- coding: utf-8 -*-
import json
import re
import execjs
import requests

from loguru import logger

with open("./eval_init_list.js", "r", encoding="utf-8")as f:
    ctx = execjs.compile(f.read())


def get_final_list(_list):
    result_array = []
    _index = 0
    _add = 0
    while len(result_array) < 64:
        if _index < 8:
            result_array.append(_list[(7 - _index) * 8 + _add])
            _index += 1
        else:
            _index = 0
            _add += 1
    return result_array


def final_list_offset(_list):
    result = ""
    for i in range(64):
        result += chr(_list[i])
    return result


def get_websectiga(res_dict):
    logger.info(f"b_d --> {res_dict}")
    init_list = ctx.call("Nami", res_dict)
    logger.info(f"init_list --> {init_list}")
    final_list = get_final_list(init_list)
    result = final_list_offset(final_list)
    logger.info(f"result --> {result}")
    return result


def get_res_dict():
    url = "https://www.xiaohongshu.com/api/sec/v1/scripting"
    data = {
        "callFrom": "web",
        "callback": "seccallback"
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    res = requests.post(url, headers=headers, json=data)
    return json.loads(re.search("\(\)\(window,(.*?)\);}\)\(\);", res.json().get("data")['data']).group(1))


if __name__ == '__main__':
    res_dict = get_res_dict()
    get_websectiga(res_dict)
