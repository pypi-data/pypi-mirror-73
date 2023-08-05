# coding:utf-8
import sys
import fire

from src.user_info_manager import UserInfoManager
from src.stamp_manager import StampManager
from src.attendance_manager import AttendanceManager


class Dakoker(object):
    """
    Dakoker:                MFクラウド勤怠向けの打刻ツールです\n

    dakoker start:          出勤の打刻をします\n
    dakoker end:            退勤の打刻をします\n
    dakoker start_break:    休憩開始の打刻をします\n
    dakoker end_break:      休憩終了の打刻をします\n
    dakoker today:          当日の勤怠状況を確認できます\n
    dakoker ckear:          ユーザーログイン情報のローカルキャッシュをクリアします\n
    """

    def start(self):
        """
        dakoker start:          出勤の打刻をします
        """
        StampManager().stamp(sys._getframe().f_code.co_name)

    def end(self):
        """
        dakoker end:            退勤の打刻をします
        """
        StampManager().stamp(sys._getframe().f_code.co_name)

    def start_break(self):
        """
        dakoker start_break:    休憩開始の打刻をします
        """
        StampManager().stamp(sys._getframe().f_code.co_name)

    def end_break(self):
        """
        dakoker end_break:      休憩終了の打刻をします
        """
        StampManager().stamp(sys._getframe().f_code.co_name)

    def today(self):
        """
        dakoker today:          当日の勤怠状況を確認できます
        """
        AttendanceManager().confirm(sys._getframe().f_code.co_name)

    def clear(self):
        """
        dakoker ckear:          ユーザーログイン情報のローカルキャッシュをクリアします
        """
        UserInfoManager.remove_with_message()


def main():
    fire.Fire(Dakoker)
