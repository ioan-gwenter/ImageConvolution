"""
main.py

Entry point for the application. Instantiates the UI and runs the main loop.
"""

from ui import MainApplication


def main() -> None:
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()
