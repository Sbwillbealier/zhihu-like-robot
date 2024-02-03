import random
import time
import pyautogui

from pynput import keyboard
import threading

# 监听ESC键标识（监听到ESC键时，停止运行）
listener_esc = False

# 图像样本的路径
agree_path = 'image/agree.png'
read_more_path = 'image/read_more.png'
close_path = 'image/close.png'

# 休息时长（单位s，最好调长一点）
sleep_time = 1

# 置信度(建议调高，不然容易误触)
confidence = 0.8

# 鼠标滚动速度
scroll_speed = 10


def on_press(key):
    # 按键按下时的操作
    try:
        if key == keyboard.Key.esc:
            # 当检测到ESC键被按下时，输出信息并停止监听
            print('ESC键被按下，停止监听。')

            # ESC已按下
            global listener_esc
            listener_esc = True
            # 返回False来停止监听器
            return False
    except AttributeError:
        pass


def get_a_number(a, b):
    """
    生成一个随机数[a, b]
    :return:
    """
    return random.Random().randint(a, b)


def on_release(key):
    # 按键释放时的操作
    pass


def start_listener():
    """
    监听ESC键
    :return:
    """
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def reading():
    """
    模拟阅读
    1、随机滚动鼠标次数
    2、随机滚动像素行数
    :return:
    """
    # 随机上下滚动鼠标次数（）
    scroll_times = get_a_number(1, 3)

    while scroll_times > 0 and not listener_esc:
        # 随机滚动像素行数
        lines = get_a_number(50, 100)

        # 向下滑动
        for _ in range(int(lines / scroll_speed)):
            pyautogui.scroll(-scroll_speed)
        time.sleep(sleep_time)

        # 向上滑动，为了能回到刚刚的位置
        for _ in range(int(lines / scroll_speed)):
            pyautogui.scroll(scroll_speed)
        time.sleep(sleep_time)

        scroll_times -= 1


def close():
    """
    模拟关闭阅读，循环是为了防止坐标不准确导致没关掉
    :return:
    """

    try:
        close_location = pyautogui.locateOnScreen(close_path, confidence=confidence)
        while close_location:
            # 计算图像中心点
            center = pyautogui.center(close_location)
            pyautogui.click(center)
            print(f"close-Clicked on {center}")
            time.sleep(sleep_time)

            close_location = pyautogui.locateOnScreen(close_path, confidence=confidence)

    except pyautogui.FailSafeException:
        print("close not found")
        return


def do_read(x, y):
    """
    模拟点击“阅读更多”
    :param x:
    :param y: 赞同上方50像素位置点击即可查看全文
    :return:
    """
    # 在屏幕上查找阅读全文图像
    if not listener_esc:
        # 点击查看全文
        pyautogui.click(x, y)
        print(f"Read more-Clicked on {x}, {y}")

        # 加载内容
        time.sleep(sleep_time)

        # 阅读
        reading()


def do_click():
    """
    模拟点赞
    :return:
    """

    # 给自己一些时间准备切换到目标应用窗口

    # 检查是否按下了ESC键，如果是，则退出循环
    while not listener_esc:
        time.sleep(sleep_time)

        try:
            # 在屏幕上查找赞同图像，可以调整confidence参数以适应图像匹配的准确性要求
            agree_location = pyautogui.locateOnScreen(agree_path, confidence=confidence)

            if agree_location:
                # 计算图像中心点
                center = pyautogui.center(agree_location)
                x, y = center

                # 模拟阅读
                do_read(x, y - 50)

                # 点赞
                if not listener_esc:
                    # pyautogui.click(x, y)  # 防止坐标因移动而造成的偏差，重新获取赞同坐标
                    agree_location = pyautogui.locateOnScreen(agree_path, confidence=confidence)
                    center = pyautogui.center(agree_location)
                    pyautogui.click(center)
                    print(f"Agree - Clicked on {center}")

                    # 点击关闭按钮
                    close()

        except pyautogui.ImageNotFoundException:
            print("agree not found. Trying again...")

            # 短暂暂停，以便循环不会过于频繁地执行
            time.sleep(sleep_time)

        # 向下滚动，大概向下滚动200像素行
        for _ in range(int(200 / scroll_speed)):
            pyautogui.scroll(-scroll_speed)

    print("Exited.")


# 创建并启动线程监听ESC键
listener_thread1 = threading.Thread(target=start_listener)
listener_thread1.start()

# 这里的代码可以在不被阻塞的情况下执行
print("Like mode begin...")
do_click()
print("Like mode end...")
