import json


def get_repaly_xpath(repaly_path):
    # 获取exp_layer
    repaly_xpath = []
    with open(repaly_path, "r") as f:
        reads = f.readlines()
    for r in reads:
        layer = "/".join(r.split("/")[0:-1])
        if layer not in repaly_xpath:
            repaly_xpath.append(layer.strip())
    print(len(repaly_xpath))
    print(repaly_xpath)
    return repaly_xpath


def get_exp_layer(path):
    with open(path, 'r') as f:
        read = f.read()
    exp_dict = json.loads(read)
    expinfo = exp_dict["expInfo"]["MTG"]
    xpath = get_xpath(expinfo)
    layer_path = []
    for expath in xpath:
        layer = "/".join(expath.split("/")[0:-1])
        if layer not in layer_path:
            layer_path.append(layer)

    print("online exp_layer:", len(layer_path))
    print(layer_path)
    return layer_path


def get_xpath(dict_data):
    xpath = []
    if dict_data["type"] == "TYPE_EXPERIMENT":
        if dict_data["xPath"] and dict_data.get("quota") > 0:
            xpath.append(dict_data["xPath"])
    if dict_data.get("children"):
        for child in dict_data.get("children"):
            child_xpath = get_xpath(child)
            xpath = xpath + child_xpath

    return xpath


def diff_xpath(online_xpath, repaly_xpath):
    diff = {}
    replay_p = repaly_xpath
    for onxpath in online_xpath:
        diff[onxpath] = 0
        for rexpaht in repaly_xpath:
            if onxpath in rexpaht:
                diff[onxpath] = 1
                replay_p.remove(onxpath)

    same = []
    replay_miss = []
    for d in diff:
        if diff[d] == 1:
            same.append(d)
        elif diff[d] == 0:
            replay_miss.append(d)

    print("same:", len(same))
    print("same:", same)
    print("replay_miss:", len(replay_miss))
    print("replay_miss:", replay_miss)
    print("online_miss:", len(replay_p))
    print("online_miss:", replay_p)



if __name__ == '__main__':
    print("====sdk")
    path = "/Users/mobvista/Documents/mtg/need/abtest反推实验优化/sdk_abtest.json"
    exp_layer = get_exp_layer(path)
    repaly_path = "/Users/mobvista/Documents/mtg/need/abtest反推实验优化/sdk_xpath.txt"
    repaly_xpath = get_repaly_xpath(repaly_path)
    diff_xpath(exp_layer, repaly_xpath)

    print("===adx")
    adx_path = "/Users/mobvista/Documents/mtg/need/abtest反推实验优化/adx_abtest.json"
    adx_exp_layer = get_exp_layer(adx_path)
    adx_repaly_path = "/Users/mobvista/Documents/mtg/need/abtest反推实验优化/adx_xpath.txt"
    adx_repaly_xpath = get_repaly_xpath(adx_repaly_path)
    diff_xpath(adx_exp_layer, adx_repaly_xpath)


