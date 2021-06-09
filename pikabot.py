from pikabot.bot import Bot
from pikabot.config import Config
import os
import sys
import logging
import asyncio

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Init logging
    logging.basicConfig(
        filename="pikabot.log",
        format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
        level=logging.INFO
    )

    # Create a default config file if it does not exist
    config = Config()
    if os.path.exists("config/config.toml"):
        config.load_append("config/config.toml")
    else:
        config.append({
            "bot": {
                "token": "",
                "prefix": "."
            }
        })
        if not os.path.exists("config"):
            os.mkdir("config")
        config.save("config/config.toml")

        print("Created default config. Please edit config/config.toml and start bot again")
        sys.exit(1)

    bot = Bot(config)

    app_coroutines = [
        bot.run()
    ]

    app_tasks = [asyncio.Task(c) for c in app_coroutines]

    async def cancel():
        for task in app_tasks:
            try:
                task.cancel()
                await task
            except asyncio.CancelledError:
                pass

    loop = asyncio.get_event_loop()
    try:
        logger.info("Starting asyncio loop")
        loop.run_until_complete(asyncio.gather(*app_tasks))
    except KeyboardInterrupt as e:
        logger.info("Caught KeyboardInterrupt, cancelling tasks")
        loop.run_until_complete(cancel())
    except Exception as e:
        logger.exception(f"Caught exception {e}")
        loop.run_until_complete(cancel())
    finally:
        logger.info("Exiting application")
        loop.close()
