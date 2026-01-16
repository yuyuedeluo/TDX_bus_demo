"""FastAPI service that proxies TDX bus ETA and stop data."""
import os
import time
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

TDX_APP_ID = os.getenv("TDX_APP_ID") or ""
TDX_APP_KEY = os.getenv("TDX_APP_KEY") or ""
TDX_API_BASE = os.getenv("TDX_API_BASE", "https://tdx.transportdata.tw/api")
TDX_TOKEN_URL = os.getenv(
    "TDX_TOKEN_URL",
    "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token",
)
DEFAULT_CITY = os.getenv("TDX_DEFAULT_CITY", "Taipei")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
REQUEST_TIMEOUT = float(os.getenv("TDX_REQUEST_TIMEOUT", "15"))
TOKEN_SAFETY_WINDOW = 30

token_cache: Dict[str, Any] = {"access_token": None, "expires_at": 0}


app = FastAPI(title="TDX Bus ETA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _get_token(client: httpx.AsyncClient) -> str:
    """Fetch and cache the TDX access token."""
    now = time.time()
    if token_cache["access_token"] and now < token_cache["expires_at"]:
        return token_cache["access_token"]

    if not TDX_APP_ID or not TDX_APP_KEY:
        raise HTTPException(status_code=500, detail="TDX credentials are missing.")

    data = {
        "grant_type": "client_credentials",
        "client_id": TDX_APP_ID,
        "client_secret": TDX_APP_KEY,
    }
    try:
        resp = await client.post(TDX_TOKEN_URL, data=data, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"TDX token error: {exc}") from exc

    payload = resp.json()
    access_token: Optional[str] = payload.get("access_token")
    expires_in: int = payload.get("expires_in", 0)
    if not access_token:
        raise HTTPException(status_code=502, detail="TDX token missing in response.")

    token_cache["access_token"] = access_token
    token_cache["expires_at"] = now + max(expires_in - TOKEN_SAFETY_WINDOW, 0)
    return access_token


async def _tdx_get(path: str, city: str, route: str) -> List[Dict[str, Any]]:
    """Call a TDX GET endpoint for the given city/route and return JSON list."""
    url = f"{TDX_API_BASE}{path.format(city=city, route=route)}"
    async with httpx.AsyncClient() as client:
        token = await _get_token(client)
        headers = {"authorization": f"Bearer {token}"}
        try:
            resp = await client.get(
                url, headers=headers, timeout=REQUEST_TIMEOUT, params={"$format": "JSON"}
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"TDX API error: {exc.response.text}",
            ) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"TDX network error: {exc}") from exc

    data = resp.json()
    if isinstance(data, dict):
        # Some TDX endpoints wrap payloads in a dict with 'data' key.
        return data.get("data", [])
    return data


def _normalize_route_name(name: Optional[str]) -> str:
    return str(name or "").strip().lower()


def _filter_by_route(rows: List[Dict[str, Any]], route: str) -> List[Dict[str, Any]]:
    """
    Keep only rows whose RouteName/SubRouteName matches the requested route.
    - Exact match is preferred.
    - Prefix match is allowed unless the suffix starts with "區" (e.g., exclude 208區 when asking 208).
    """
    target = _normalize_route_name(route)

    def name_matches(name: Optional[str]) -> bool:
        if not name:
            return False
        norm = _normalize_route_name(name)
        if norm == target:
            return True
        if norm.startswith(target):
            suffix = norm[len(target) :]
            if suffix and suffix[0] == "區":
                return False
            return True
        return False

    return [
        row
        for row in rows
        if name_matches((row.get("RouteName") or {}).get("Zh_tw"))
        or name_matches((row.get("RouteName") or {}).get("En"))
        or name_matches((row.get("SubRouteName") or {}).get("Zh_tw"))
        or name_matches((row.get("SubRouteName") or {}).get("En"))
    ]


