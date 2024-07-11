from asyncio import sleep
from random import uniform
import asyncio
import aiohttp
from aiocfscrape import CloudflareScraper
from .agents import generate_random_user_agent

from data import config
from utils.duck import Duckbot
from utils.core import logger
from utils.helper import format_duration
from datetime import datetime


async def start(thread: int, account: str, proxy: [str, None]):
    while True:
         
        async with aiohttp.ClientSession(headers={'User-Agent': generate_random_user_agent(device_type='android',
                                                                                            browser_type='chrome')},
                                        timeout=aiohttp.ClientTimeout(total=60)) as session:
            useragent= generate_random_user_agent(device_type='android',browser_type='chrome')
            try:                                     
                Duck = Duckbot(account=account, thread=thread, session=session, proxy=proxy, useragent=useragent)
                await asyncio.sleep(uniform(*config.DELAYS['ACCOUNT']))
                max_try = 2
                await Duck.login()
                
                
                while True:
                    try:
                        timestamp = datetime.timestamp(datetime.now())
                        start_time, end_time, balance, state, end_dt= await Duck.time()
                        if start_time is None and end_time is None and max_try > 0 and state == "notStarted":
                            await Duck.start()
                            logger.info(f"{account} | Start farming!")
                            max_try -= 1
                            await sleep(5)

                        if (start_time is not None and end_time is not None and timestamp is not None and 
                                  timestamp >= end_time and max_try > 0):
                            claim = await Duck.claim()
                            logger.success(f"{account} | Claimed reward! Balance: {balance}")
                            max_try -= 1
                            await sleep(5)

                        if state == "inProgress":
                            sleep_duration = end_dt - timestamp
                            logger.info(f"{account} | Sleep {format_duration(sleep_duration)}")
                            max_try += 1
                            await sleep(sleep_duration)
                            

                        elif max_try == 0:
                            break
                    except Exception as e:
                                 logger.error(f"{account} | Error in farming management: {e}")
            except Exception as outer_e:
                logger.error(f"{account} | Session error: {outer_e}")
            finally:
                logger.info(f"{account} | Reconnecting, 61 s")
                await sleep(61)
