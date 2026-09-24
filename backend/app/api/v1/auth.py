"""
CIVICFLOW AI — Authentication API Endpoints
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from uuid import uuid4

from app.core.security import create_access_token, get_current_user
from app.db.repository import repo
from app.models.entities import Profile, UserRole

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    phone: Optional[str] = None
    ward_number: Optional[str] = "Ward 3"


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    profile: Profile


class DemoSwitchRequest(BaseModel):
    role: UserRole


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    # Match user profile by email in repository
    profile = next((p for p in repo.profiles.values() if p.email.lower() == req.email.lower()), None)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(
        user_id=profile.id,
        email=profile.email,
        role=profile.role,
        department_id=profile.department_id,
    )
    return AuthResponse(access_token=token, profile=profile)


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(req: RegisterRequest):
    # Check if user already exists
    existing = next((p for p in repo.profiles.values() if p.email.lower() == req.email.lower()), None)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    new_profile = Profile(
        id=str(uuid4()),
        full_name=req.full_name,
        email=req.email,
        phone=req.phone,
        role=UserRole.CITIZEN,
        ward_number=req.ward_number,
    )
    repo.profiles[new_profile.id] = new_profile

    token = create_access_token(
        user_id=new_profile.id,
        email=new_profile.email,
        role=new_profile.role,
    )
    return AuthResponse(access_token=token, profile=new_profile)


@router.get("/me", response_model=Profile)
async def get_my_profile(current_user: Profile = Depends(get_current_user)):
    return current_user


@router.post("/demo-switch", response_model=AuthResponse)
async def switch_demo_persona(req: DemoSwitchRequest):
    """Allows 1-click switching of active persona during hackathon evaluation."""
    target_profile = next((p for p in repo.profiles.values() if p.role == req.role), None)
    if not target_profile:
        target_profile = repo.profiles["u0000000-0000-0000-0000-000000000001"]

    token = create_access_token(
        user_id=target_profile.id,
        email=target_profile.email,
        role=target_profile.role,
        department_id=target_profile.department_id,
    )
    return AuthResponse(access_token=token, profile=target_profile)
