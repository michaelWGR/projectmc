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
        # response.raise_for_status()  # 检查响应状态，如果不是 200，会抛出异常
        return response
    except requests.exceptions.RequestException as e:
        print("请求失败:", e)
        return None


# def check_version(domain: str):
#     url_http = "http://"+domain+"/version"
#     url_https = "https://"+domain+"/version"
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     try:
#         res_http = custom_get(url_http, headers=headers)
#         if "appversion: ssplib0.0.4" not in str(res_http.content):
#             print("check erro:domain:", url_http)
#             return
#         res_https = custom_get(url_https, headers=headers)
#         if "appversion: ssplib0.0.4" not in str(res_https.content):
#             print("check erro:domain:", url_https)
#             return
#     except Exception as e:
#         print("erro:domain:", domain, "erro:", e)
#         return
#
#     print("check success:", domain)


def check_http_https(domain: str, path: str, expect_resp: str, expect_code=200, prefix=None):
    if prefix is None:
        prefix = ["http", "https"]
    urls = []
    for pf in prefix:
        if pf == "http":
            urls.append("http://" + domain + path)
        elif pf == "https":
            urls.append("https://" + domain + path)

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        for url in urls:
            res = custom_get(url, headers=headers)
            if res.status_code != expect_code:
                print("check code erro:domain:", url, "status_code:", res.status_code)
                return
            if expect_resp not in str(res.content):
                print("check content erro:domain:", url, "content:", res.content)
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
        expect_resp = "appversion: v5.3.17"
        check_http_https(domain, path, expect_resp)


def check_ad_track(domain_list):
    for domain in domain_list:
        path = "/m_imp"
        expect_resp = '{"status": 0,"msg": ""}'
        check_http_https(domain, path, expect_resp)


def check_analytics(domain_list):
    for domain in domain_list:
        path = "/collect"
        expect_resp = ""
        check_http_https(domain, path, expect_resp, prefix=["http"])


if __name__ == '__main__':
    feedback = [
        "sg-new-hb-bid-feedback.rayjump.com",
        "sg-new-hb-bid-feedback.mtgglobals.com",
        "sg-new-hb-bid-feedback.mintegral.net",
    ]
    # check_feedback(feedback)
    supply = [
        "or-gcp-adx-us-west1-a-ssp-tk.mintegral.net",
        "or-gcp-adx-us-west1-a-ssp-tk.rayjump.com",
        "or-gcp-adx-us-west1-a-ssp-tk.mtgglobals.com",
        "or-gcp-adx-us-west1-b-ssp-tk.mintegral.net",
        "or-gcp-adx-us-west1-b-ssp-tk.rayjump.com",
        "or-gcp-adx-us-west1-b-ssp-tk.mtgglobals.com",
    ]
    # check_supply_tracking(supply)
    adx = [
        "nl-gcp-ssplib-sdk-bid-v2.rayjump.com",
        "sg-gcp-ssplib-sdk-bid-v2.rayjump.com",
    ]
    # check_adx(adx)
    ad_track = [
        "sg-ali-ad-track-sdk.rayjump.com",
        "sg-ali-ad-track-sdk.mtgglobals.com",
        "sg-ali-ad-track-sdk.mintegral.net",
    ]
    # check_ad_track(ad_track)

    analytics = [
        "analytics-eu-gcp-tcp.mtgglobals.com",
        "analytics-sg-gcp-tcp.mtgglobals.com"
    ]
    check_analytics(analytics)
