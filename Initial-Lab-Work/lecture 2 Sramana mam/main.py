"""
Runs all the practice scripts in sequence.

Each script exposes a run() function; this calls them one at a time and
catches failures so one broken site doesn't stop the rest. Also wires in
scroll_click_About, which the original main.py never imported (its source
file was named "scroll&click_About.py" - the '&' makes it un-importable).
"""

import copy_msg
import drag_and_drop
import keyboard_actions
import popup
import scroll_click_About
import select_mobiles

TESTS = [
    ("copy_msg", copy_msg.run),
    ("drag_and_drop", drag_and_drop.run),
    ("keyboard_actions", keyboard_actions.run),
    ("popup", popup.run),
    ("scroll_click_About", scroll_click_About.run),
    ("select_mobiles", select_mobiles.run),
]


def main(headless: bool = False) -> None:
    results = {}
    for name, fn in TESTS:
        print(f"\n=== Running {name} ===")
        try:
            fn(headless=headless)
            results[name] = "PASSED"
        except Exception as exc:
            results[name] = f"FAILED: {exc}"
            print(f"{name} failed: {exc}")

    print("\n=== Summary ===")
    for name, status in results.items():
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
