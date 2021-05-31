
from api.endpoints import app
from config.config import isDevelopment


def main():
    if isDevelopment:
        app.run(debug=True)
    pass


if __name__ == '__main__':
    main()
