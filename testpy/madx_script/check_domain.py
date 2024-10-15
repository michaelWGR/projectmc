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


def check_ad_track(domain_list):
    for domain in domain_list:
        path = "/impression"
        expect_resp = '{"status": 0,"msg": ""}'
        check_http_https(domain, path, expect_resp)


if __name__ == '__main__':
    feedback = [
        "or-gcp-adx-us-west1-a-bid-feedback.mintegral.net",
        "or-gcp-adx-us-west1-a-bid-feedback.rayjump.com",
        "or-gcp-adx-us-west1-a-bid-feedback.mtgglobals.com",
        "or-gcp-adx-us-west1-b-bid-feedback.mintegral.net",
        "or-gcp-adx-us-west1-b-bid-feedback.rayjump.com",
        "or-gcp-adx-us-west1-b-bid-feedback.mtgglobals.com",
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
        "or-gcp-madx-adx.mobvista.com",
    ]
    # check_adx(adx)
    ad_track = [
        "or-gcp-ad-track-adx.mintegral.net",
        "or-gcp-ad-track-adx.rayjump.com",
        "or-gcp-ad-track-adx.mtgglobals.com",
        "or-gcp-ad-track-adx-us-west1-a.mintegral.net",
        "or-gcp-ad-track-adx-us-west1-a.rayjump.com",
        "or-gcp-ad-track-adx-us-west1-a.mtgglobals.com",
        "or-gcp-ad-track-adx-us-west1-b.mintegral.net",
        "or-gcp-ad-track-adx-us-west1-b.rayjump.com",
        "or-gcp-ad-track-adx-us-west1-b.mtgglobals.com",
    ]
    check_ad_track(ad_track)



