# 🎣 Palworld Auto-Fisher

A tiny program that plays Palworld's fishing catch minigame for you. It just
**watches your screen and moves the mouse** — like a macro. It does **not**
change the game or any files. **Single-player only.**

## ⬇️ Get it
Click the green **Code** button → **Download ZIP**, then unzip it anywhere.

## 🛠️ First time (once)
Double-click **`1_SETUP.bat`**. It installs everything automatically
(Python if you don't have it, plus the bits the fisher needs). When it says
**"All set!"**, you're done.

> If it says Python isn't installed, let it install Python, then **close the
> window and run `1_SETUP.bat` again**. (Or grab Python from
> [python.org](https://www.python.org/downloads/) and tick *"Add Python to PATH"*.)

## ▶️ Every time you want to fish
1. Open **Palworld** (Windowed or Borderless mode works best).
2. Double-click **`2_PLAY.bat`** → click **Yes** if Windows asks.
3. In-game, cast and hook a fish.
4. When the catch bar appears, **double-tap `X`** → it takes over!
5. **Double-tap `X`** again to pause. Press **`F8`** to quit.

## ⚠️ If Windows warns you
Because it moves the mouse, Windows Defender / SmartScreen may show a warning.
It's a false alarm. On *"Windows protected your PC"* click **More info → Run anyway**.

## 🔧 If it doesn't catch well
- Use **Windowed / Borderless** mode on a normal **16:9** monitor.
- If the block moves the **wrong way**, open `fisher.py` in Notepad, change
  `HOLD_MOVES_RIGHT = True` to `HOLD_MOVES_RIGHT = False`, save, and play again.

---
*Made for fun — for single-player Palworld only.*
