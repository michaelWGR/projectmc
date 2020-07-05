import os
import time
import argparse


def is_old_file(file_path, duration):
    """
    通过duration判断是否为旧文件
    :param file_path: 文件路径
    :param duration: 文件的保持时间，单位s
    :return: True为旧文件，False为新文件
    """
    if os.path.isfile(file_path):
        c_time = os.path.getctime(file_path)
        present = time.time()
        return present - c_time > duration
    else:
        return False


def read_dir(dir_path):
    """
    遍历文件夹，获取所有文件夹路径
    :param dir_path: 遍历的文件夹路径
    :return: 文件夹下的所有文件路径列表
    """
    all_files = []
    if dir_path[-1] == os.sep:
        print('文件夹路径末尾不能有{}'.format(os.sep))
        return
    if os.path.isdir(dir_path):
        file_list = os.listdir(dir_path)
        for f in file_list:
            f = os.path.join(dir_path, f)
            if os.path.isdir(f):
                sub_files = read_dir(f)
                all_files = sub_files + all_files
            else:
                all_files.append(f)
        return all_files


def rm_old_file(file_path, duration):
    """
    删除旧文件夹
    :param duration: 文件的保持时间，单位s
    :param file_path: 文件路径
    """
    if is_old_file(file_path, duration):
        os.remove(file_path)
        print(file_path)
        print('移除文件：' + file_path)


def rm_empty_dir(dir_path):
    """
    删除空文件夹
    :param dir_path: 文件夹路径
    """
    print(dir_path)
    if os.path.isdir(dir_path):
        for d in os.listdir(dir_path):
            rm_empty_dir(os.path.join(dir_path, d))
    else:
        return
    if not os.listdir(dir_path):
        os.rmdir(dir_path)
        print('移除空目录: ' + dir_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True, dest='path', help='执行的目录')
    parser.add_argument('-d', '-duration', type=int, required=True, dest='duration', help='文件的保留时长，单位秒')
    args = parser.parse_args()
    path = args.path
    duration = args.duration
    for f in read_dir(path):
        rm_old_file(f, duration=duration)
    rm_empty_dir(path)


if __name__ == '__main__':
    main()