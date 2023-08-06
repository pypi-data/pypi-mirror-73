# python3.7
# encoding: utf-8
"""
@author: Chenjin.Qian
@email:  chenjin.qian@xquant.com
@file:   tests.py
@time:   2020-07-10 13:29
"""
from exception_sms.logs_models import GetNotification

logs = GetNotification(
    "HGBjkUdjqKegADBDmVvTkmf2_dTEIJawM39um0MI",
    "I2Lj4zNysPkpme6HCrEzkymkkP8rzjH-bHfeP2l7",
    "1281023854495416320",
    "Jingxuan",
    "18606511719",
    r"D:\test\logs"
)


@logs.exce_note
def tes(x, y):
    a = x / y
    return a


if __name__ == '__main__':
    b = tes(0, 0)
    print(b)
