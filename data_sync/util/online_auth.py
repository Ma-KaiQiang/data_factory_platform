import json
import requests
import re
# from django_redis import get_redis_connection as client
from data_sync.util.redis_handle import RedisHandle


def login():
    data = {
        'username': 'makaiqiang',
        'password': '1q2w3e4r5t!'
    }
    res = requests.post(url='https://wos.mabangerp.com/authenticate/', data=data, headers={
        'Cookie': '__bid_n=184984426188f4f0e54207; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221849844268025f-02f76a14ab7589-26021e51-921600-18498442682475%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221849844268025f-02f76a14ab7589-26021e51-921600-18498442682475%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfYW5vbnltb3VzX2lkIjoiMTg0OTg0NDI2ODAyNWYtMDJmNzZhMTRhYjc1ODktMjYwMjFlNTEtOTIxNjAwLTE4NDk4NDQyNjgyNDc1IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4NGViNjczZTAyYzUtMGYzYmRmYjE1NmJjZWQ4LTI2MDIxZTUxLTIwNzM2MDAtMTg0ZWI2NzNlMDM0ZjkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; gr_user_id=d8a536f5-5a0e-4fe2-accf-eaafd898759e; Hm_lvt_b888e3a9116ee926400397d5e2c3792b=1680831772,1680839229,1680839264,1680839310; csrftoken=HaVMCJghax1j3TgLeSSYMSbxaUsRl0wDhc0JsM95ZX7Hj4qSjBshVQw7s6qYmQKa; Hm_lpvt_b888e3a9116ee926400397d5e2c3792b=1680857189; CRAWL_KANDENG_KEY=yZaUCj0x80W%2FPQWYZNOX7O7%2Bg5Aj68KQM5ayIutncO9XRNpPafYmhX5vChkbGu75koFGubH9SGkU8fkr0xkt4w%3D%3D',
        'X-CSRFToken': 'HaVMCJghax1j3TgLeSSYMSbxaUsRl0wDhc0JsM95ZX7Hj4qSjBshVQw7s6qYmQKa'
    })
    set_cookie = res.headers.get('set-Cookie')
    csrftoken = re.search('\w{64}', set_cookie)[0]
    session_id = re.findall('\w{32}', set_cookie)[2]
    # Authorization.objects.update_or_create(id=0, defaults={'id': 0, 'sessionId': session_id, 'csrfToken': csrftoken})
    return csrftoken, session_id


def headers():
    c, s = login()
    headers = {
        'Cookie': f'__bid_n=184984426188f4f0e54207; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221849844268025f-02f76a14ab7589-26021e51-921600-18498442682475%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221849844268025f-02f76a14ab7589-26021e51-921600-18498442682475%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfYW5vbnltb3VzX2lkIjoiMTg0OTg0NDI2ODAyNWYtMDJmNzZhMTRhYjc1ODktMjYwMjFlNTEtOTIxNjAwLTE4NDk4NDQyNjgyNDc1IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4NGViNjczZTAyYzUtMGYzYmRmYjE1NmJjZWQ4LTI2MDIxZTUxLTIwNzM2MDAtMTg0ZWI2NzNlMDM0ZjkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; MULTI_LANGUAGE_TYPE=%2BYjZ6oacL7xJ%2FKOcmBg9Z7cTOqi7UgOUgujRs4KQ4Ms%3D; gr_user_id=d8a536f5-5a0e-4fe2-accf-eaafd898759e; Hm_lvt_b888e3a9116ee926400397d5e2c3792b=1680831772,1680839229,1680839264,1680839310; Hm_lpvt_b888e3a9116ee926400397d5e2c3792b=1680857189; CRAWL_KANDENG_KEY=yZaUCj0x80W%2FPQWYZNOX7O7%2Bg5Aj68KQM5ayIutncO9XRNpPafYmhX5vChkbGu75koFGubH9SGkU8fkr0xkt4w%3D%3D; csrftoken={c}; sessionid={s}',
        'X-CSRFToken': c
    }
    client = RedisHandle().client
    client.hset('authorization', 'headers', json.dumps(headers))
    print(client.hget('authorization', 'headers'))


if __name__ == '__main__':
    headers()
