import config  # noqa: F401 (Needed for logging setup)
from app.ui import GUI


def main():
    root = GUI().create_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
