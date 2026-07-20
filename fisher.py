"""
Palworld Auto-Fisher  (share edition)
-------------------------------------
Plays the Palworld fishing catch minigame for you by watching the screen
and moving the block to keep it on the fish. No cheats, no game files
touched -- it just looks at the screen and clicks, like a macro.

CONTROLS (shown on screen too):
    Double-tap Q  ->  start / pause fishing
    F8            ->  quit

Must run as administrator (the launcher handles that for you).
"""

import time
import mss
import numpy as np
from pynput import mouse, keyboard

# --- Where the fishing bar sits on screen (fractions, so any resolution) ---
X_LEFT_FRAC = 0.25
X_RIGHT_FRAC = 0.75
Y_TOP_FRAC = 0.28
Y_BOT_FRAC = 0.37

# --- Behaviour ---
DEADZONE = 30            # how close to center is "good enough" (bigger = calmer)
LOOP_DELAY = 0.03        # how often it checks the screen
MAX_RUNTIME = 3600       # auto-stop after 60 min as a safety net
HOLD_MOVES_RIGHT = True  # does holding the mouse move the block right? flip if not

# --- How it recognizes things by colour ---
STRONG_GREEN = 60        # a pixel is "block green" if green beats red & blue by this
MIN_GREEN_ROWS = 8       # a column needs this many green pixels to count as block
GAP_TOLERANCE = 20       # bridge small gaps within the block

# --- Keys ---
TOGGLE_CHAR = "q"
QUIT_KEY = keyboard.Key.f8
DOUBLE_TAP_WINDOW = 0.4


def find_positions(arr):
    """Find the green block (edges + center) and the yellow fish line."""
    b = arr[:, :, 0].astype(int)
    g = arr[:, :, 1].astype(int)
    r = arr[:, :, 2].astype(int)

    strong = (g - np.maximum(r, b)) > STRONG_GREEN
    col_strong = strong.sum(axis=0)
    block_cols = col_strong > MIN_GREEN_ROWS

    runs = []
    start = None
    end = 0
    gap = 0
    for x in range(len(block_cols)):
        if block_cols[x]:
            if start is None:
                start = x
            end = x
            gap = 0
        elif start is not None:
            gap += 1
            if gap > GAP_TOLERANCE:
                runs.append((start, end))
                start = None
    if start is not None:
        runs.append((start, end))

    if runs:
        block_left, block_right = max(runs, key=lambda t: t[1] - t[0])
        block_center = (block_left + block_right) // 2
    else:
        block_center = None

    yellowness = np.clip(np.minimum(r, g) - b, 0, None)
    col_yellow = yellowness.sum(axis=0)
    fish_x = int(col_yellow.argmax()) if col_yellow.max() > 400 else None
    return block_center, fish_x


# --- Mouse control ---
mouse_ctl = mouse.Controller()
holding = False
running = True
armed = False
last_toggle_tap = 0.0


def press_mouse():
    global holding
    if not holding:
        mouse_ctl.press(mouse.Button.left)
        holding = True


def release_mouse():
    global holding
    if holding:
        mouse_ctl.release(mouse.Button.left)
        holding = False


def move_block_right():
    press_mouse() if HOLD_MOVES_RIGHT else release_mouse()


def move_block_left():
    release_mouse() if HOLD_MOVES_RIGHT else press_mouse()


def is_toggle_key(key):
    if key == keyboard.Key.f7:
        return True
    ch = getattr(key, "char", None)
    return ch is not None and ch.lower() == TOGGLE_CHAR


def on_press(key):
    global running, armed, last_toggle_tap
    if key == QUIT_KEY:
        running = False
        return False
    if is_toggle_key(key):
        now = time.time()
        if now - last_toggle_tap < DOUBLE_TAP_WINDOW:
            armed = not armed
            last_toggle_tap = 0.0
            print("\n>>> FISHING <<<  (double-tap Q to pause)" if armed
                  else "\n>>> PAUSED <<<  (double-tap Q to fish again)")
        else:
            last_toggle_tap = now


def main():
    global running
    sct = mss.mss()
    mon = sct.monitors[1]
    W, H = mon["width"], mon["height"]
    roi = {
        "left": mon["left"] + int(W * X_LEFT_FRAC),
        "top": mon["top"] + int(H * Y_TOP_FRAC),
        "width": int(W * (X_RIGHT_FRAC - X_LEFT_FRAC)),
        "height": int(H * (Y_BOT_FRAC - Y_TOP_FRAC)),
    }

    print("=" * 50)
    print("            PALWORLD  AUTO-FISHER")
    print("=" * 50)
    print(" HOW TO USE:")
    print("   1. Go into Palworld and cast your line.")
    print("   2. When the catch bar shows up, DOUBLE-TAP  Q")
    print("   3. Watch it play! DOUBLE-TAP  Q  again to pause.")
    print("   4. Press  F8  to quit.")
    print()
    print(" Keep this window open while you fish. Good luck!")
    print("=" * 50)
    print("\nReady and waiting -- double-tap Q when the bar appears...")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    end = time.time() + MAX_RUNTIME
    try:
        while running and time.time() < end:
            if not armed:
                release_mouse()
                time.sleep(0.05)
                continue

            arr = np.array(sct.grab(roi))
            block_center, fish_x = find_positions(arr)

            if block_center is not None and fish_x is not None:
                if fish_x > block_center + DEADZONE:
                    move_block_right()
                elif fish_x < block_center - DEADZONE:
                    move_block_left()
                else:
                    # centered -> pulse to hover in place (smooth)
                    release_mouse() if holding else press_mouse()
            else:
                release_mouse()

            time.sleep(LOOP_DELAY)
    finally:
        release_mouse()
        listener.stop()
        print("\nStopped. Happy fishing!")


if __name__ == "__main__":
    main()
