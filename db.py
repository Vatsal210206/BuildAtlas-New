"""Supabase persistence layer for BuildAtlas.

The Streamlit UI should use this module instead of writing application records
into session state or local files. Credentials are read from Streamlit secrets
first and environment variables second so local and Community Cloud deployments
use the same code path.
"""

from datetime import datetime, timezone
import os
import re
from typing import Any, Dict, Iterable, List, Optional

try:
    from postgrest.exceptions import APIError
except ImportError:  # pragma: no cover - available with the Supabase client
    APIError = Exception


class DatabaseConfigurationError(RuntimeError):
    """Raised when Supabase has not been configured for this deployment."""


class DatabaseOperationError(RuntimeError):
    """Raised when a Supabase operation cannot be completed."""


USER_COLUMNS = frozenset({
    "id", "email", "phone", "password_hash", "password_salt", "role", "verified",
    "otp_salt", "otp_hash", "otp_expires_at", "otp_attempts", "otp_invalidated",
    "otp_last_sent_at", "otp_delivery_status", "created_at",
})
USER_UPDATE_COLUMNS = USER_COLUMNS - {"id", "created_at"}


def _setting(name: str) -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value
    try:
        import streamlit as st
        return str(st.secrets.get(name, "")).strip()
    except (FileNotFoundError, KeyError, RuntimeError):
        return ""


def _database_key() -> str:
    """Return the server-side Supabase key, preferring the explicit name."""
    return _setting("SUPABASE_SERVICE_ROLE_KEY") or _setting("SUPABASE_KEY")


def is_configured() -> bool:
    return bool(_setting("SUPABASE_URL") and _database_key())


def connect():
    url = _setting("SUPABASE_URL")
    key = _database_key()
    if not url or not key:
        raise DatabaseConfigurationError(
            "Supabase is not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in Streamlit secrets."
        )
    try:
        from supabase import create_client
    except ImportError as exc:
        raise DatabaseConfigurationError("The supabase package is not installed.") from exc
    return create_client(url, key)


def _rows(response: Any) -> List[Dict[str, Any]]:
    error = getattr(response, "error", None)
    if error:
        raise DatabaseOperationError(str(error))
    data = getattr(response, "data", None)
    if not isinstance(data, list):
        return []
    return [row for row in data if isinstance(row, dict)]


def _one(response: Any) -> Optional[Dict[str, Any]]:
    rows = _rows(response)
    return rows[0] if rows else None


def _log_api_error(error: APIError) -> None:
    details = {
        "code": getattr(error, "code", None),
        "message": getattr(error, "message", None),
        "details": getattr(error, "details", None),
        "hint": getattr(error, "hint", None),
    }
    print(f"Supabase APIError: {details}")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_user(identifier: str) -> Optional[Dict[str, Any]]:
    client = connect()
    value = identifier.strip().lower()
    response = client.table("users").select("*").or_(f"email.eq.{value},phone.eq.{identifier.strip()}").limit(1).execute()
    return _one(response)


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    response = connect().table("users").select("*").eq("email", email.strip().lower()).limit(1).execute()
    return _one(response)


def list_users() -> List[Dict[str, Any]]:
    return _rows(connect().table("users").select("id,email,phone,role,verified,created_at").order("created_at", desc=True).execute())


def list_auth_users() -> List[Dict[str, Any]]:
    return _rows(connect().table("users").select("*").order("created_at", desc=True).execute())


def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "email": data["email"].strip().lower(),
        "phone": data.get("phone", "").strip(),
        "password_hash": data["password_hash"],
        "password_salt": data["password_salt"],
        "role": data["role"],
        "verified": bool(data.get("verified", False)),
    }
    row = _one(connect().table("users").insert(payload).execute())
    if not row:
        raise DatabaseOperationError("Supabase did not return the created user.")
    return row


