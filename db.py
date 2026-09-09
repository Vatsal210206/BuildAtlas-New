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
    class APIError(Exception):
        """Fallback type used when the Supabase client is unavailable locally."""


class DatabaseConfigurationError(RuntimeError):
    """Raised when Supabase has not been configured for this deployment."""


class DatabaseOperationError(RuntimeError):
    """Raised when a Supabase operation cannot be completed."""


class DuplicateUserError(DatabaseOperationError):
    """Raised when a user email or phone is already registered."""

    def __init__(self, field: str):
        self.field = field
        super().__init__(f"An account with this {field} already exists.")


USER_COLUMNS = frozenset({
    "id", "email", "phone", "password_hash", "password_salt", "role", "verified",
    "otp_salt", "otp_hash", "otp_expires_at", "otp_attempts", "otp_invalidated",
    "otp_last_sent_at", "otp_delivery_status", "created_at",
})
USER_UPDATE_COLUMNS = USER_COLUMNS - {"id", "created_at"}
USER_INSERT_COLUMNS = frozenset({
    "email", "phone", "password_hash", "password_salt", "role", "verified",
})
PROFILE_COLUMNS = {
    "vendor_profiles": frozenset({
        "id", "user_id", "business_name", "contact_name", "phone", "address", "city",
        "state", "created_at"
    }),
    "builder_profiles": frozenset({
        "id", "user_id", "business_name", "contact_name", "phone", "address", "city",
        "state", "gst_number", "portfolio_summary", "website", "specializations", "created_at"
    }),
    "customer_profiles": frozenset({
        "id", "user_id", "full_name", "phone", "created_at"
    }),
}
BUILDER_PAST_PROJECT_COLUMNS = frozenset({
    "project_name", "estimated_value", "description",
})


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


def _api_error_message(error: APIError) -> str:
    return " ".join(str(value) for value in (
        getattr(error, "message", ""), getattr(error, "details", ""), getattr(error, "hint", "")
    ) if value) or str(error)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_user(identifier: str) -> Optional[Dict[str, Any]]:
    client = connect()
    value = identifier.strip().lower()
    response = client.table("users").select("*").or_(f"email.eq.{value},phone.eq.{identifier.strip()}").limit(1).execute()
    return _one(response)


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    return _one(connect().table("users").select("*").eq("id", user_id).limit(1).execute())


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    response = connect().table("users").select("*").eq("email", email.strip().lower()).limit(1).execute()
    return _one(response)


def list_users() -> List[Dict[str, Any]]:
    return _rows(connect().table("users").select("id,email,phone,role,verified,created_at").order("created_at", desc=True).execute())


def list_auth_users() -> List[Dict[str, Any]]:
    return _rows(connect().table("users").select("*").order("created_at", desc=True).execute())


def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    email = str(data.get("email", "")).strip().lower()
    phone = str(data.get("phone", "")).strip()
    role = str(data.get("role", "")).strip()
    if not email or not phone or not role:
        raise DatabaseOperationError("Email, phone, and role are required to create an account.")
    client = connect()
    try:
        if _one(client.table("users").select("id").eq("email", email).limit(1).execute()):
            raise DuplicateUserError("email")
        if _one(client.table("users").select("id").eq("phone", phone).limit(1).execute()):
            raise DuplicateUserError("phone")
    except APIError as exc:
        _log_api_error(exc)
        raise DatabaseOperationError(
            f"Supabase could not check whether the account already exists: {_api_error_message(exc)}"
        ) from exc
    payload = {
        "email": email,
        "phone": phone,
        "password_hash": data["password_hash"],
        "password_salt": data["password_salt"],
        "role": role,
        "verified": bool(data.get("verified", False)),
    }
    payload = {key: value for key, value in payload.items() if key in USER_INSERT_COLUMNS}
    try:
        row = _one(client.table("users").insert(payload).select("*").execute())
    except APIError as exc:
        _log_api_error(exc)
        message = _api_error_message(exc)
        lowered_message = message.lower()
        if "users_email_key" in message or ("email" in lowered_message and "duplicate" in lowered_message):
            raise DuplicateUserError("email") from exc
        if "users_phone_key" in message or ("phone" in lowered_message and "duplicate" in lowered_message):
            raise DuplicateUserError("phone") from exc
        raise DatabaseOperationError(f"Supabase could not create the user: {message or 'database error'}") from exc
    if not row:
        raise DatabaseOperationError("Supabase did not return the created user.")
    return row


