# -*- coding: utf-8 -*-
import os
import sys
import traceback
from datetime import datetime

import pytz
import telegram

from ae_logger import ae_log
from ae_telegram_constant import CHAT_ID_AFRICA_ELEPHANT, TELEGRAM_TOKEN, CHAT_ID_AFRICA_ELEPHANT_ERROR, TELEGRAM_COMMAND, TELEGRAM_CMD_STX, TELEGRAM_CMD_SPLIT, TELEGRAM_CMD_ETX

class ae_TelegramMessage:
    tz_seoul = pytz.timezone('Asia/Seoul')

    def __init__(self):
        import os
        from dotenv import load_dotenv
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(dotenv_path=os.path.join(cur_dir, '..', 'telegram.env'), encoding='utf-8')


    def send_message(self, msg, chat_id=CHAT_ID_AFRICA_ELEPHANT, token=TELEGRAM_TOKEN):
        """
    	Send a mensage to a telegram_collect user specified on chatId
    	chat_id must be a number!
    	"""
        bot = telegram.Bot(token=token)
        str_msg = f'{datetime.now(self.tz_seoul).strftime("%Y-%m-%d %H:%M:%S")} | {msg}'
        bot.sendMessage(chat_id=chat_id, text=str_msg)
        ae_log.info(str_msg)

    def send_protocol(self, cmd: TELEGRAM_COMMAND, args:[] = None):
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        str_arg = ""
        arg_len = 0
        if None != args:
            str_arg = ''.join(args)
            arg_len = len(args)
        str_msg = f'{TELEGRAM_CMD_STX}{TELEGRAM_CMD_SPLIT}{cmd.name}{TELEGRAM_CMD_SPLIT}{arg_len}{TELEGRAM_CMD_SPLIT}{str_arg}{TELEGRAM_CMD_SPLIT}{TELEGRAM_CMD_ETX}'
        bot.sendMessage(chat_id=CHAT_ID_AFRICA_ELEPHANT, text=str_msg)
        ae_log.info(str_msg)

    def getTracebackStr(self):
        lines = traceback.format_exc().strip().split('\n')
        rl = [lines[-1]]
        lines = lines[1:-1]
        lines.reverse()
        nstr = ''
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('File "'):
                eles = lines[i].strip().split('"')
                basename = os.path.basename(eles[1])
                lastdir = os.path.basename(os.path.dirname(eles[1]))
                eles[1] = '%s/%s' % (lastdir, basename)
                rl.append('^\t%s %s' % (nstr, '"'.join(eles)))
                nstr = ''
            else:
                nstr += line
        return '\n'.join(rl)

    def send_error(self, msg: str):
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        str_msg = f'[ERROR]\n{msg}'
        bot.sendMessage(chat_id=CHAT_ID_AFRICA_ELEPHANT_ERROR, text=str_msg)
        ae_log.info(str_msg)

    def send_exception(self, app_name: str):
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        exc_info = sys.exc_info()
        # traceback.print_exception(*exc_info)
        # trace = self.getTracebackStr()
        formatted_lines = traceback.format_exc().splitlines()
        tele_msg = ""
        for line in formatted_lines:
            tele_msg = tele_msg + line + "\n"
            # print(line)
        str_msg = f'[EXCEPTION] | {app_name} \n{tele_msg}'
        # bot.sendMessage(chat_id=CHAT_ID_AFRICA_ELEPHANT_ERROR, text=str_msg)
        ae_log.error(str_msg)

ae_tele_message = ae_TelegramMessage()