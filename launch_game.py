import platform
import subprocess
import threading
import time

from generate_traffic import *
from manual_control import *


import socket

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        sock.close()


def launch_carla():
    # 如果CarlaUE4.exe已经启动，则跳过
    host = 'localhost'
    port = 2000
    if check_port(host, port):
        print(f'The port {port} on {host} is open. Pass launch CarlaUE4.exe')
        return 0
    else:
        print(f'The port {port} on {host} is closed.')

    launch_info = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'WindowsNoEditor_9.15', 'CarlaUE4.exe -RenderOffscreen')
    # 等待调用的程序执行结束后再运行
    os.popen(launch_info)
    print("launch carla")
    time.sleep(20)


# class Manual_Control:
#     def manual_control_method(self):
#         while(True):
#             print("Manual control")
#             manual_control()


if __name__ == '__main__':

    launch_carla()

    # 使用独立的现成启动交通管理器
    if platform.system().lower() == 'windows':
        gen_traffic_cmd = 'start ' + sys.executable + ' ' + os.path.join(os.path.split(os.path.realpath(__file__))[0], 'generate_traffic.py')
    elif platform.system().lower() == 'linux':
        gen_traffic_cmd = sys.executable + ' ' + os.path.join(os.path.split(os.path.realpath(__file__))[0], 'generate_traffic.py') + ' &'

    # creationflags 设置为 0x08000000，是隐藏cmd窗口的标识（无效）
    subprocess.Popen(gen_traffic_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, creationflags=0x08000000)
    # os.system(gen_traffic_cmd)

    manual_control()

