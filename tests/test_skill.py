import asyncio
import unittest
from unittest.mock import patch, MagicMock
from aura_pheromone.skill import AromaticOracleSkill

class TestAromaticOracle(unittest.IsolatedAsyncioTestCase):
    @patch("aura_pheromone.vision.VisionCortex.ping")
    @patch("aura_pheromone.vision.VisionCortex.verify_asset")
    @patch("aura_pheromone.skill.AromaticOracleSkill._emit_pheromone")
    async def test_verify_asset_quality(self, mock_emit, mock_verify, mock_ping):
        mock_ping.return_value = {"status": "VITALS_STATUS_OK"}
        mock_verify.return_value = {
            "make": "Honda",
            "model": "FORZA 300",
            "year": 2024,
            "color": "White",
            "confidence_score": 0.98,
            "estimated_price": 6500.0
        }

        skill = AromaticOracleSkill()
        result = await skill.verify_asset_quality("mock_image_data")

        self.assertEqual(result["domain"], "ASSET_DOMAIN_VEHICLE")
        self.assertEqual(result["vehicle"]["make"], "Honda")
        self.assertEqual(result["metadata"]["confidence_score"], "0.98")
        mock_emit.assert_called_once()

    @patch("aura_pheromone.skill.AromaticOracleSkill._fetch_repo_data")
    @patch("aura_pheromone.metabolism.MetabolicInterceptor.request_with_payment")
    @patch("aura_pheromone.skill.AromaticOracleSkill._emit_pheromone")
    async def test_appraise_honey_code_with_foraging(self, mock_emit, mock_request, mock_fetch):
        mock_fetch.return_value = {"stargazers_count": 10, "size": 100}

        # Mock GoldRush response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        skill = AromaticOracleSkill()
        # Ensure energy is present
        with patch("os.environ", {"WALLET_PRIVATE_KEY": "0x123"}):
            result = await skill.appraise_honey_code("https://github.com/user/trenchchat")

        self.assertIn("SURGE", result["recommended_protocol_value"])
        # Should have found rhizome keywords in our logic
        self.assertGreater(result["affinity"], 0.5)
        self.assertEqual(mock_request.call_count, 1) # GoldRush Foraging triggered

if __name__ == "__main__":
    unittest.main()
