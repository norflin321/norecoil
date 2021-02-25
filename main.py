# -*- coding: utf-8 -*-
import time
import win32api
import win32con
import ctypes
import json
import sys

# weapons fire speed
WEAPONS_RPMS = {
  "havoc": 672,
  "flatline": 600,
  "r-301": 810,
  "alternator": 600,
  "r-99": 1080,
  "volt": 720,
  "spitfire": 540,
}

# for cursor detector
class POINT(ctypes.Structure):
  _fields_ = [('x', ctypes.c_int), ('y', ctypes.c_int)]
class CURSORINFO(ctypes.Structure):
  _fields_ = [('cbSize', ctypes.c_uint),
              ('flags', ctypes.c_uint),
              ('hCursor', ctypes.c_void_p),
              ('ptScreenPos', POINT)]

# move mouse
def mouse_move_relative(dx, dy):
  win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)

# get weapon fire rate
def get_tick(rpm):
  rps = rpm/60
  mstick = 1000.0/rps
  stick = round(mstick/1000, 3)
  return stick

# process no recoil
def process_no_recoil(pattern, rpm):
  shot_tick = get_tick(rpm)
  shot_index = 0
  while is_lmb_pressed():
    if shot_index < len(pattern) - 1:
      dx = -pattern[shot_index][0]
      dy = -pattern[shot_index][1]
      mouse_move_relative(dx, dy)
      time.sleep(shot_tick)
      shot_index += 1

#  check if left mouse button pressed
def is_lmb_pressed():
  return win32api.GetKeyState(win32con.VK_LBUTTON) < 0

#  detect cursor idk what is it
def cursor_detector():
  GetCursorInfo = ctypes.windll.user32.GetCursorInfo
  GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
  info = CURSORINFO()
  info.cbSize = ctypes.sizeof(info)
  if GetCursorInfo(ctypes.byref(info)):
    if info.flags & 0x00000001:
      return True
    else:
      return False
  else:
    print("cursor detector err")

def main():
  with open('./patterns/{}.json'.format(sys.argv[1])) as file:
    pattern = json.load(file)
    rpm = WEAPONS_RPMS[sys.argv[1]]
    while True:
      if is_lmb_pressed() and not cursor_detector():
        process_no_recoil(pattern, rpm)
        time.sleep(0.01)

if __name__ == "__main__":
  main()

#[[0, 0], [-2, -19], [-1, -8], [-8, -11], [-2, -9], [-3, -10], [-1, -11], [4, -4], [9, 4], [4, -4], [3, -6], [-2, -1], [-10, -7], [-5, 1], [-6, 2], [-5, 1], [-1, -9], [-1, -7], [-1, -7], [-8, 0], [3, -7], [7, -2], [6, -1], [6, 0], [9, -2], [5, 5], [5, -4], [2, -5], [-3, -4], [8, 1], [4, 3], [2, -4], [4, -8]]
