"""
Fetch runtime config from gensprite API using the user's API key.
This provides LLM credentials, model settings, and feature flags
without exposing them to the end user.
"""

import httpx
import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)

GENSPRITE_API = "https://gensprite.ai/api"


@dataclass
class AgentConfig:
    anthropic_api_key: str
    model: str = "claude-opus-4-5"
    gensprite_api_key: str = ""
    max_tokens: int = 8096
    user_id: str = ""
    credits: int = 0


async def fetch_config(gensprite_key: str) -> AgentConfig:
    """
    Authenticate with gensprite and get runtime agent config.
    The user only needs to provide their gensprite key —
    LLM credentials are provisioned server-side.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GENSPRITE_API}/agent/config",
            headers={"Authorization": f"Bearer {gensprite_key}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

    config = AgentConfig(
        anthropic_api_key=data["anthropic_api_key"],
        model=data.get("model", "claude-opus-4-5"),
        gensprite_api_key=gensprite_key,
        max_tokens=data.get("max_tokens", 8096),
        user_id=data.get("user_id", ""),
        credits=data.get("credits", 0),
    )

    log.info(f"Config loaded for user {config.user_id} ({config.credits} credits)")
    return config
