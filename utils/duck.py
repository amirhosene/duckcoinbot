import random
from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestWebView
import asyncio, aiohttp
from urllib.parse import unquote
from data import config
import datetime

class Duckbot:
    def __init__(self, thread, account, session, proxy):
        self.proxy - f"http://{proxy}" if proxy is not None else None
        self.thread = thread
        
        if proxy:
            proxy = proxy.split(":")
            proxy = {
                "scheme": "http",
                "hostname": parts[0] if len(parts) == 2 else parts[1].split('@')[1],
                "port": int(parts[2]) if len(parts) == 3 else int(parts[1]),
                "username": parts[0] if len(parts) == 3 else "",
                "password": parts[1].split('@')[0] if len(parts) == 3 else ""
            }

        self.client = Client(name= account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR, proxy=proxy)
        self.session = session
    async def logout(self):
        """
        Logout by closing the aiohttp session.
        """
        await self.session.close()
    async def login(self):
        try:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 'task.duckdns.pro',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
                       }
            response = await self.session.get('https://task.duckdns.pro/', headers=headers)
            status = response.status
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/json' in content_type:
                data = await response.json()
            else:
                data = await response.text()
            return status, content_type, data
        except Exception as e:
            print(e)



    async def time(self):
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': await self.get_tg_web_data(),
                'Connection': 'keep-alive',
                'Host': 'api.duckcoingame.duckdns.org',
                'Origin': 'https://task.duckdns.pro',
                'Referer': 'https://task.duckdns.pro/',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
            }

            response = await self.session.get('https://api.duckcoingame.duckdns.org/v1/api/game/time', headers=headers)
            res_json = await response.json()

            balance = res_json.get("experience")

            start_time = None
            end_time = None
            en = res_json.get('end')
            state = res_json.get("state")
            end_dt = datetime.datetime.fromisoformat(en[:-1])
            end_dt = end_dt.timestamp()
            if res_json.get("state") == "completed":
                start = res_json.get('start')
                end = res_json.get('end')
                
                start_dt = datetime.datetime.fromisoformat(start[:-1])
                end_dt = datetime.datetime.fromisoformat(end[:-1])

                start_time = start_dt.timestamp()
                end_time = end_dt.timestamp()

            return start_time, end_time, balance, state, end_dt

        except Exception as e:
            print(f"Error occurred: {e}")   
    
    async def claim(self):
        """
        Claim the farming rewards.
        """ 
        try:
            
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': await self.get_tg_web_data(),
                'Connection': 'keep-alive',
                'Host': 'api.duckcoingame.duckdns.org',
                'Origin': 'https://task.duckdns.pro',
                'Referer': 'https://task.duckdns.pro/',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
                'Content-Type': 'application/json; charset=utf-8'
            }
            response = await self.session.post('https://api.duckcoingame.duckdns.org/v1/api/game/claim', headers=headers)
            status = response.status
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/json' in content_type:
                data = await response.json()
            else:
                data = await response.text()
            return status, content_type, data
        except Exception as e:
            print(e)

    async def start(self):
        """
        start farming
        """
        try:
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en-US,en;q=0.9',
                'Authorization': await self.get_tg_web_data(),
                'Connection': 'keep-alive',
                'Content-Length': '0',
                'Host': 'api.duckcoingame.duckdns.org',
                'Origin': 'https://task.duckdns.pro',
                'Referer': 'https://task.duckdns.pro/',
                'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
            }
            response = await self.session.post('https://api.duckcoingame.duckdns.org/v1/api/game/farm', headers=headers)
            status = response.status
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/json' in content_type:
                data = await response.json()
            else:
                data = await response.text()
            return status, content_type, data
        except Exception as e:
            print(e)

    async def get_tg_web_data(self):
        """
        Get the Telegram web data needed for login.
        """
        await self.client.connect()

        web_view = await self.client.invoke(RequestWebView(
            peer=await self.client.resolve_peer('DuckTask_bot'),
            bot=await self.client.resolve_peer('DuckTask_bot'),
            platform='android',
            from_bot_menu=False,
            url='https://task.duckdns.pro/'
        ))

        auth_url = web_view.url
        await self.client.disconnect()
        #print(auth_url)
        return unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
        