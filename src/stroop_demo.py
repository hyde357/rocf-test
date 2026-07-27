# 示例：Stroop 实验
from psychopy import visual, core, event
import random

win = visual.Window(fullscr=False, size=[1024, 768], color=[0, 0, 0], units="height")

colors = ["red", "blue", "green", "yellow"]
words = ["红", "蓝", "绿", "黄"]

instructions = visual.TextStim(win, text="按颜色按键:\nR=红 B=蓝 G=绿 Y=黄\n按空格开始", height=0.06)
instructions.draw()
win.flip()
event.waitKeys(keyList=["space"])

for _ in range(20):
    color_name = random.choice(colors)
    word = random.choice(words)
    
    stim = visual.TextStim(win, text=word, color=color_name, height=0.1)
    stim.draw()
    win.flip()
    
    keys = event.waitKeys(keyList=["r", "b", "g", "y", "escape"])
    if "escape" in keys:
        win.close()
        core.quit()

win.close()
core.quit()
