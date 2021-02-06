from itertools import groupby

import cv2
import numpy as np

from rcon import MCRcon
from block_setter import block_setter  # generate coords and set repeaters in serpentine form (compact as possible)


def main():
    # google: minecraft rcon
    with MCRcon("ip", 'password') as rcon:

        # the only way to choose world - use execute at (maybe)
        # you also can add logging here, use rcon.command() to receive response
        command_func = lambda cmd: rcon.command_wo_res(f"execute at svinerus run {cmd}")

        block_coords = block_setter(start_pos=(0, 1, 0), size=(125, 125), command_func=command_func)

        for frame in proccess_video('badapple.mp4'):
            cmds = list(proccess_frame(frame))
            coords = next(block_coords)
            set_cmd_blocks(cmds, coords, command_func=command_func)


def proccess_video(videoname):
    SIZE = 1/8

    vidcap = cv2.VideoCapture(videoname)
    count = 0
    while True:
        success, frame = vidcap.read()
        if not success:
            break
        if count > 50:  # skip first 50 frames
            frame = cv2.resize(frame, (0, 0), fx=SIZE, fy=SIZE)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = frame // 128  # 0-255//128 = 0-1 range
            yield frame
        count += 1
        print(count)


old_image = None
def proccess_frame(image):
    def group_row(row):  # optimize: group row to use fill instead of setblock
        last = 0
        res = []  # value, start, stop
        for color, items in groupby(list(row)):
            res.append((color, last, last := last + len(list(items))))
        return res

    global old_image
    if old_image is None:
        old_image = np.zeros(image.shape)

    for y, row in enumerate(image):
        row_groupped = group_row(row)
        for g in row_groupped:
            if not set(old_image[y, g[1]:g[2]]) == {g[0]}:
                y_ = image.shape[0] - y  # draw from bottom pivot
                yield g[0], g[1], g[2], y_  # value, z_start, z_stop, y
    old_image = image


def set_cmd_blocks(cmds, coords, command_func):
    def fillrow(value, z1, z2, y):
        block = ('black_wool', 'white_wool')[value]
        return f"execute at @e[name=bad_apple] run fill ~1 ~{y} ~{z1} ~1 ~{y} ~{z2} minecraft:{block}"

    cmds = [fillrow(*cmd) for cmd in cmds] or [""]
    x, y0, z = coords

    # vertical bunch of cmd blocks
    command_func(f'setblock {x} {y0} {z} minecraft:command_block[facing=up]{{Command:"{cmds[0]}"}}')
    for cmd, y in zip(cmds[1:], range(y0 + 1, 256)):
        command_func(f'setblock {x} {y} {z} minecraft:chain_command_block[facing=up]{{Command:"{cmd}",auto:1}}')


main()
