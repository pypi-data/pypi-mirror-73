import math
import os
import re
import time
from pathlib import Path


def tell_the_datetime(time_stamp=None, compact_mode=False):
    time_stamp = time_stamp if time_stamp else time.time()
    if not compact_mode:
        format_str = '%Y-%m-%d %H:%M:%S'
    else:
        format_str = '%Y-%m-%d-%H-%M-%S'
    tm = time.strftime(format_str, time.localtime(time_stamp))
    return tm


def convert_bytes(bts, lst=None, refresh_rate="s"):
    if lst is None:
        lst = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = int(math.floor(  # 舍弃小数点，取小
        math.log(int(bts) or 1, 1024)  # 求对数(对数：若 a**b = N 则 b 叫做以 a 为底 N 的对数)
    ))

    if i >= len(lst):
        i = len(lst) - 1
    return ('%.2f' + f" {lst[i]}/{refresh_rate}") % (bts / math.pow(1024, i))


def find_local_redis_pass():
    rc_path_tmp = os.popen("whereis 'redis.conf'").read().split(' ')[-1].strip()
    rd_pass = None
    if rc_path_tmp:
        rcf_path = Path(rc_path_tmp)
        if rcf_path.is_dir():
            rcf_path = rcf_path / "redis.conf"
            if rcf_path.exists():
                rcf = get_file_lines(str(rcf_path.absolute()))
                rd_pass = [re.findall("^requirepass(.*)", x)[0].strip() for x in rcf if re.findall("^requirepass(.*)", x)][0]
    return rd_pass


def get_file_lines(f_path):
    try:
        with open(f_path, 'r') as rf:
            f_lines = rf.readlines()
    except PermissionError:
        f_lines = os.popen(f"sudo cat {f_path}").read().split('\n')
    f_lines = [x.strip() for x in f_lines]
    return f_lines


def main():
    print(convert_bytes(int(input('Bytes: '))))


if __name__ == '__main__':
    print(find_local_redis_pass())
