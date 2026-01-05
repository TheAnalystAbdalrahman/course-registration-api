"""
Authentication API routes
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services import auth_service
from app.middleware.auth import get_current_active_user, require_role
from app.models.user import User, UserRole
from app.exceptions import conflict, bad_request

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Register a new user (Admin only).
    
    For initial setup, you may want to create the first admin user directly in the database
    or through a separate script.
    """
    # Check if user with email already exists
    existing_user = auth_service.get_user_by_email(db, user.email)
    if existing_user:
        raise conflict(f"User with email '{user.email}' already exists")
    
    # If student_id is provided, validate it exists
    if user.student_id:
        from app.services import student_service
        student = student_service.get_student_by_id(db, user.student_id)
        if not student:
            raise bad_request(f"Student with id {user.student_id} does not exist")
        
        # Check if student already has a user account
        existing_student_user = db.query(User).filter(User.student_id == user.student_id).first()
        if existing_student_user:
            raise conflict(f"Student with id {user.student_id} already has a user account")
    
    return auth_service.create_user(db, user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and receive JWT access token.
    
    Use form data with 'username' (email) and 'password' fields.
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-json", response_model=Token)
def login_json(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login using JSON body (alternative to OAuth2 form).
    
    Use this endpoint if you prefer JSON over form data.
    """
    user = auth_service.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current authenticated user information."""
    return current_user
