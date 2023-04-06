import json
import requests
import wget
import ssl
import os
from res import SUBJECTS
import time, random
import MuyunxiSupports

log = MuyunxiSupports.log('', 'log')

ssl._create_default_https_context = ssl._create_unverified_context

if not os.path.exists('./files'):
    os.mkdir('files')

def get_types(subject:str, year:int, season:str):
    """
    根据学科，年份，以及季节，获取可用的试卷

    :param subject: 学科编号
    :param year: 年
    :param season: 季节 ( Jun / Nov / Mar / Gen )
    :return:
    """

    url = "https://cie.fraft.cn/obj/Fetch/renum"
    data = {
        "subject": subject,
        "year": year,
        "season": season
    }
    req = requests.post(url, data=data)
    # print(req.text)

    return_data = json.loads(req.text)

    if return_data['status'] == 0:
        return return_data['data']
    else:
        return None


def get_file(file_name:str):
    url = 'https://cie.fraft.cn/obj/Fetch/redir/' + file_name
    # 创建文件夹
    segments = file_name.split('_')
    dir_name = SUBJECTS[segments[0]]  # 学科
    sub_dir_name = '20' + segments[1][1:]  # 年份
    fpath = os.path.join("./files", dir_name, sub_dir_name)
    if not os.path.exists(fpath):
        os.makedirs(fpath)

    wget.download(url, out=fpath+'/'+file_name)
    log.add_log(f'Downloaded FILE: {fpath}/{file_name}', 0)
    time.sleep(random.random())


YEARS = list(range(2015, 2023+1))

SEASONS = ['Gen', 'Jun', 'Mar', 'Nov']

if __name__ == "__main__":
    for subject in SUBJECTS:
        for year in YEARS:
            for season in SEASONS:
                files = get_types(subject, year, season)
                if files:
                    for name, status in files:
                        get_file(name)
