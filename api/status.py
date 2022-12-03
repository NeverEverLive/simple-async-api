import json

from aiohttp import web

async def health(request):
    response_data = {"status": "success"}
    return web.Response(
        body=json.dumps(response_data), 
        content_type="application/json",
        status=200
    )
