import requests


def custom_get(url, params=None, headers=None):
    """
    封装 requests 包的 GET 方法，添加了异常处理
    :param url: 请求的 URL
    :param params: 请求的参数 (可选)
    :param headers: 请求的头部信息 (可选)
    :return: 如果请求成功，返回响应对象；否则返回 None
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查响应状态，如果不是 200，会抛出异常
        return response
    except requests.exceptions.RequestException as e:
        print("请求失败:", e)
        return None


def check_version(domain: str):
    url_http = "http://"+domain+"/version"
    url_https = "https://"+domain+"/version"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res_http = custom_get(url_http, headers=headers)
        if "appversion: ssplib0.0.4" not in str(res_http.content):
            print("check erro:domain:", url_http)
            return
        res_https = custom_get(url_https, headers=headers)
        if "appversion: ssplib0.0.4" not in str(res_https.content):
            print("check erro:domain:", url_https)
            return
    except Exception as e:
        print("erro:domain:", domain, "erro:", e)
        return

    print("check success:", domain)


def check_http_https(domain: str, path: str, expect_resp: str):
    urls = ["http://" + domain + path, "https://" + domain + path]
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        for url in urls:
            res = custom_get(url, headers=headers)
            if res.status_code != 200:
                print("check erro:domain:", url)
                return
            if expect_resp not in str(res.content):
                print("check erro:domain:", url)
                return
    except Exception as e:
        print("check erro:domain:", domain, "erro:", e)
        return
    print("check success:", domain)


def check_bid(domain):
    path = "/bid"
    expect_resp = '{"status":-1301,"msg":"EXCEPTION_APP_ID_EMPTY"}'
    check_http_https(domain, path, expect_resp)


def check_v3path(domain):
    path = "/openapi/ad/v3"
    expect_resp = '{"status":-1301,"msg":"EXCEPTION_APP_ID_EMPTY"}'
    check_http_https(domain, path, expect_resp)


def check_load(domain):
    path = "/load"
    expect_resp = '{"status":204,"msg":"load no ad"}'
    check_http_https(domain, path, expect_resp)


def check_feedback(domain_list):
    for domain in domain_list:
        path = "/win"
        expect_resp = ""
        check_http_https(domain, path, expect_resp)


def check_supply_tracking(domain_list):
    for domain in domain_list:
        path = "/billing"
        expect_resp = ""
        check_http_https(domain, path, expect_resp)


def check_adx(domain_list):
    for domain in domain_list:
        path = "/version"
        expect_resp = "appversion:"
        check_http_https(domain, path, expect_resp)


if __name__ == '__main__':
    feedback = [
        "sg-gcp-adx-asia-southeast1-a-bid-feedback.mintegral.net",
        "sg-gcp-adx-asia-southeast1-a-bid-feedback.rayjump.com",
        "sg-gcp-adx-asia-southeast1-a-bid-feedback.mtgglobals.com",
        "sg-gcp-adx-asia-southeast1-b-bid-feedback.mintegral.net",
        "sg-gcp-adx-asia-southeast1-b-bid-feedback.rayjump.com",
        "sg-gcp-adx-asia-southeast1-b-bid-feedback.mtgglobals.com",
    ]
    check_feedback(feedback)
    supply = [
        "sg-gcp-adx-asia-southeast1-a-ssp-tk.mintegral.net",
        "sg-gcp-adx-asia-southeast1-a-ssp-tk.rayjump.com",
        "sg-gcp-adx-asia-southeast1-a-ssp-tk.mtgglobals.com",
        "sg-gcp-adx-asia-southeast1-b-ssp-tk.mintegral.net",
        "sg-gcp-adx-asia-southeast1-b-ssp-tk.rayjump.com",
        "sg-gcp-adx-asia-southeast1-b-ssp-tk.mtgglobals.com",
    ]
    check_supply_tracking(supply)
    adx = [
        "sg-gcp-madx-adx.mobvista.com"
    ]
    check_adx(adx)
    # bid_domain = [
    #     "sg-new-cdn-ssplib-ap-southeast-1a-hb.mtgglobals.com",
    #     "sg-new-cdn-ssplib-ap-southeast-1b-hb.mtgglobals.com",
    #     "sg-new-cdn-ssplib-ap-southeast-1c-hb.mtgglobals.com",
    #     "sg-new-cdn-ssplib-ap-southeast-1a-hb.rayjump.com",
    #     "sg-new-cdn-ssplib-ap-southeast-1b-hb.rayjump.com",
    #     "sg-new-cdn-ssplib-ap-southeast-1c-hb.rayjump.com",
    #     "sg-new-ssplib-ap-southeast-1a-hb.mintegral.net",
    #     "sg-new-ssplib-ap-southeast-1b-hb.mintegral.net",
    #     "sg-new-ssplib-ap-southeast-1c-hb.mintegral.net",
    # ]
    # for b in bid_domain:
    #     check_load(b)
    #
    # v3_domain = [
    #     "bj-ali-ssplib-sdk-wf.rayjump.com",
    #     "vg-ali-ssplib-sdk-wf.rayjump.com",
    #     "nl-gcp-ssplib-sdk-wf.rayjump.com",
    #     "sg-gcp-ssplib-sdk-wf.rayjump.com",
    #     "vg-aws-ssplib-sdk-wf.rayjump.com",
    #     "vg-ali-ssplib-sdk-wf.mtgglobals.com",
    #     "nl-gcp-ssplib-sdk-wf.mtgglobals.com",
    #     "sg-gcp-ssplib-sdk-wf.mtgglobals.com",
    #     "vg-aws-ssplib-sdk-wf.mtgglobals.com",
    #     "bj-ali-ssplib-sdk-wf.mintegral.net",
    #     "vg-ali-ssplib-sdk-wf.mintegral.net",
    #     "nl-gcp-ssplib-sdk-wf.mintegral.net",
    #     "sg-gcp-ssplib-sdk-wf.mintegral.net",
    #     "vg-aws-ssplib-sdk-wf.mintegral.net"
    # ]
    # for v in v3_domain:
    #     check_v3path(v)
    # domain_list = [
    #     "vg-aws-cdn-ssplib-us-east-1a-hb.mtgglobals.com",
    #     "vg-aws-cdn-ssplib-us-east-1b-hb.mtgglobals.com",
    #     "vg-aws-cdn-ssplib-us-east-1a-hb.rayjump.com",
    #     "vg-aws-cdn-ssplib-us-east-1b-hb.rayjump.com",
    #     "vg-aws-ssplib-us-east-1a-hb.mintegral.net",
    #     "vg-aws-ssplib-us-east-1b-hb.mintegral.net",
    #     "vg-aws-ssplib-us-east-1a-hb.mtgglobals.com",
    #     "vg-aws-ssplib-us-east-1b-hb.mtgglobals.com",
    #     "vg-new-ssplib-hb.mtgglobals.com",
    #     "vg-new-ssplib-hb.rayjump.com",
    #     "vg-new-ssplib-hb.mintegral.net",
    #     "sg-new-cdn-ssplib-asia-southeast1-c-hb.mtgglobals.com",
    #     "sg-new-cdn-ssplib-asia-southeast1-b-hb.mtgglobals.com",
    #     "sg-new-cdn-ssplib-asia-southeast1-c-hb.rayjump.com",
    #     "sg-new-cdn-ssplib-asia-southeast1-b-hb.rayjump.com",
    #     "sg-new-cdn-ssplib-asia-southeast1-c-hb.mintegral.net",
    #     "sg-new-cdn-ssplib-asia-southeast1-b-hb.mintegral.net",
    #     "sg-new-ssplib-asia-southeast1-c-hb.mintegral.net",
    #     "sg-new-ssplib-asia-southeast1-b-hb.mintegral.net",
    #     "nl-new-cdn-ssplib-europe-west4-c-hb.rayjump.com",
    #     "nl-new-cdn-ssplib-europe-west4-b-hb.rayjump.com",
    #     "nl-new-cdn-ssplib-europe-west4-c-hb.mtgglobals.com",
    #     "nl-new-cdn-ssplib-europe-west4-b-hb.mtgglobals.com",
    #     "nl-new-cdn-ssplib-europe-west4-c-hb.mintegral.net",
    #     "nl-new-cdn-ssplib-europe-west4-b-hb.mintegral.net",
    #     "nl-new-ssplib-europe-west4-b-hb.mintegral.net",
    #     "nl-new-ssplib-europe-west4-c-hb.mintegral.net",
    #     "bj-new-ssplib-hb.mintegral.net",
    #     "bj-new-ssplib-hb.rayjump.com",
    # ]
    # for d in domain_list:
    #     check_version(d)


