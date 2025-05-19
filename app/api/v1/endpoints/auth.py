from fastapi import APIRouter, HTTPException, Depends, Response
from firebase_admin import auth as firebase_auth
from app.core.supabase import supabase
from app.models.user import UserCreate, UserLogin, UserProfile, PasswordReset, UserUpdate
from app.utils.auth import verify_password_firebase
from app.services.email import email_service
from typing import Optional
import uuid
import os
from datetime import datetime, timedelta
import hashlib


router = APIRouter()

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

async def get_current_user(token: str) -> dict:
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.post("/register", response_model=UserProfile)
async def register_user(user: UserCreate):
    try:
        firebase_user = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )

        user_data = {
            "id": str(uuid.uuid4()),
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture": user.profile_picture,
            "password_hash": hash_password(user.password)
        }
        result = supabase.table("profiles").insert(user_data).execute()
        
        if not result.data:
            firebase_auth.delete_user(firebase_user.uid)
            raise HTTPException(status_code=400, detail="Failed to create user profile")
        
        return UserProfile(**result.data[0])
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(user: UserLogin, response: Response):
    try:
        # Verify credentials with Firebase Auth REST API
        auth_result = await verify_password_firebase(user.email, user.password)
        
        if not auth_result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Get user profile from Supabase
        result = supabase.table("profiles").select("*").eq("email", user.email).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Set httpOnly cookie
        response.set_cookie(
            key="auth_token",
            value=auth_result["idToken"],
            httponly=True,
            secure=True,  # Solo HTTPS
            samesite="lax",  # Protección CSRF
            max_age=3600,  # 1 hora
            path="/"
        )
        
        return {
            "token_type": "bearer",
            "expires_in": int(auth_result["expiresIn"]),
            "refresh_token": auth_result["refreshToken"],
            "profile": result.data[0]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset):
    try:
        link = firebase_auth.generate_password_reset_link(reset_data.email)
        
        await email_service.send_password_reset_email(reset_data.email, link)
        
        return {"message": "Password reset link sent to your email"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout")
async def logout_user(response: Response):
    try:
        # Eliminar la cookie de autenticación
        response.delete_cookie(
            key="auth_token",
            path="/",
            secure=True,
            httponly=True,
            samesite="lax"
        )
        return {"message": "Sesión cerrada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

