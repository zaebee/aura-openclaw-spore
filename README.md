# 🧬 Aura Pheromone Spore (OpenClaw)

The **Aura Pheromone** Spore is a premium OpenClaw Skill that enables autonomous agents to verify digital/physical assets and monetize these insights using the x402 (Payment Required) protocol.

## 🚀 Features

- **VisionCortex Integration:** Remote eye connectivity via Colab Savant node.
- **Aromatic Oracle Tools:**
  - `verify_asset_quality`: High-acuity image analysis (Gemma 3).
  - `appraise_honey_code`: Semantic match analysis for GitHub repositories.
- **Foraging (x402):** Automatic payment handling for deep on-chain data verification.
- **Pheromone Signaling:** Automatic reporting to Moltbook `lablab` submolt.

## 🛠 Installation

Managed with `uv`:

```bash
uv sync
```

## 🧬 Configuration

Required environment variables:
- `AURA_WORKER__PUNK_KEY`: Sensitive key for Savant node connection.
- `MOLTBOOK_TOKEN`: API key for Moltbook signaling.
- `BASE_RPC_URL`: RPC for Base Sepolia transactions.
- `WALLET_PRIVATE_KEY`: Private key for x402 payments.
