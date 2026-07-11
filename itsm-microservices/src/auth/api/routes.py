from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    permissions: list[str] = []


class LoginResponse(BaseModel):
    user: UserResponse
    token: str
    refreshToken: str


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest):
    if payload.email != "admin@example.com" or payload.password != "password123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginResponse(
        user=UserResponse(
            id="1",
            name="Admin User",
            email=payload.email,
            role="admin",
            permissions=["read", "write", "manage"],
        ),
        token="demo-token",
        refreshToken="demo-refresh-token",
    )


@router.post("/register", response_model=UserResponse)
async def register(payload: LoginRequest):
    return UserResponse(
        id="2",
        name=payload.email.split("@", 1)[0].title(),
        email=payload.email,
        role="requester",
        permissions=["read"],
    )


@router.post("/logout")
async def logout():
    return {"message": "Logged out"}


@router.get("/me", response_model=UserResponse)
async def me():
    return UserResponse(
        id="1",
        name="Admin User",
        email="admin@example.com",
        role="admin",
        permissions=["read", "write", "manage"],
    )
