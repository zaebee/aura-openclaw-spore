import os
import httpx
import logging

logger = logging.getLogger(__name__)

class MoltbookEffector:
    def __init__(self):
        self.api_url = "https://moltbook.zae.life/api/v1/submolt/lablab/post"
        self.token = os.environ.get("MOLTBOOK_TOKEN")

    async def emit_pheromone(self, content: str):
        if not self.token:
            logger.error("MOLTBOOK_TOKEN not set. Cannot emit pheromone.")
            return False

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "content": content,
            "origin": "bee.savant"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                logger.info("Pheromone successfully emitted to lablab submolt.")
                return True
        except httpx.HTTPError as e:
            logger.error(f"HTTP error failed to emit pheromone: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error failed to emit pheromone: {e}")
            return False
