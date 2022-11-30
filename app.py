import pandas as pd
import serial
import time
import atexit

# 아두이노 포트 번호 입력(아두이노와 Python의 연결)
s = serial.Serial('COM3', 9600)

# csv 파일 정리
def convert_data(filename, name):

    # csv파일 읽기 및 인코딩
    df = pd.read_csv(filename, encoding='cp949')
    # column명 재설정
    df.rename(columns=df.iloc[1], inplace=True)
    # 필요없는 행 제거
    df.drop([0,1], inplace=True)
    # 정리한 파일 저장
    df.to_csv(f'./data/{name}.csv', encoding='cp949')
    # 정리한 파일 읽기
    df = pd.read_csv(f'./data/{name}.csv', encoding='cp949')

    return df


# 아두이노 우노에 신호보내기위한 함수 정의
def send_signal_to_sfarm(msg):
    if (s.readable()):
        s.write("{}\n".format(msg).encode())
    else:
        print("message is not transferred")

#### 환경제어_환경장치 ####
# vent - 40, 50, 60, 70, 80, 90
def cvent(df_control):
    # df에서 Vent열만 읽기
    vent_value = df_control["Vent"]
    # Vent 한 셀의 값이 40이상 60미만이면 "CFAN-1"
    if 40 <= vent_value < 60:
        return "CFAN-1"
    # Vent 한 셀의 값이 60이상 80미만이면 "CFAN-1"
    elif 60 <= vent_value <80:
        return "CFAN-2"
    # Vent 한 셀의 값이 80이상이면 "CFAN-1"
    elif 80 <= vent_value:
        return "CFAN-3"
    # Vent 한 셀의 값이 30이하이면 "CFAN-0"
    else:
        return "CFAN-0"

# heat - 3, 2, 1, 0
def cheat(df_control):
    heat_value = df_control["Heater"]
    if heat_value == 3:
        return "CHEAT-3"
    elif heat_value == 2:
        return "CHEAT-2"
    elif heat_value == 1:
        return "CHEAT-1"
    else:
        return "CHEAT-0"

# fog - 1은 on, 0은 off
def cfog(df_control):
    fog_value = df_control["Fogging"]
    if fog_value == 0:
        return "CFOG-1"
    else:
        return "CFOG-0"


#### 미설치_환경장치 ####
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

# heat - 3, 2, 1, 0
def nheat(df_normal):
    heat_value = df_normal["Heater"]
    if heat_value == 3:
        return "NHEAT-3"
    elif heat_value == 2:
        return "NHEAT-2"
    elif heat_value == 1:
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

# python 프로그램 실행을 중단하였을 때 아두이노 기기들이 모두 작동하지 않도록 하기 위한 함수 정의
# python 프로그램이 중단되었을 때 모두 끄는 명렁어를 아두이노에 전달한다.
def handle_exit():
    return send_signal_to_sfarm("CFAN-0CHEAT-0CFOG-0NFAN-0NHEAT-0NFOG-0")

def main():

    # 제공된 시나리오 더미 데이터 정의
    control_filenmae = "./data/시나리오 더미 데이터_환경제어.csv"
    normal_filename = "./data/시나리오 더미 데이터_미설치.csv"

    # 앞의 더미 데이터를 정리 후 저장할 파일 정의
    df_control_name = "control_scenario"
    df_normal_name = "normal_scenario"

    # 앞서 정의한 함수를 실행 -> 제공된 시나리오 더미 데이터를 정리, 정리한 데이터를 불러옴
    df_control = convert_data(control_filenmae, df_control_name)
    df_normal = convert_data(normal_filename, df_normal_name)

    # 각 행에 대한 연산을 반복
    for i in range(len(df_control.index)):
        control_scenario = df_control.iloc[i]
        normal_scenario = df_normal.iloc[i]

        # 각 셀에 해당하는 조건에 맞는 return 값을 모아 list형태로 저장
        control_rule = [cvent(control_scenario), cheat(control_scenario), cfog(control_scenario)]
        normal_rule = [nvent(normal_scenario), nheat(normal_scenario), nfog(normal_scenario)]

        # 앞선 list 형태를 문자열 형태로 변경하여 아두이노에 신호전달
        # 앞서 정의한 아두이노에 신호를 보내기 위한 함수 실행
        send_signal_to_sfarm("".join(control_rule))
        send_signal_to_sfarm("".join(normal_rule))

        print(f"send signal: {''.join(control_rule)}")
        print(f"send signal: {''.join(normal_rule)}")

        # 한 행을 몇 초 동안 수행할 것인지 정함
        # '3' = '3초' ; 원하는 시간으로 바꾸면 됨
        time.sleep(3)

        # 프로그램을 중단하였을 떄 led 및 환기팬 작동을 멈춤
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
