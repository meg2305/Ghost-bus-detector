import aiohttp
import asyncio
import logging
from app.config import GTFS_FEED_URL, FETCH_INTERVAL

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GTFSFetcher:
    def __init__(self, feed_url: str = GTFS_FEED_URL, interval: int = FETCH_INTERVAL):
        """
                A class responsible for fetching GTFS-Realtime feeds continuously.

                Args:
                    feed_url (str): URL of the GTFS-Realtime protobuf feed.
                    interval (int): Interval (in seconds) between fetches.
                """
        self.feed_url = feed_url
        self.interval = interval
        self.session = None  # aiohttp session, initialized in start()

    async def start(self, callback):
        """
        Start the infinite loop to fetch GTFS feed periodically.

        Args:
            callback (function): A coroutine function that will receive the raw
                                 protobuf feed data after each successful fetch.
        """
        async with aiohttp.ClientSession() as self.session:
            while True:
                try:
                    # Try to fetch GTFS feed
                    data = await self.fetch_feed()
                    if data:
                        # Pass raw data to the callback (parser, detector, etc.)
                        await callback(data)  # hand off to parser/detector
                except Exception as e:
                    # Log errors instead of crashing
                    logger.error(f"Error fetching GTFS feed: {e}")

                # Wait before fetching again
                await asyncio.sleep(self.interval)

    async def fetch_feed(self) -> bytes:
        """
        Fetches the GTFS-Realtime feed once.

        Returns:
            bytes: Raw protobuf feed data, or None if fetch failed.
        """
        async with self.session.get(self.feed_url) as response:
            if response.status == 200:
                logger.info("Successfully fetched GTFS feed")
                return await response.read()
            else:
                logger.warning(f"Failed to fetch GTFS feed: {response.status}")
                return None
