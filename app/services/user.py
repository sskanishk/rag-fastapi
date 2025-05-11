from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import UserCreate
from app.db.models import User
from app.core.security.jwt import hash_password

async def get_user_by_email_old(db: AsyncSession, email: str):
    print("get user back via meial - result 1 ", email)
    result = await db.execute(select(User).filter(User.email == email))
    print("get user back via meial - result ", result.scalar_one_or_none())
    return result.scalar_one_or_none()

async def get_user_by_email__o(db: AsyncSession, email: str) -> User | None:
    """Get a single user by email address.
    Args:
        db: Async SQLAlchemy session
        email: Email address to search for
    Returns:
        User object if found, None otherwise
    """
    try:
        # logger.debug(f"Fetching user by email: {email}")  # Use logging instead of print
        result = await db.execute(
            select(User).where(User.email == email).limit(1)
        )
        user = result.scalars().first()  # More explicit than scalar_one_or_none()
        # logger.debug(f"User found: {bool(user)}")
        print("get user back via meial - result new ", user)
        return user
        
    except Exception as e:
        # logger.error(f"Error fetching user by email {email}: {str(e)}")
        raise  # Re-raise if you want calling code to handle, or return None

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    print(f"[DEBUG] Searching for user with email: {email}")  # Verify input
    
    try:
        query = select(User).where(User.email == email).limit(1)
        print(f"[DEBUG] Generated SQL: {query}")  # Inspect the raw SQL
        
        result = await db.execute(query)
        user = result.scalars().first()
        
        print(f"[DEBUG] User found: {user}")  # Confirm result
        return user
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch user: {str(e)}")
        raise

async def create_user(db: AsyncSession, user_data: UserCreate):
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("User already exists")

    hashed_pw = hash_password(user_data.password)
    new_user = User(email=user_data.email, name=user_data.name, hashed_password=hashed_pw)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
