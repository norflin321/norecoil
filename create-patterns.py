# -*- coding: utf-8 -*-

import time
import win32api
import win32con
import winsound
import json
import sys


LMB = win32con.VK_LBUTTON
F4 = win32con.VK_F4
F10 = win32con.VK_F10


def beep():
  winsound.Beep(2000, 100)


def beep_exit():
  winsound.Beep(500, 500)


def main(weapon_name):
  running = True
  reading_clicks = False
  prev_x = 0
  prev_y = 0
  new_pattern = []
  while running:
    if win32api.GetAsyncKeyState(F4):
      reading_clicks = not reading_clicks
      print("Reading clicks: {}".format(reading_clicks))
      time.sleep(0.2)

    if win32api.GetAsyncKeyState(F10):
      running = not running
      time.sleep(0.2)

    if win32api.GetAsyncKeyState(LMB) < 0 and reading_clicks:
      beep()
      now_pos = win32api.GetCursorPos()
      if prev_x == 0 and prev_y == 0:
        prev_x = now_pos[0]
        prev_y = now_pos[1]
        moved_x = 0
        moved_y = 0
      else:
        moved_x = int((now_pos[0]-prev_x+1)/2)  # div by 2 round up => real pattern
        moved_y = int((now_pos[1]-prev_y+1)/2)  # because you should click x2 zoomed pattern
        prev_x = now_pos[0]
        prev_y = now_pos[1]

      new_pattern.append([moved_x, moved_y])
      time.sleep(0.15)
    time.sleep(0.1)

  print("new pattern:", new_pattern)
  with open("./patterns/{}.json".format(weapon_name), 'w', encoding='utf-8') as f:
    json.dump(new_pattern, f)

if __name__ == "__main__":
  print("Open image with recoil pattern, zoom x2, activate, click bullet-prints, ..., PROFIT!?")
  print("F4 - Activate/deactivate tracking!")
  print("F10 - Exit!")
  print("Make pattern by clicking bullet-prints one at a time...")
  main(sys.argv[1])
  beep_exit()
