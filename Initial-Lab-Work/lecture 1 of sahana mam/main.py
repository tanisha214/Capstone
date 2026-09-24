"""
Runs all the practice scripts in sequence.

The original main.py just did `import automate`, `import checkbox`, etc.
That "worked" only because each module ran its Selenium code as a top-level
side effect of being imported - which is fragile (no error isolation: one
script crashing kills the whole run, can't re-run a single script cleanly,
and every import opens its own browser with no shared setup). Now each
script exposes a `run()` function and this file calls them one at a time,
catching failures so one broken site doesn't stop the rest.
"""

import automate
import checkbox
import dropdown
import germanyclicking
import listofelements
import radiobutton
import test
import webdrivermanager

TESTS = [
    ("automate", automate.run),
    ("checkbox", checkbox.run),
    ("dropdown", dropdown.run),
    ("germanyclicking", germanyclicking.run),
    ("listofelements", listofelements.run),
    ("radiobutton", radiobutton.run),
    ("test", test.run),
    ("webdrivermanager", webdrivermanager.run),
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
