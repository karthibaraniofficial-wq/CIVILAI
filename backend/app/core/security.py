"""
CIVICFLOW AI — Security, Authentication & Role-Based Access Control (RBAC)
Supports both Supabase JWT authentication and zero-config local/demo credentials.
"""
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.core.config import settings
from app.db.repository import repo
from app.models.entities import Profile, UserRole

SECRET_KEY = "civicflow-super-secret-key-change-in-production-only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

security_bearer = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    sub: str
    email: str
    role: UserRole
    department_id: Optional[str] = None
    exp: int


def create_access_token(
    user_id: str,
    email: str,
    role: UserRole,
    department_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": user_id,
        "email": email,
        "role": role.value,
        "department_id": department_id,
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[TokenPayload]:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(
            sub=decoded["sub"],
            email=decoded["email"],
            role=UserRole(decoded["role"]),
            department_id=decoded.get("department_id"),
            exp=decoded["exp"]
        )
    except Exception:
        return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer)
) -> Profile:
    """
    Extracts the authenticated profile from Bearer JWT.
    In DEMO mode, if no token is provided, defaults to the default citizen profile.
    """
    if credentials:
        payload = decode_access_token(credentials.credentials)
        if payload:
            profile = repo.profiles.get(payload.sub)
            if profile:
                return profile
            return Profile(
                id=payload.sub,
                full_name=payload.email.split("@")[0].title(),
                email=payload.email,
                role=payload.role,
                department_id=payload.department_id,
            )

    # In Demo mode, provide default profile
    if settings.DEMO_MODE:
        default_user = repo.profiles.get("u0000000-0000-0000-0000-000000000001")
        if default_user:
            return default_user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={"WWW-Authenticate": "Bearer"},
    )


def require_role(allowed_roles: List[UserRole]):
    """
    FastAPI dependency enforcing that the authenticated user possesses one of the allowed roles.
    """
    async def role_checker(current_user: Profile = Depends(get_current_user)) -> Profile:
        if current_user.role not in allowed_roles and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of: {[r.value for r in allowed_roles]}. Current role: {current_user.role.value}"
            )
        return current_user
    return role_checker
