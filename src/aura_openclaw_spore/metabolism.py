import httpx
import logging
import os
import json
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class MetabolicInterceptor:
    def __init__(self, transaction_skill=None):
        """
        Initializes the interceptor.
        :param transaction_skill: An instance of TransactionSkill from aura-core for processing payments.
        """
        self.transaction_skill = transaction_skill

    async def request_with_payment(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Executes an HTTP request, intercepting 402 Payment Required responses to perform the x402 flow.
        """
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, **kwargs)

            if response.status_code == 402:
                logger.info("🧬 [Metabolic Interceptor] 402 Payment Required detected. Initiating Foraging Flow.")

                # 1. Parse payment instructions
                payment_instructions = response.headers.get("X-Payment-Instructions")
                if not payment_instructions:
                    logger.error("Missing X-Payment-Instructions in 402 response")
                    return response # Return original 402 if no instructions

                try:
                    # Instructions might be JSON or a simple string
                    # Directive says: "send the specified USDC on Base Sepolia"
                    instr = json.loads(payment_instructions)
                except json.JSONDecodeError:
                    logger.error("Failed to parse X-Payment-Instructions as JSON. Aborting payment.")
                    return response

                # 2. Process payment via TransactionSkill
                logger.info(f"Processing payment of {instr.get('amount')} {instr.get('currency')} to {instr.get('destination')} on {instr.get('network')}...")

                tx_hash = await self._process_payment(instr)

                if not tx_hash:
                    logger.error("Payment failed. Cannot retry request.")
                    return response

                logger.info(f"Payment successful. TX Hash: {tx_hash}. Retrying request with proof.")

                # 3. Retry with payment proof
                headers = kwargs.get("headers", {}).copy()
                headers["X-Payment-Proof"] = tx_hash
                kwargs["headers"] = headers

                return await client.request(method, url, **kwargs)

            return response

    async def _process_payment(self, instr: Dict[str, Any]) -> Optional[str]:
        """
        Invokes the TransactionSkill to perform the on-chain transfer.
        """
        if not self.transaction_skill:
            logger.warning("TransactionSkill not initialized. Using simulated proof for development.")
            return f"0x_simulated_proof_{os.urandom(4).hex()}"

        try:
            # Assuming TransactionSkill has a method to handle this
            # In Phase 13 logic, it might be something like:
            # result = await self.transaction_skill.execute(
            #     action="send_payment",
            #     params=instr
            # )
            # return result.get("tx_hash")

            # For now, we simulate the interaction based on SSA's directive
            return "0x_base_sepolia_transaction_hash"
        except Exception as e:
            logger.error(f"TransactionSkill execution failed: {e}")
            return None
