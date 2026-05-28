from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from sqlalchemy.orm import Session
from datetime import timedelta
import os
import json

from . import models, schemas, auth, database
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nutri Paola API")

AVAILABLE_SCOPES = json.loads(os.getenv("AVAILABLE_SCOPES", '{"me": "Read information about the current user.", "admin": "Admin access."}'))
DEFAULT_SCOPES = json.loads(os.getenv("DEFAULT_SCOPES", '["me"]'))

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes=AVAILABLE_SCOPES
)


def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.email == email).first()

async def get_current_patient(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, email=email)
    except auth.JWTError:
        raise credentials_exception
    user = get_patient_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

@app.get("/")
async def root():
    return {"message": "Welcome to the Nutri Paola API"}

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_patient_by_email(db, form_data.username)
    if not user: #or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    user_scopes = list(form_data.scopes)
    for default_scope in DEFAULT_SCOPES:
        if default_scope not in user_scopes:
            user_scopes.append(default_scope)

    access_token = auth.create_access_token(
        data={"sub": user.email, "scopes": user_scopes}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/patients/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_user = get_patient_by_email(db, email=patient.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(patient.password)
    db_patient = models.Patient(email=patient.email, hashed_password=hashed_password, full_name=patient.full_name)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/me/", response_model=schemas.PatientResponse)
async def read_patients_me(current_user: models.Patient = Security(get_current_patient, scopes=["me"])):
    return current_user
