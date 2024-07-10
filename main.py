from utils.core import create_sessions, logger
from utils.telegram import Accounts
from utils.starter import start
import asyncio
from itertools import zip_longest
#from utils.core import get_all_lines
import os
import argparse
from data import config


async def main():
    print("amir")

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=int, help='Action to perform')
    action = parser.parse_args().action

    if not os.path.exists('sessions'):
        os.mkdir('sessions')
    if not os.path.exists('statistics'):
        os.mkdir('statistics')

    if not action:
        action = int(input("Select action:\n1. Start soft\n2. Create pyrogram sessions\n\n> "))

    if action == 2:
        await create_sessions()

    if action == 1:
        try:
            accounts = await Accounts().get_accounts()

            if config.PROXY is True:
                proxys = get_all_lines("data/proxy.txt")
            else:
                proxys = ""

            tasks = []
            for thread, (account, proxy) in enumerate(zip_longest(accounts, proxys)):
                if not account:
                    break
                tasks.append(asyncio.create_task(start(account=account, thread=thread, proxy=proxy)))

            await asyncio.gather(*tasks)
        except ValueError as error:
            logger.error('I guess there ain`t any sessions, please add one by typing 2 in this CMD next start')
            logger.error('If you think that sessions are valid, below is error, please send it in telegram chat')
            logger.error(error)

if __name__ == '__main__':
    print("""
   @sudo_amirh """)
    asyncio.run(main())
