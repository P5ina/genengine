# Промпт: документация API gensprite / genengine

Используй для создания страницы с документацией API на gensprite.ai.

---

Create an API documentation page at `gensprite.ai/docs/api` (or `/api-docs`).

The page should document all public API endpoints used by genengine and third-party integrations.

## Style

- Clean, developer-focused. Inspired by Stripe Docs / Anthropic Docs.
- Dark code blocks with copy button
- Left sidebar with endpoint navigation
- Show request + response examples for every endpoint

## Endpoints to document

### Authentication
All requests use `Authorization: Bearer <api_key>` header.

---

### GET /api/agent/config
Returns runtime config for the genengine agent.

**Response:**
```json
{
  "user_id": "usr_abc123",
  "credits": 142,
  "model": "claude-opus-4-5",
  "max_tokens": 8096
}
```
Note: LLM credentials are provisioned server-side and not exposed.

---

### POST /api/generate
Generate a sprite or tileset image.

**Request:**
```json
{
  "prompt": "pixel art warrior, idle pose, 64x64",
  "width": 64,
  "height": 64,
  "type": "sprite"
}
```

**Response:** PNG binary (Content-Type: image/png)

**Credit cost:** 1 credit per generation

---

### POST /api/generate/tileset
Generate a tileset image.

**Request:**
```json
{
  "prompt": "dungeon stone tiles, top-down, dark",
  "tile_size": 16,
  "type": "tileset"
}
```

**Response:** PNG binary

---

### GET /api/keys
List user's API keys.

### POST /api/keys
Generate a new API key. Returns the full key once — store it immediately.

### DELETE /api/keys/:id
Revoke an API key.

---

### GET /api/credits
Get current credit balance and recent transaction history.

---

## Also include

- Rate limits table (per endpoint)
- Error codes reference (401, 402 insufficient credits, 429 rate limit)
- SDK section: "genengine uses this API automatically when you enter your key in Godot"
- Code examples in Python and GDScript