async def fetch_eta(city: str, route: str) -> List[Dict[str, Any]]:
    """Fetch estimated arrival times."""
    rows = await _tdx_get(
        "/v2/Bus/EstimatedTimeOfArrival/City/{city}/{route}", city=city, route=route
    )
    return _filter_by_route(rows, route)


async def fetch_stop_of_route(city: str, route: str) -> List[Dict[str, Any]]:
    """Fetch stop order for both directions."""
    rows = await _tdx_get("/v2/Bus/StopOfRoute/City/{city}/{route}", city=city, route=route)
    return _filter_by_route(rows, route)


def merge_stop_eta(
    stop_rows: List[Dict[str, Any]], eta_rows: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Merge stop order with ETA data, grouped by direction."""
    eta_lookup: Dict[str, Dict[int, Dict[str, Any]]] = {}
    for row in eta_rows:
        stop_uid = row.get("StopUID")
        direction = row.get("Direction")
        if stop_uid is None or direction is None:
            continue
        eta_lookup.setdefault(stop_uid, {})[direction] = row

    merged: Dict[int, Dict[str, Any]] = {}
    for stop in stop_rows:
        direction = stop.get("Direction")
        stops = stop.get("Stops") or []
        key = direction if direction is not None else -1
        dir_bucket = merged.setdefault(
            key,
            {
                "direction": key,
                "stops": [],
                "route_name": stop.get("RouteName", {}).get("Zh_tw", ""),
                "headsign": stop.get("Headsign", ""),
                "update_time": stop.get("UpdateTime"),
            },
        )
        seen_uids: set[str] = {s["stop_uid"] for s in dir_bucket["stops"] if s.get("stop_uid")}
        for s in stops:
            uid = s.get("StopUID")
            if uid and uid in seen_uids:
                continue  # skip duplicated StopUID within same direction
            if uid:
                seen_uids.add(uid)
            eta = eta_lookup.get(uid, {}).get(direction, {})
            dir_bucket["stops"].append(
                {
                    "stop_uid": uid,
                    "stop_id": s.get("StopID"),
                    "stop_sequence": s.get("StopSequence"),
                    "direction": direction,
                    "name": {
                        "zh": (s.get("StopName") or {}).get("Zh_tw"),
                        "en": (s.get("StopName") or {}).get("En"),
                    },
                    "estimate_seconds": eta.get("EstimateTime"),
                    "stop_status": eta.get("StopStatus"),
                    "plate_numb": eta.get("PlateNumb"),
                    "next_bus_time": eta.get("NextBusTime"),
                }
            )

    for bucket in merged.values():
        bucket["stops"].sort(key=lambda x: x.get("stop_sequence") or 0)

    return list(merged.values())


@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/api/routes/{route}/eta")
async def route_eta(
    route: str,
    city: str = Query(DEFAULT_CITY, description="TDX city name, e.g. Taipei or NewTaipei"),
) -> List[Dict[str, Any]]:
    return await fetch_eta(city, route)


@app.get("/api/routes/{route}/stops")
async def route_stops(
    route: str,
    city: str = Query(DEFAULT_CITY, description="TDX city name, e.g. Taipei or NewTaipei"),
) -> List[Dict[str, Any]]:
    return await fetch_stop_of_route(city, route)


@app.get("/api/routes/{route}/stop-etas")
async def route_stop_etas(
    route: str,
    city: str = Query(DEFAULT_CITY, description="TDX city name, e.g. Taipei or NewTaipei"),
) -> Dict[str, Any]:
    stop_rows, eta_rows = await fetch_stop_of_route(city, route), await fetch_eta(city, route)
    merged = merge_stop_eta(stop_rows, eta_rows)
    return {
        "route": route,
        "city": city,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "directions": merged,
    }


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "TDX Bus ETA service"}


if __name__ == "__main__":
    import uvicorn

    current_dir = os.path.dirname(os.path.join(os.path.dirname(__file__), ".."))
    app_dir = os.path.dirname(current_dir)

    uvicorn.run("main:app", host="0.0.0.0", port=8000, app_dir=app_dir, reload=True)
