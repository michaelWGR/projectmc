import json
import xmind
import sys
import os

sensive_word = ['公会', '工会', '家族', '会长', '陪陪', '主播', '妹子'
                '分成', '返点', '抽成', '分销', '直招']

sensive_replace = {'公会': '推广', '':''}

def read_xmind(path):
    workbook = xmind.load(path)
    sheet = workbook.getPrimarySheet()
    print(sheet.getData())


def genXmindByJson(parent, data):
    if data is None:
        return
    node = parent.addSubTopic()
    for key in data:
        if key == 'title':
            # print(data['title'])
            node.setTitle(data['title'])
        # elif key == 'link':
        #     node.setURLHyperlink(data['link'])
        elif key == 'labels':
            node.addLabel(data['labels'][0])
        elif key == 'topic':
            node.setTitle(data['title'])
        elif key == 'topics':
            if isinstance(data['topics'], dict):
                genXmindByJson(node, data['topics'])
            elif isinstance(data['topics'], list):
                for i in range(len(data['topics'])):
                    genXmindByJson(node, data['topics'][i])
            else:
                print("其它类型")


def genJsonData(filepath):
    workbook = xmind.load(filepath)
    sheet = workbook.getPrimarySheet()
    root = sheet.getRootTopic()
    data_dict = root.getData()
    return data_dict


def replace_by_dict(data):
    word = '个人主页'
    for key in data:
        if key != 'topics':
            if data[key] == word:
                print(data[key])
                data[key] = '这是个人主页'
        else:
            if isinstance(data['topics'], dict):
                replace_by_dict(data['topics'])
            elif isinstance(data['topics'], list):
                for i in range(len(data['topics'])):
                    replace_by_dict(data['topics'][i])
            else:
                print("其它类型")
    return data



def genXmind(filepath, savefilepath):
    if os.path.exists(savefilepath):
        os.remove(savefilepath)
    filename = os.path.splitext(os.path.split(filepath)[-1])[0]
    workbook = xmind.load(savefilepath)
    sheet = workbook.getPrimarySheet()

    root = sheet.getRootTopic()
    root.setTitle(filename)
    # data_dict = root.getData()
    data_dict = genJsonData(filepath)
    data = replace_by_dict(data_dict)
    print(data)
    root.setStructureClass = "org.xmind.ui.logic.right"
    genXmindByJson(root, data)
    xmind.save(workbook, path=savefilepath)


if __name__ == '__main__':
    # genJsonData('/Users/michael/Downloads/dwn/个人主页.xmind')
    genXmind("/Users/michael/Downloads/dwn/个人主页.xmind", '/Users/michael/Downloads/dwn/res/个人主页.xmind')
