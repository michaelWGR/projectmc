#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, session, redirect
import json

app = Flask(__name__)


@app.route('/post/send', methods=['POST', 'GET'])
def adx_creative_post():
    # 改这个即可
    return_json = {
        "status": 0,
        "msg": "",
        "id": "fbc7e7db4b6ca149df78df1929a5333f"
    }
    return json.dumps(return_json)


@app.route('/post/sync', methods=['POST', 'GET'])
def adx_creative_post_sync():
    # 改这个即可
    return_json = {
        "status": 0,
        "msg": "",
        "data":
        {
            "status": 1,
            "update_time": "2022-04-19 12:00:00",
            "remark": "",
            "end_time": "2022-06-18",
            "transcode_list":
            [
                {
                    "width": 480,
                    "height": 270,
                    "size": 103.026,
                    "platform": "DEFAULT",
                    "url": "http://image.res.hunantv.com/mediafiles/wiad_creative/27/15130700418269.jpg"
                }
            ]
        }
    }
    return json.dumps(return_json)


@app.route('/get', methods=['GET'])
def adx_creative_get():
    return_json = {
        "state": "abnormal"
    }
    return json.dumps(return_json)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8081)
    # a = {'1': [1,2,3], '2': [2,4,6]}
    # for v in a.values():
    #     for i in v:
    #         print(i)
        # print(v)