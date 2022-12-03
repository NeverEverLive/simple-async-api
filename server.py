from aiohttp import web
from app import init


if __name__ == "__main__":
    app = init()
    web.run_app(app, port=5001)