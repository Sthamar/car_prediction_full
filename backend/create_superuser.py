from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, auth
import sys

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

def create_superuser(email, password):
    db: Session = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            print(f"User {email} already exists.")
            user.hashed_password = auth.get_password_hash(password)

            if not user.is_superuser:
                print("Promoting to superuser...")
                user.is_superuser = True
            
            db.commit()
            print(f"Password updated for {email}.")
            return

        print(f"Creating superuser {email}...")
        hashed_password = auth.get_password_hash(password)

        db_user = models.User(
            email=email,
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print("Superuser created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_superuser.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    create_superuser(email, password)
