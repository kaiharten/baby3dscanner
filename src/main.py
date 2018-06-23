import sys
from babyscanner import BabyScannerApp

def main():
    app = BabyScannerApp()
    try:
        app.userinterface.mainloop()

    except:
        app.cam.stop()
        quit()

if __name__ == "__main__":
    main()