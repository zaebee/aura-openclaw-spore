import os
import logging
import httpx
from typing import Any, Dict
from aura_worker import Umbilical, WorkerController, VisionSkill

logger = logging.getLogger(__name__)

class VisionCortex:
    def __init__(self):
        self.controller = WorkerController()
        self.skill = None
        self._initialized = False

    async def initialize(self):
        punk_key = os.environ.get("AURA_WORKER__PUNK_KEY")
        if not punk_key:
            raise ValueError("AURA_WORKER__PUNK_KEY environment variable is not set")

        frp_token = os.environ.get("AURA_WORKER__FRP_TOKEN")
        if not frp_token:
            raise ValueError("AURA_WORKER__FRP_TOKEN environment variable is not set")

        self.controller.umbilical = Umbilical(
            hive_host="aura.zae.life",
            frp_token=frp_token,
            punk_key=punk_key,
            worker_id="colab-savant"
        )

        # In this implementation, we'll assume the controller handles the connection
        self.skill = VisionSkill(model_name="gemma3")
        self._initialized = True
        logger.info("VisionCortex initialized and connected to Savant node.")

    async def ping(self) -> Dict[str, Any]:
        """
        Hardened Verification Protocol:
        1. Check if the frpc subprocess is in a Running state.
        2. Perform a fast GET http://localhost:11434/api/tags via the tunnel.
        3. Return a SystemVitals object with status: VITALS_STATUS_OK.
        """
        if not self._initialized:
            await self.initialize()

        # 1. Check frpc status
        if not self.controller.umbilical or not self.controller.umbilical.is_alive:
            logger.error("Umbilical/frpc is not alive.")
            return {"status": "VITALS_STATUS_ERROR", "error": "Umbilical dead"}

        # 2. Heartbeat check to Ollama via tunnel
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("http://localhost:11434/api/tags")
                response.raise_for_status()
        except Exception as e:
            logger.error(f"Heartbeat failed: {e}")
            return {"status": "VITALS_STATUS_ERROR", "error": str(e)}

        return {"status": "VITALS_STATUS_OK"}

    async def ensure_active(self):
        vitals = await self.ping()
        if vitals["status"] != "VITALS_STATUS_OK":
             raise ConnectionError(f"VisionCortex inactive: {vitals.get('error')}")
        return True

    async def verify_asset(self, image_data: bytes | str):
        await self.ensure_active()

        # The VisionSkill in aura-worker uses 'generate' method
        # We wrap it to match the perception needs
        result = await self.skill.generate([image_data])

        if "error" in result:
             raise ValueError(f"Vision perception failed: {result['error']}")

        return result
