# Промпт: личный кабинет gensprite

Используй для создания dashboard страницы в существующем gensprite.ai (SvelteKit + Drizzle).

---

Add a dashboard page to gensprite.ai at `/dashboard` with the following features:

## API Keys section

- User can generate a personal API key (shown once on creation, then masked)
- Button: "Generate new key" (invalidates previous key)
- Key is displayed in a copyable input field right after generation
- Keys table: shows key prefix (first 8 chars + "..."), created_at, last_used_at, status (active/revoked)
- Button to revoke a key

## Credits section

- Show current credit balance
- Show credit usage history (date, action, credits spent)
- Actions: "generate_sprite", "generate_tileset", "agent_llm_call", "agent_asset_call"
- Link to buy more credits (existing payment flow)

## DB schema additions needed

```sql
-- api_keys table
id, user_id, key_hash, key_prefix, created_at, last_used_at, revoked_at

-- credit_transactions table  
id, user_id, action, credits_delta, metadata (json), created_at
```

## API endpoint needed

`GET /api/agent/config` — authenticated by API key (Bearer token)

Returns:
```json
{
  "anthropic_api_key": "sk-ant-...",
  "model": "claude-opus-4-5",
  "max_tokens": 8096,
  "user_id": "...",
  "credits": 142
}
```

This endpoint is called by the genengine agent on startup.
The `anthropic_api_key` is the platform key (from env), not exposed to users.
Before returning, deduct credits or check balance.

## Security

- API keys stored as bcrypt hash in DB, never in plaintext
- Key prefix stored for display only
- `/api/agent/config` rate-limited to 1 req/min per key
- Log every config fetch to credit_transactions
