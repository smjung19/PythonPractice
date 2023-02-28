# ====================================================================================================

import os
import time
import six
import re
import clipboard
import keyboard
from google.cloud import translate_v2 as translate

# ====================================================================================================

my_path = os.path.dirname(os.path.realpath(__file__))                                                       # .py 파일 위치

CREDENTIALS_PATH = my_path + "\\credentials.json"                                                           # 개별 Credential 이용-교체 필요

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH                                             # 환경변수에 Credential 등록

# ====================================================================================================

def translate_text(target, text):
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("UTF-8")

    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]
    #print(u"Text: {}".format(result["input"]))
    #print(u"Translation: {}".format(result["translatedText"]))
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

def PyRefmover():                                                                                           # 각주 표시 제거 함수
    tmp_str = clipboard.paste()                                                                             # Clipboard에서 복사
    tmp_str = tmp_str.replace('\r', '').replace('\n', ' ')                                                  # 줄바꿈 제거
    tmp_str = tmp_str.replace('Į','α').replace('ȕ','β').replace('Ȗ', 'γ')
    for i in my_dict:
        tmp_str = tmp_str.replace(i, i + '@')
    tmp_str = re.sub(r'\ (\d{1,2})\ ', ' \\1@ ', tmp_str)
    tmp_str = re.sub(r'([a-z].*?)(\d[ 0-9,–\-]*\d+)([,.\ ])', '\\1\\3', tmp_str)                            # 각주 제거
    tmp_str = re.sub(r'\ [ 0-9,–\-]*([ ,.])', '\\1', tmp_str)                                               #  각주 제거
    tmp_str = re.sub(r'\([ 0-9,–\-]*\)', '', tmp_str)                                                       # (각주) 제거
    tmp_str = re.sub(r'\[[ 0-9,–\-]*\]', '', tmp_str)                                                       # [각주] 제거
    tmp_str = re.sub(r'\ ,', ',', tmp_str)                                                                  # , 앞 공백 제거
    tmp_str = re.sub(r'\ \.', '.', tmp_str)                                                                 # . 앞 공백 제거
    tmp_str = re.sub(r'\.,', ',', tmp_str)
    tmp_str = re.sub(r',,', ',', tmp_str)
    tmp_str = re.sub(r'\.\.', '.', tmp_str )
    tmp_str = re.sub(r'\ \ ', ' ', tmp_str)                                                                 # 2번 연속되는 공백 제거
    for i in my_dict:
        tmp_str = tmp_str.replace(i + '@', i)
    tmp_str = re.sub(r'(\d)@', '\\1', tmp_str)
    return tmp_str

def toggler(mode, state):
    if state == True:
        time.sleep(0.1)                                                                                     # 연속 전환 방지
        print(mode + ": OFF\r")
        return False
    else:
        time.sleep(0.1)                                                                                     # 연속 전환 방지
        print(mode + ": ON \r")
        return True

# ====================================================================================================

my_dict = []

# ====================================================================================================

my_dict_f = open(my_path + '/mydict.txt', "r")                                                              # 각주 제거 예외처리(e.g., CD4, CD8)
lines = my_dict_f.readlines()
for line in lines:
    my_dict.append(line.strip())
my_dict_f.close()

# ====================================================================================================

while True:
    print("Google API 이용 자동 번역기(유료 버전 ver.1)\n")
    print("사용법: 1) 복사할 내용 드래그 후 Ctrl + C")
    print("        2) [자동으로 번역 또는 각주 표시 제거]")
    print("        3) 원하는 곳에 Ctrl + V\n")
    print("ON/OFF 전환: F2 누르기\n")
    print("자동 번역기(1)\n각주 제거기(2)\n종료(F4)\n")
    flag = True
    select = ''
    while True:
        if keyboard.is_pressed("1"):
            select = 'Translator'
            os.system('cls')
            print("번역: ON ")
            print("\n뒤로가기(F4)")
            break
        elif keyboard.is_pressed("2"):
            select = 'Refmover'
            os.system('cls')
            print("각주 제거: ON ")
            print("\n뒤로가기(F4)")
            break
        elif keyboard.is_pressed("F4"):
            select = 'Quit'
            break
        time.sleep(0.05)
    
    if select == 'Quit':
        break

    while select == 'Translator':                                                                           # 자동 번역기
        if keyboard.is_pressed("F2"):                                                                       # F2로 On/Off 토글
            os.system("cls")
            flag = toggler('번역', flag)
            print("\n뒤로가기(F4)")
        elif keyboard.is_pressed("F4"):                                                                     # F4로 이전 단계로 이동
            time.sleep(0.1)
            break
        elif flag and keyboard.is_pressed("Ctrl") and keyboard.is_pressed("c"):                             # Ctrl C 감지
            os.system('cls')
            print("번역: ON ")
            text = PyRefmover()                                                                             # 문자열 text에 각주 제거된 문자열 대입
            print("...\r", end = "")
            text = translate_text("ko", text)
            clipboard.copy(text)
            print("         ")
            print(text)
            print("\n뒤로가기(F4)")
            time.sleep(0.1)
        else:
            time.sleep(0.05)                                                                                # 속도 제한용 0.05초 대기

    while select == 'Refmover':                                                                             # 각주 제거기
        if keyboard.is_pressed("F2"):                                                                       # F2로 On/Off 토글
            os.system("cls")
            flag = toggler('각주 제거', flag)
            print("\n뒤로가기(F4)")
        elif keyboard.is_pressed("F4"):                                                                     # F4로 이전 단계로 이동
            time.sleep(0.1)
            break
        elif flag and keyboard.is_pressed("Ctrl") and keyboard.is_pressed("c"):                             # Ctrl C 감지
            os.system("cls")
            print("각주 제거: ON ")
            print("...\r", end = "")
            text = PyRefmover()
            print("         ")
            print(text)
            clipboard.copy(text)
            print("\n뒤로가기(F4)")
            time.sleep(0.1)
        else:
            time.sleep(0.05)
    os.system("cls")