def delete_user(user_id: str) -> None:
    if not user_id:
        return
    try:
        response = connect().table("users").delete().eq("id", user_id).execute()
        _rows(response)
    except APIError as exc:
        _log_api_error(exc)
        raise DatabaseOperationError(f"Supabase could not roll back the new user: {_api_error_message(exc)}") from exc


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
    while compatible_fields:
        try:
            response = client.table("users").update(compatible_fields).eq("id", user_id).select("*").execute()
            updated_user = _one(response)
            if updated_user is None:
                raise DatabaseOperationError("Supabase users update did not affect the requested user.")
            return updated_user
        except APIError as exc:
            _log_api_error(exc)
            code = getattr(exc, "code", None)
            message = _api_error_message(exc)
            missing_column = re.search(r"Could not find the '([^']+)' column", message)
            if code == "PGRST204" and missing_column:
                column = missing_column.group(1)
                if column in compatible_fields and column in USER_UPDATE_COLUMNS:
                    raise DatabaseOperationError(
                        f"The Supabase users table is missing required OTP/authentication column '{column}'. "
                        "Apply the users OTP migration and reload the PostgREST schema cache."
                    ) from exc
            raise DatabaseOperationError(f"Supabase users update failed: {message or 'unknown API error'}") from exc
    return None


def get_profile(user: Dict[str, Any]) -> Dict[str, Any]:
    table = {"DEALER / SUPPLIER": "vendor_profiles", "BUILDER / CONTRACTOR": "builder_profiles", "CUSTOMER": "customer_profiles"}.get(user.get("role"))
    if not table:
        return {}
    try:
        return _one(connect().table(table).select("*").eq("user_id", user["id"]).limit(1).execute()) or {}
    except APIError as exc:
        raise DatabaseOperationError(f"Supabase could not load the {table} profile: {_api_error_message(exc)}") from exc


