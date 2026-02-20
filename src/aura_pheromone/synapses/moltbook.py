import os
import httpx
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

class MoltbookClient:
    def __init__(self):
        self.api_url = "https://moltbook.zae.life/api/v1"
        self.api_key = os.environ.get("MOLTBOOK_API_KEY")
        self.identity_token: Optional[str] = None
        self.token_expiry: float = 0

    async def get_identity_token(self) -> Optional[str]:
        """
        Step 1 & 2: Activation and Expression.
        Fetches a 1-hour identity token using the API key.
        """
        if not self.api_key:
            logger.error("MOLTBOOK_API_KEY not set.")
            return None

        # Metabolic Refresh check
        if self.identity_token and time.time() < self.token_expiry - 60:
            return self.identity_token

        logger.info("🧬 [Moltbook Client] Refreshing Identity Token...")
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_url}/me/identity-token", headers=headers)
                response.raise_for_status()
                data = response.json()
                self.identity_token = data.get("identity_token")
                # Tokens live for 1 hour as per SSA
                self.token_expiry = time.time() + 3600
                logger.info("Identity token successfully expressed.")
                return self.identity_token
        except Exception as e:
            logger.error(f"Failed to fetch identity token: {e}")
            return None

    async def emit_pheromone(self, content: str):
        """
        Step 3: Signaling.
        Uses the identity token to post to the lablab submolt.
        """
        token = await self.get_identity_token()
        if not token:
            logger.error("No valid identity token available. Signaling aborted.")
            return False

        headers = {
            "X-Moltbook-Identity": token,
            "Content-Type": "application/json"
        }

        payload = {
            "content": content,
            "origin": "bee.savant"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api_url}/submolt/lablab/post", json=payload, headers=headers)
                response.raise_for_status()
                logger.info("Pheromone successfully signaled to lablab submolt.")
                return True
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during signaling: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during signaling: {e}")
            return False
