import sys
from console.main_console import run_console
from gui.main_gui import App

if __name__ == "__main__":
    if "gui" in sys.argv:
        App().run()
    else:
        run_console()
