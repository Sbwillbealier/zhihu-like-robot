# zhihu-like-robot

模拟鼠标给知乎点赞，仅供学习~

# 演示视频

<video src="https://coderjia-1254377750.cos.ap-shanghai.myqcloud.com/blog/202402032303833.mp4" controls>
  你的浏览器不支持 <code>video</code> 标签。
</video>

# 依赖

```commandline
pip intall pyautogui
pip install pynput
pip install opencv-python
```

- pyautogui：作用是模拟鼠标的点击和滚动；
- pynput：作用是模拟键盘的输入，捕获退出按钮
- opencv-python：作用是图标识别；

# 注意

1. 像素坐标是左上角坐标，不是中心坐标；
2. 点赞按钮和关闭按钮截图要清晰，截图时网页缩放大小最好和程序运行时一致；
3. 为了防止被知乎官方检测到，建议把休息时间调长点，时间调为随机；
4. 本项目仅供学习，切勿作恶。