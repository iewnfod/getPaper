import json
import requests
import wget
import ssl
import os
from res import SUBJECTS
import time, random
import MuyunxiSupports

log = MuyunxiSupports.log('', 'Get Paper Log')

ssl._create_default_https_context = ssl._create_unverified_context

target_dir = 'pastpaper'

if not os.path.exists(f'./{target_dir}'):
    os.mkdir(target_dir)

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "33",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "cie.fraft.cn",
    "Origin": "https://cie.fraft.cn",
    "Referer": "https://cie.fraft.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62 X-Requested-With: XMLHttpRequest",
    "sec-ch-ua": '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS"
}


def get_types(subject:str, year:int, season:str):
    """
    根据学科，年份，以及季节，获取可用的试卷

    :param subject: 学科编号
    :param year: 年
    :param season: 季节 ( Jun / Nov / Mar / Gen )
    :return: 返回所有文件
    """

    url = "https://cie.fraft.cn/obj/Fetch/renum"
    data = {
        "subject": subject,
        "year": year,
        "season": season
    }
    req = requests.post(url, data=data, headers=headers)
    # print(req.text)

    return_data = json.loads(req.text)

    if return_data['status'] == 0:
        return return_data['data']
    else:
        return None


def draw_bar(current, total, width=80):
    width = 80
    percent = int(current / total * width)
    print('[' + '\033[92m🁢\033[0m'*percent + '🁢'*(width - percent) + ']', current, '/', total, end='\r')


def get_file(file_name: str):
    url = 'https://cie.fraft.cn/obj/Fetch/redir/' + file_name
    # 创建文件夹
    segments = file_name.split('_')
    dir_name = SUBJECTS[segments[0]]  # 学科
    sub_dir_name = '20' + segments[1][1:]  # 年份
    dir_path = os.path.join(target_dir, dir_name, sub_dir_name)
    f_path = os.path.join(dir_path, file_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if os.path.exists(f_path):
        log.add_log(f'FILE {f_path} has existed', 1)
        return

    wget.download(url, out=f_path)
    print()
    log.add_log(f'Downloaded FILE: {f_path}', 0)
    time.sleep(random.random())

SUBJECT_LISTS = list(SUBJECTS.keys())

YEARS = list(range(2018, 2023+1))

SEASONS = ['Gen', 'Jun', 'Mar', 'Nov']

def save(subject, year, season):
    with open('.saves', 'w') as f:
        f.write(f'{subject} {year} {season}')


def load():
    if not os.path.exists('.saves'):
        return SUBJECT_LISTS[0], -1, SEASONS[0]
    with open('.saves', 'r') as f:
        data = f.read().split(' ')
    return data[0], int(data[1]), data[2]


if __name__ == "__main__":
    last_subject, last_year, last_season = load()
    for subject in SUBJECTS:
        if SUBJECT_LISTS.index(last_subject) > SUBJECT_LISTS.index(subject):
            continue
        for year in YEARS:
            if last_year > year:
                continue
            for season in SEASONS:
                if SEASONS.index(last_season) > SEASONS.index(season):
                    continue
                try:
                    files = get_types(subject, year, season)
                except Exception as err:
                    log.add_log(str(err), 2)
                    continue
                if files:
                    for name, status in files:
                        try:
                            get_file(name)
                            save(subject, year, season)
                        except Exception as err:
                            log.add_log(str(err), 2)
                            wait_time = 10
                            while 1:
                                try:
                                    log.add_log(f'Retry {name}', 1)
                                    time.sleep(wait_time)
                                    get_file(name)
                                    break
                                except:
                                    wait_time += 10
