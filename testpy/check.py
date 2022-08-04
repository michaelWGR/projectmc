import requests
import json
import time
import argparse
requests.packages.urllib3.disable_warnings()
starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())-3600))
endtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def maidian(uid, cv="lovemeet", start_time=starttime, end_time=endtime, name="lovemeet_basic_heartbeat"):
    url = "https://etms.busi.inkept.cn/v1/etms/query"
    headers = {
        "Connection": "keep - alive",
    }
    params = {"uid": uid,
              "pageNo": 1,
              "pageNum": 10,
              "appid": 260032,
              "str": name,
              "start_time": start_time,
              "end_time": end_time
              }
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    try:
        rp_dict = json.loads(response.content)
        str_dict = json.loads(rp_dict['data']['list'][0]['str'])
    except Exception as e:
        print('error msg: {}'.format(e))
        return

    # 获取校验字段
    m_uid = str_dict['uid']
    md_userid = str_dict['md_userid']
    smid = str_dict['smid']
    md_mod = str_dict['md_mod']
    cvInfo = str_dict['cv']
    cc = str_dict['cc']
    md_eid = str_dict['md_eid']
    try:
        oaid = str_dict['oaid']
    except KeyError as e:
        oaid = ""
    try:
        imei = str_dict['imei']
    except KeyError as e:
        imei = ""

    is_true = {}
    is_true['m_uid'] = m_uid == str(uid)
    is_true['md_userid'] = md_userid == str(uid)
    is_true['smid'] = smid != ""
    is_true['md_mod'] = md_mod == "1"
    is_true['cv'] = cv in cvInfo.lower()
    is_true['cc'] = cc != ""
    is_true['imei_oaid'] = (imei != "" or oaid != "")
    is_true['md_eid'] = md_eid == str(name)

    ispass = True
    fail_params = []
    for _ in is_true:
        if not is_true[_]:
            ispass = False
            fail_params.append(_)

    params_ft = "\n搜索埋点前缀: {0[0]} \nmd_userid: {0[1]} \nsmid: {0[2]} " \
                "\nme_mod: {0[3]} \ncv: {0[4]} \ncc: {0[5]} \nimei: {0[6]} " \
                "\noaid: {0[7]} \nmd_eid: {0[8]} \nuid: {0[9]}\n"
    params = name, md_userid, smid, md_mod, cvInfo, cc, imei, oaid, md_eid, m_uid
    params_str = params_ft.format(params)

    if ispass:
        params_str = params_str + "校验通过\n"
        print(params_str)
    else:
        params_str = params_str + "校验失败,请检查以下参数\n" + ",".join(fail_params)
        print(params_str)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--uid", required=True, help="输入uid")
    parser.add_argument('-c', "--cv", default="lovemeet", help="输入cv，默认为lovemeet")
    parser.add_argument("-d", "--duration", default=10, type=int, help="请输入查询的时间间隔，单位min，默认为10min")
    args = parser.parse_args()
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())-args.duration*60))
    maidian(args.uid, args.cv, starttime, name="lovemeet_basic_heartbeat")
    maidian(args.uid, args.cv, starttime, name="lovemeet_app_heartbeat")


if __name__ == '__main__':
    main()
    # maidian('2185963', name="lovemeet_basic_heartbeat")
    # maidian('2185963', name="lovemeet_app_heartbeat")

