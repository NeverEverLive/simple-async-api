from aiohttp import web

from api import status, files

async def init():
    app = web.Application()
    app.router.add_get("/api/v1/", status.health)
    app.router.add_post("/api/v1/files", files.download_files)

    return app
