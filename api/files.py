import asyncio
import json
import time
from pathlib import Path

import aiohttp
import aiofiles
from aiohttp import web

from validators import Validator


async def fetch_content(url: str, session: aiohttp.ClientSession):
    async with session.get(url, allow_redirects=True) as response:
        file_name = f"files/{int(time.time() * 10000)}{str(response.url).split('/')[-1]}"
        data = await response.read()
        await write_file(file_name, data)


async def write_file(file_name: str, data: bytes):
    if Path(file_name).exists():
        print(f"{file_name}file already exist")
        return
    async with aiofiles.open(file_name, 'wb') as file:
        await file.write(data)


def track_time(start_time: float):
        return round(time.time() - start_time, 2)


async def download_files(request: web.Request):
    if not request.body_exists:
        return web.Response(
            body=json.dumps({
                "message": "You're need to send some URL"
            }),
            content_type="application/json",
            status=400
        )
    try:
        url = (await request.json())["url"]
        number_of_task = (await request.json())["files_count"]
    except KeyError:
        return web.Response(
            body=json.dumps({
                "message": "You're need to send some URL and files count"
            }),
            content_type="application/json",
            status=400
        )

    if not Validator.validate_url(url):
        return web.Response(
            body=json.dumps({
                "message": "Invalid URL"
            }),
            content_type="application/json",
            status=400
        )

    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_content(url, session)) for _ in range(number_of_task)]
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as error:
            with open("error.txt", "a+") as file:
                file.write(str(error))

    end_time = track_time(start_time)

    return web.Response(
        body=json.dumps({
            "message": "It's cool", 
            "url": url, 
            "execution_time": end_time
        }),
        content_type="application/json",
        status=200
    )
