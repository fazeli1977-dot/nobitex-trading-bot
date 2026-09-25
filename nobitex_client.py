"""
Nobitex margin trading client
High-performance async client for Nobitex API interactions.
"""

import asyncio
import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import aiohttp

from config import NOBITEX_API_BASE_URL, NOBITEX_API_KEY, NOBITEX_API_SECRET, SYSTEM_CONFIG


@dataclass
class AccountBalance:
    currency: str
    free: float
    locked: float
    total: float


@dataclass
class MarketStats:
    symbol: str
    last_price: float
    change_percent_24h: float
    volume_24h: float
    high_24h: float
    low_24h: float


class NobitexClient:
    """Async client wrapper for Nobitex API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = NOBITEX_API_BASE_URL,
        timeout: int = None,
    ) -> None:
        self.api_key = api_key or NOBITEX_API_KEY
        self.api_secret = api_secret or NOBITEX_API_SECRET
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout or SYSTEM_CONFIG.API_TIMEOUT_SECONDS
        self.session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def start(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers={"Accept": "application/json"},
            )

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    def _utc_timestamp(self) -> int:
        return int(time.time() * 1000)

    def _sign(self, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> str:
        if not self.api_key or not self.api_secret:
            raise ValueError("Nobitex API key and secret are required.")

        nonce = str(self._utc_timestamp())
        payload = f"{nonce}{method.upper()}{path}"
        if body:
            payload += json.dumps(body, separators=(",", ":"), sort_keys=True)

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return signature

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        auth: bool = True,
        retries: int = 0,
    ) -> Any:
        if self.session is None or self.session.closed:
            await self.start()

        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}

        if auth:
            nonce = str(self._utc_timestamp())
            body = json_body or {}
            payload = f"{nonce}{method.upper()}{path}"
            if body:
                payload += json.dumps(body, separators=(",", ":"), sort_keys=True)
            signature = hmac.new(
                self.api_secret.encode("utf-8"),
                payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            headers.update(
                {
                    "Api-Key": self.api_key,
                    "Nonce": nonce,
                    "Signature": signature,
                }
            )

        try:
            async with self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_body if method.upper() in {"POST", "PUT", "PATCH"} else None,
                headers=headers,
            ) as response:
                data = await response.text()
                if response.status == 204:
                    return {}
                if response.status == 429:
                    backoff = min(2 ** retries * SYSTEM_CONFIG.BACKOFF_MULTIPLIER, SYSTEM_CONFIG.BACKOFF_MAX_WAIT)
                    if retries < SYSTEM_CONFIG.API_MAX_RETRIES:
                        await asyncio.sleep(backoff)
                        return await self._request(method, path, params=params, json_body=json_body, auth=auth, retries=retries + 1)
                    raise RuntimeError(f"Rate limit exceeded on {path}")
                if response.status >= 400:
                    raise RuntimeError(f"HTTP {response.status}: {data}")
                try:
                    return json.loads(data) if data else {}
                except json.JSONDecodeError:
                    return data
        except asyncio.TimeoutError:
            if retries < SYSTEM_CONFIG.API_MAX_RETRIES:
                await asyncio.sleep(2 ** retries)
                return await self._request(method, path, params=params, json_body=json_body, auth=auth, retries=retries + 1)
            raise

    async def get_markets(self) -> List[Dict[str, Any]]:
        return await self._request("GET", "/v2/markets")

    async def get_market_stats(self, symbol: str) -> Dict[str, Any]:
        return await self._request("GET", f"/v2/market/stats/{symbol}")

    async def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        return await self._request("GET", f"/v2/orderbook/{symbol}", params={"limit": limit})

    async def get_trades(self, symbol: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self._request("GET", f"/v2/trades/{symbol}", params={"limit": limit})

    async def get_ohlcv(self, symbol: str, interval: str = "5m", limit: int = 200) -> List[Dict[str, Any]]:
        return await self._request("GET", f"/v2/ohlcv/{symbol}", params={"interval": interval, "limit": limit})

    async def get_account_balance(self) -> List[Dict[str, Any]]:
        return await self._request("GET", "/v2/users/me/wallets")

    async def get_margin_summary(self) -> Dict[str, Any]:
        return await self._request("GET", "/v2/margin/summary")

    async def get_open_positions(self) -> List[Dict[str, Any]]:
        return await self._request("GET", "/v2/margin/positions")

    async def get_open_orders(self) -> List[Dict[str, Any]]:
        return await self._request("GET", "/v2/orders")

    async def create_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        price: Optional[float] = None,
        order_type: str = "limit",
        leverage: Optional[int] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "symbol": symbol,
            "side": side.lower(),
            "amount": amount,
            "type": order_type,
        }
        if price is not None:
            payload["price"] = price
        if leverage is not None:
            payload["leverage"] = leverage
        if stop_loss is not None:
            payload["stop_loss"] = stop_loss
        if take_profit is not None:
            payload["take_profit"] = take_profit
        return await self._request("POST", "/v2/margin/order", json_body=payload)

    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/v2/orders/{order_id}")

    async def close_position(self, symbol: str, side: str, amount: Optional[float] = None) -> Dict[str, Any]:
        payload = {"symbol": symbol, "side": side.lower()}
        if amount is not None:
            payload["amount"] = amount
        return await self._request("POST", "/v2/margin/close", json_body=payload)

    async def heartbeat(self) -> bool:
        try:
            await self.get_markets()
            return True
        except Exception:
            return False


async def main() -> None:
    client = NobitexClient()
    await client.start()
    try:
        data = await client.get_markets()
        print(f"Market sample: {data[:2] if isinstance(data, list) else data}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
