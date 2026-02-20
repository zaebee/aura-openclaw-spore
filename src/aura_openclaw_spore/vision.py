import os
import logging
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

        # In a real scenario, we might need to wait for the tunnel to be active
        # For this implementation, we'll assume the controller handles the connection
        self.skill = VisionSkill(model_name="gemma3")
        self._initialized = True
        logger.info("VisionCortex initialized and connected to Savant node.")

    async def ensure_active(self):
        if not self._initialized:
            await self.initialize()

        # Check tunnel status if possible via controller
        # This is a placeholder for actual tunnel health check logic
        if not self.controller.umbilical:
             raise ConnectionError("Umbilical connection is not established")

        return True

    async def verify_asset(self, image_data: bytes | str):
        await self.ensure_active()
        # This calls the VisionSkill through the tunnel
        # The actual implementation of verify_asset would depend on VisionSkill's API
        # but following the directive's logic:
        return await self.skill.perceive(image_data)