def create_profile(role: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    table = {"DEALER / SUPPLIER": "vendor_profiles", "BUILDER / CONTRACTOR": "builder_profiles", "CUSTOMER": "customer_profiles"}.get(role)
    if not table:
        return {}
    if role == "CUSTOMER":
        payload = {"user_id": user_id, "full_name": data.get("full_name", ""), "phone": data.get("phone", "")}
    else:
        payload = {"user_id": user_id, "business_name": data.get("business_name", ""), "contact_name": data.get("contact_name", data.get("full_name", "")), "phone": data.get("phone", ""), "address": data.get("address", ""), "city": data.get("city", ""), "state": data.get("state", ""), "gst_number": data.get("gst_number", ""), "portfolio_summary": data.get("portfolio_summary", ""), "website": data.get("website", ""), "specializations": data.get("specializations", "")}
    allowed = PROFILE_COLUMNS[table] - {"id", "created_at"}
    payload = {key: value for key, value in payload.items() if key in allowed}
    try:
        row = _one(connect().table(table).insert(payload).select("*").execute())
    except APIError as exc:
        raise DatabaseOperationError(f"Supabase could not create the {table} profile: {_api_error_message(exc)}") from exc
    if not row:
        raise DatabaseOperationError(f"Supabase did not return the created {table} profile.")
    return row


def update_profile(role: str, user_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    table = {"DEALER / SUPPLIER": "vendor_profiles", "BUILDER / CONTRACTOR": "builder_profiles", "CUSTOMER": "customer_profiles"}.get(role)
    if not table:
        return None
    allowed = PROFILE_COLUMNS[table] - {"id", "user_id", "created_at"}
    payload = {key: value for key, value in fields.items() if key in allowed}
    if not payload:
        raise DatabaseOperationError(f"No supported fields were provided for {table}.")
    client = connect()
    try:
        existing = _one(client.table(table).select("id").eq("user_id", user_id).limit(1).execute())
        if existing:
            updated = _one(client.table(table).update(payload).eq("user_id", user_id).select("*").execute())
            if not updated:
                raise DatabaseOperationError(f"Supabase did not update the {table} profile.")
            return updated
        created = _one(client.table(table).insert({"user_id": user_id, **payload}).select("*").execute())
    except APIError as exc:
        raise DatabaseOperationError(f"Supabase could not save the {table} profile: {_api_error_message(exc)}") from exc
    if not created:
        raise DatabaseOperationError(f"Supabase did not create the missing {table} profile.")
    return created


def list_builder_projects(user_id: str) -> List[Dict[str, Any]]:
    return _rows(connect().table("builder_projects").select("*").eq("user_id", user_id).order("created_at", desc=True).execute())


def create_builder_project(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("builder_projects").insert(data).execute()) or {}


def update_builder_project(project_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(connect().table("builder_projects").update({**fields, "updated_at": _now()}).eq("id", project_id).execute())


def list_builder_past_projects(user_id: str) -> List[Dict[str, Any]]:
    if not user_id:
        raise DatabaseOperationError("A builder user ID is required to load past projects.")
    try:
        return _rows(
            connect().table("builder_projects")
            .select("id,user_id,project_name,estimated_value,description,created_at,updated_at")
            .eq("user_id", user_id).order("created_at", desc=True).execute()
        )
    except APIError as exc:
        _log_api_error(exc)
        raise DatabaseOperationError(f"Supabase could not load past projects: {_api_error_message(exc)}") from exc


def create_builder_past_project(user_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    if not user_id:
        raise DatabaseOperationError("A builder user ID is required to create a past project.")
    if not isinstance(fields, dict):
        raise DatabaseOperationError("Past project fields must be a dictionary.")
    payload = {key: value for key, value in fields.items() if key in BUILDER_PAST_PROJECT_COLUMNS}
    if not payload.get("project_name"):
        raise DatabaseOperationError("A past project name is required.")
    payload["user_id"] = user_id
    try:
        row = _one(
            connect().table("builder_projects")
            .insert(payload).select("id,user_id,project_name,estimated_value,description,created_at,updated_at").execute()
        )
    except APIError as exc:
        _log_api_error(exc)
        raise DatabaseOperationError(f"Supabase could not create the past project: {_api_error_message(exc)}") from exc
    if not row:
        raise DatabaseOperationError("Supabase did not return the created past project.")
    return row


def update_builder_past_project(user_id: str, project_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not user_id or not project_id:
        raise DatabaseOperationError("A builder user ID and past project ID are required to update a past project.")
    if not isinstance(fields, dict):
        raise DatabaseOperationError("Past project fields must be a dictionary.")
    payload = {key: value for key, value in fields.items() if key in BUILDER_PAST_PROJECT_COLUMNS}
    if not payload:
        raise DatabaseOperationError("No supported past project fields were provided.")
    if "project_name" in payload and not payload["project_name"]:
        raise DatabaseOperationError("A past project name is required.")
    try:
        row = _one(
            connect().table("builder_projects").update({**payload, "updated_at": _now()})
            .eq("id", project_id).eq("user_id", user_id)
            .select("id,user_id,project_name,estimated_value,description,created_at,updated_at").execute()
        )
    except APIError as exc:
        _log_api_error(exc)
        raise DatabaseOperationError(f"Supabase could not update the past project: {_api_error_message(exc)}") from exc
    if row is None:
        raise DatabaseOperationError("Past project was not found for the authenticated builder.")
    return row


def delete_builder_past_project(user_id: str, project_id: str) -> None:
    if not user_id or not project_id:
        raise DatabaseOperationError("A builder user ID and past project ID are required to delete a past project.")
    try:
        response = connect().table("builder_projects").delete().eq("id", project_id).eq("user_id", user_id).select("id").execute()
        rows = _rows(response)
        if not rows:
            raise DatabaseOperationError("Past project was not found for the authenticated builder.")
    except APIError as exc:
        _log_api_error(exc)
        raise DatabaseOperationError(f"Supabase could not delete the past project: {_api_error_message(exc)}") from exc


def list_builder_quotations(user_id: str) -> List[Dict[str, Any]]:
    return _rows(connect().table("builder_quotations").select("*").eq("user_id", user_id).order("created_at", desc=True).execute())


def create_builder_quotation(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("builder_quotations").insert(data).execute()) or {}


def update_builder_quotation(quote_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(connect().table("builder_quotations").update({**fields, "updated_at": _now()}).eq("id", quote_id).execute())


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


def vendor_order_unlock(vendor_id: str, order_id: str) -> Optional[Dict[str, Any]]:
    return _one(
        connect().table("vendor_order_unlocks").select("*")
        .eq("vendor_id", vendor_id).eq("order_id", order_id).limit(1).execute()
    )


def create_vendor_order_unlock(data: Dict[str, Any]) -> Dict[str, Any]:
    return _one(connect().table("vendor_order_unlocks").insert(data).execute()) or {}


def update_vendor_order_unlock(vendor_id: str, order_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return _one(
        connect().table("vendor_order_unlocks")
        .update({**fields, "updated_at": _now()})
        .eq("vendor_id", vendor_id).eq("order_id", order_id).execute()
    )


def customer_contact(user_id: str) -> Optional[Dict[str, Any]]:
    user = _one(connect().table("users").select("id,email,phone,role").eq("id", user_id).limit(1).execute())
    if not user or user.get("role") != "CUSTOMER":
        return None
    profile = _one(connect().table("customer_profiles").select("full_name,phone").eq("user_id", user_id).limit(1).execute()) or {}
    return {
        "id": user["id"],
        "name": profile.get("full_name", "Customer"),
        "phone": profile.get("phone") or user.get("phone", ""),
        "email": user.get("email", ""),
    }


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


def list_public_products() -> List[Dict[str, Any]]:
    """Fetch all vendor-added products for customer marketplace.

    Retrieves all products from the products table and enriches them with
    vendor business names from vendor_profiles. If a vendor profile is not found,
    uses a generic 'Vendor' label.
    """
    try:
        # Fetch all products
        response = connect().table("products").select("*").order("created_at").execute()
        products = _rows(response)

        if not products:
            return []

        # Fetch all vendor profiles to map vendor_id -> business_name
        vendor_response = connect().table("vendor_profiles").select("user_id, business_name").execute()
        vendor_profiles = _rows(vendor_response)

        # Build vendor_id -> business_name map
        vendor_name_map = {vp["user_id"]: vp["business_name"] for vp in vendor_profiles if isinstance(vp, dict)}

        # Add supplier field to each product
        for product in products:
            if isinstance(product, dict):
                vendor_id = product.get("vendor_id")
                product["supplier"] = vendor_name_map.get(vendor_id, "Vendor")

        return products
    except Exception as e:
        _log_api_error(e) if isinstance(e, APIError) else print(f"Error fetching public products: {e}")
        return []


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
