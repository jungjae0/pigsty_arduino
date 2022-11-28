import atexit

import pandas as pd
import serial
import time
import atexit

# https://kocoafab.cc/fboard/view/2159

s = serial.Serial('COM3', 9600)

# csv 파일 정리
def convert_data(filename, name):

    df = pd.read_csv(filename, encoding='cp949')
    df.rename(columns=df.iloc[1], inplace=True)
    df.drop([0,1], inplace=True)
    df.to_csv(f'./data/{name}.csv', encoding='cp949')
    df = pd.read_csv(f'./data/{name}.csv', encoding='cp949')

    return df


# 아두이노 우노에 신호보내기
def send_signal_to_sfarm(msg):
    if (s.readable()):
        s.write("{}\n".format(msg).encode())
    else:
        print("message is not transferred")

# 환경제어_환경장치
# vent - 40, 50, 60, 70, 80, 90
def cvent(df_control):
    vent_value = df_control["Vent"]
    if 40 <= vent_value < 60:
        return "CFAN-1"
    elif 60 <= vent_value <80:
        return "CFAN-2"
    elif 80 <= vent_value:
        return "CFAN-3"
    else:
        return "CFAN-0"

# heat - 3, 2, 1, 0
def cheat(df_control):
    heat_value = df_control["Heater"]
    if heat_value == 3:
        # send_signal_to_sfarm("HEAT-1")
        return "CHEAT-3"
    elif heat_value == 2:
        # send_signal_to_sfarm("HEAT-1")
        return "CHEAT-2"
    elif heat_value == 1:
        # send_signal_to_sfarm("HEAT-1")
        return "CHEAT-1"
    else:
        return "CHEAT-0"

# fog-1은 on, 2는 off
def cfog(df_control):
    fog_value = df_control["Fogging"]
    if fog_value == 0:
        return "CFOG-1"
    else:
        return "CFOG-0"


# 미설치_환경장치
# vent - 40, 50, 60, 70, 80, 90
def nvent(df_normal):
    vent_value = df_normal["Vent"]
    if 40 <= vent_value < 60:
        return "CFAN-1"
    elif 60 <= vent_value <80:
        return "CFAN-2"
    elif 80 <= vent_value:
        return "CFAN-3"
    else:
        return "CFAN-0"
    # if vent_value == 90:
    #     # send_signal_to_sfarm("FAN-1")
    #     return "NFAN-9"
    # elif vent_value == 80:
    #     # send_signal_to_sfarm("FAN-1")
    #     return "NFAN-8"
    # elif vent_value == 70:
    #     # send_signal_to_sfarm("FAN-1")
    #     return "NFAN-7"
    # elif vent_value == 60:
    #     # send_signal_to_sfarm("FAN-1")
    #     return "NFAN-6"
    # elif vent_value == 50:
    #     # send_signal_to_sfarm("FAN-1")
    #     return "NFAN-5"
    # else:
    #     return "NFAN-0"
    #     # send_signal_to_sfarm("FAN-0")


# heat - 3, 2, 1, 0
def nheat(df_normal):
    heat_value = df_normal["Heater"]
    if heat_value == 3:
        # send_signal_to_sfarm("HEAT-1")
        return "NHEAT-3"
    elif heat_value == 2:
        # send_signal_to_sfarm("HEAT-1")
        return "NHEAT-2"
    elif heat_value == 1:
        # send_signal_to_sfarm("HEAT-1")
        return "NHEAT-1"
    else:
        return "NHEAT-0"


# fog-1은 on, 2는 off
def nfog(df_normal):
    fog_value = df_normal["Fogging"]
    if fog_value == 0:
        return "NFOG-1"
    else:
        return "NFOG-0"

def handle_exit():
    return send_signal_to_sfarm("CFAN-0CHEAT-0CFOG-0NFAN-0NHEAT-0NFOG-0")

def main():

    control_filenmae = "./data/시나리오 더미 데이터_환경제어.csv"
    normal_filename = "./data/시나리오 더미 데이터_미설치.csv"

    df_control_name = "control_scenario"
    df_normal_name = "normal_scenario"

    df_control = convert_data(control_filenmae, df_control_name)
    df_normal = convert_data(normal_filename, df_normal_name)

    for i in range(len(df_control.index)):
        control_scenario = df_control.iloc[i]
        normal_scenario = df_normal.iloc[i]

        # print(df_control.iloc[i], df_normal.iloc[i])
        control_rule = [cvent(control_scenario), cheat(control_scenario), cfog(control_scenario)]
        normal_rule = [nvent(normal_scenario), nheat(normal_scenario), nfog(normal_scenario)]

        # 아두이노에 시나리오 신호 보내기
        send_signal_to_sfarm("".join(control_rule))
        send_signal_to_sfarm("".join(normal_rule))

        print(f"send signal: {''.join(control_rule)}")
        print(f"send signal: {''.join(normal_rule)}")
        time.sleep(3)

        atexit.register(handle_exit)

    # print(df_control["Heater"].unique())
    # print(df_normal["Heater"].unique())



if __name__ == '__main__':
    main()

# # 시나리오 csv 불러오기
# df_control = pd.read_csv("C:\code\pigsty\data\시나리오 더미 데이터_환경장치.csv", encoding='utf-8')
# df_none = pd.read_csv("C:\code\pigsty\data\시나리오 더미 데이터_미설치.csv", encoding='utf-8')
#
# # column 명 변경
# df_control = df_control.rename(columns=df_control.iloc[1])
# df_control = df_control.drop([0,1])
#
# df_none = df_none.rename(columns=df_none.iloc[1])
# df_none = df_none.drop([0,1])
#
# # 정리한 df를 csv 파일로 저장
# df_control.to_csv('./data/control_scenario.csv', index=None)
# df_none.to_csv('./data/none_scenario.csv', index=None)
#
# # 정리한 파일 불러오기
# df_control = pd.read_csv('./data/control_scenario.csv', encoding='utf-8')
# df_normal = pd.read_csv('./data/none_scenario.csv', encoding='utf-8')
