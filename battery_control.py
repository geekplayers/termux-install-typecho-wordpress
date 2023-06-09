import argparse
import time
import subprocess
from miio import Device

#blog:linzimo.com

# 设置插座的IP地址和令牌
# 设置插座的IP地址和令牌
ip = "192.168.6.181"
token = "5735d4a2ce13e339ac560a6d7f3e2131"

def get_battery_info():
    battery_info = subprocess.check_output(['termux-battery-status']).decode('utf-8')
    battery_data = {
        'level': int(battery_info.split('"percentgage":')[1].split(',')[0]),
        'temperature': float(battery_info.split('"temperature":')[1].split(',')[0])
    }
    return battery_data

def toggle_gosund_plug(ip, token, state):
    device = Device(ip, token)
    device.send("set_properties", [{"siid": 2, "piid": 1, "did": "state", "value": state}])
    print(f"Gosund插座已{'打开' if state else '关闭'}")

# 解析命令行参数
parser = argparse.ArgumentParser(description='Battery Control')
parser.add_argument('-on', action='store_true', help='打开插座')
parser.add_argument('-off', action='store_true', help='关闭插座')
parser.add_argument('-start', action='store_true', help='开始自动检测触发开关服务')
parser.add_argument('-test', action='store_true', help='测试打开和关闭')
args = parser.parse_args()


if args.on:
    toggle_gosund_plug(ip, token, True)  # 打开插座
elif args.off:
    toggle_gosund_plug(ip, token, False)  # 关闭插座
elif args.test:
        print("正在尝试打开插座...")
        toggle_gosund_plug(ip, token, True)  # 打开插座
        time.sleep(3)
  
        print("正在尝试关闭插座...")
        toggle_gosund_plug(ip, token, False)  # 关闭插座
        time.sleep(3)
  
        print("正在尝试termux-api命令 termux-battery-status...")
        battery_data = get_battery_info()
        print("当前电池信息：")
        print(f"电量：{battery_data['level']}%")
        print(f"温度：{battery_data['temperature']}°C")
elif args.start:
    battery_low_threshold = 50  # 电池电量低于此阈值时，打开插座
    battery_high_threshold = 90  # 电池电量高于此阈值时，关闭插座
    temperature_threshold = 40  # 电池温度高于此阈值时，关闭插座
    
    print("开始自动检测并开关服务...")
    # 运行自动开关逻辑
    while True:
        battery_data = get_battery_info()
        battery_level = battery_data['level']
        battery_temp = battery_data['temperature']

        if battery_level < battery_low_threshold:
            print("当前电量低于{battery_low_threshold}，打开插座")
            toggle_gosund_plug(ip, token, True)  # 打开插座
        elif battery_level > battery_high_threshold or battery_temp > temperature_threshold:
            print("当前电量高于{battery_high_threshold}，或温度高于{temperature_threshold}，关闭插座")
            toggle_gosund_plug(ip, token, False)  # 关闭插座

        time.sleep(60)  # 每隔60秒检查一次电池电量和温度
else:
    parser.print_help()