def update_user(user_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not isinstance(fields, dict):
        raise DatabaseOperationError("User update fields must be a dictionary.")
    compatible_fields = dict(fields)
    unsupported = set(compatible_fields) - USER_UPDATE_COLUMNS
    if unsupported:
        names = ", ".join(sorted(unsupported))
        raise DatabaseOperationError(f"Unsupported users table field(s): {names}")
    if not compatible_fields:
        return None
    client = connect()
    try:
        response = client.table("users").update(compatible_fields).eq("id", user_id).execute()
    except APIError as exc:
        _log_api_error(exc)
        code = getattr(exc, "code", None)
        message = " ".join(str(value) for value in (
            getattr(exc, "message", ""), getattr(exc, "details", ""), getattr(exc, "hint", "")
        ) if value)
        missing_column = re.search(r"Could not find the '([^']+)' column", message)
        if code != "PGRST204" or not missing_column:
            raise
        column = missing_column.group(1)
        if column not in compatible_fields or column not in USER_UPDATE_COLUMNS:
            raise
        compatible_fields = {key: value for key, value in compatible_fields.items() if key != column}
        if not compatible_fields:
            return None
        try:
            response = client.table("users").update(compatible_fields).eq("id", user_id).execute()
        except APIError as retry_error:
            _log_api_error(retry_error)
            raise
    return _one(response)


def get_profile(user: Dict[str, Any]) -> Dict[str, Any]:
    table = {"DEALER / SUPPLIER": "vendor_profiles", "BUILDER / CONTRACTOR": "builder_profiles", "CUSTOMER": "customer_profiles"}.get(user.get("role"))
    if not table:
        return {}
    return _one(connect().table(table).select("*").eq("user_id", user["id"]).limit(1).execute()) or {}


def create_profile(role: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    table = {"DEALER / SUPPLIER": "vendor_profiles", "BUILDER / CONTRACTOR": "builder_profiles", "CUSTOMER": "customer_profiles"}.get(role)
    if not table:
        return {}
    if role == "CUSTOMER":
        payload = {"user_id": user_id, "full_name": data.get("full_name", ""), "phone": data.get("phone", "")}
    else:
        payload = {"user_id": user_id, "business_name": data.get("business_name", ""), "contact_name": data.get("contact_name", data.get("full_name", "")), "phone": data.get("phone", ""), "address": data.get("address", ""), "city": data.get("city", ""), "state": data.get("state", "")}
    return _one(connect().table(table).insert(payload).execute()) or {}


def update_profile(role: str, user_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    table = {"DEALER / SUPPLIER": "vendor_profiles", "BUILDER / CONTRACTOR": "builder_profiles", "CUSTOMER": "customer_profiles"}.get(role)
    if not table:
        return None
    return _one(connect().table(table).update(fields).eq("user_id", user_id).execute())


def vendor_products(vendor_id: str) -> List[Dict[str, Any]]:
    return _rows(connect().table("products").select("*").eq("vendor_id", vendor_id).order("created_at").execute())


def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("products").insert(data).execute()) or {}


def update_product(product_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    fields = {**fields, "updated_at": _now()}
    return _one(connect().table("products").update(fields).eq("id", product_id).execute())


def delete_product(product_id: str) -> None:
    response = connect().table("products").delete().eq("id", product_id).execute()
    _rows(response)


def vendor_enquiries(vendor_id: str) -> List[Dict[str, Any]]:
    return _rows(connect().table("enquiries").select("*,products(product_name,unit)").eq("vendor_id", vendor_id).order("created_at", desc=True).execute())


def update_enquiry(enquiry_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(connect().table("enquiries").update(fields).eq("id", enquiry_id).execute())


def vendor_quotations(vendor_id: str) -> List[Dict[str, Any]]:
    return _rows(connect().table("quotations").select("*").eq("vendor_id", vendor_id).order("created_at", desc=True).execute())


def create_quotation(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("quotations").insert(data).execute()) or {}


def update_quotation(quote_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(connect().table("quotations").update({**fields, "updated_at": _now()}).eq("id", quote_id).execute())


def vendor_orders(vendor_id: str) -> List[Dict[str, Any]]:
    return _rows(connect().table("orders").select("*").eq("vendor_id", vendor_id).order("created_at", desc=True).execute())


def create_order(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("orders").insert(data).execute()) or {}


def update_order(order_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(connect().table("orders").update({**fields, "updated_at": _now()}).eq("id", order_id).execute())


def vendor_deliveries(vendor_id: str) -> List[Dict[str, Any]]:
    orders = _rows(connect().table("orders").select("id").eq("vendor_id", vendor_id).execute())
    deliveries = []
    for order in orders:
        deliveries.extend(_rows(connect().table("deliveries").select("*").eq("order_id", order["id"]).execute()))
    return deliveries


def create_delivery(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("deliveries").insert(data).execute()) or {}


def update_delivery(delivery_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(connect().table("deliveries").update({**fields, "updated_at": _now()}).eq("id", delivery_id).execute())


def create_enquiry(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("enquiries").insert(data).execute()) or {}


def find_product(product_name: str, supplier: str) -> Optional[Dict[str, Any]]:
    response = connect().table("products").select("*").eq("product_name", product_name).limit(10).execute()
    rows = _rows(response)
    return next((row for row in rows if supplier.lower() in str(row.get("brand", "")).lower() or supplier.lower() in str(row.get("product_name", "")).lower()), rows[0] if rows else None)


def list_project_quote_requests() -> List[Dict[str, Any]]:
    rows = _rows(connect().table("project_quote_requests").select("*").order("created_at", desc=True).execute())
    return [{**row.get("payload", {}), "request_id": row.get("request_id"), "status": row.get("status", "New"), "created_at": row.get("created_at", ""), "updated_at": row.get("updated_at", "")} for row in rows]


def create_project_quote_request(data: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(data)
    request_id = payload.pop("request_id")
    status = payload.pop("status", "New")
    created_at = payload.pop("created_at", _now())
    updated_at = payload.pop("updated_at", created_at)
    row = _one(connect().table("project_quote_requests").insert({"request_id": request_id, "payload": payload, "status": status, "created_at": created_at, "updated_at": updated_at}).execute()) or {}
    return {**payload, "request_id": row.get("request_id", request_id), "status": row.get("status", status), "created_at": row.get("created_at", created_at), "updated_at": row.get("updated_at", updated_at)}


def update_project_quote_request(request_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    current = _one(connect().table("project_quote_requests").select("*").eq("request_id", request_id).limit(1).execute())
    if not current:
        return None
    payload = {**current.get("payload", {}), **{key: value for key, value in fields.items() if key not in {"status", "created_at", "updated_at"}}}
    update = {"payload": payload, "status": fields.get("status", current.get("status", "New")), "updated_at": fields.get("updated_at", _now())}
    row = _one(connect().table("project_quote_requests").update(update).eq("request_id", request_id).execute()) or {}
    return {**payload, "request_id": request_id, "status": row.get("status", update["status"]), "created_at": current.get("created_at", ""), "updated_at": row.get("updated_at", update["updated_at"])}


def quote_requests_for_user(user_id: str, role: str) -> List[Dict[str, Any]]:
    client = connect()
    column = "buyer_id" if role != "BUILDER / CONTRACTOR" else "buyer_id"
    return _rows(client.table("enquiries").select("*").eq(column, user_id).order("created_at", desc=True).execute())


def admin_overview() -> Dict[str, Any]:
    client = connect()
    tables = ("users", "products", "enquiries", "quotations", "orders")
    counts = {}
    for table in tables:
        counts[table] = len(_rows(client.table(table).select("id").execute()))
    users = list_users()
    counts["vendors"] = sum(user.get("role") == "DEALER / SUPPLIER" for user in users)
    counts["builders"] = sum(user.get("role") == "BUILDER / CONTRACTOR" for user in users)
    counts["customers"] = sum(user.get("role") == "CUSTOMER" for user in users)
    profiles = []
    for user in users:
        profile = get_profile(user)
        profiles.append({"role": user.get("role"), "email": user.get("email", ""), "phone": user.get("phone", ""), "verified": user.get("verified", False), "created_at": user.get("created_at", ""), **profile})
    return {"counts": counts, "users": users, "profiles": profiles}
