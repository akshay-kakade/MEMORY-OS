from app.core.database import engine, Base, SessionLocal
from app.models.models import MemoryCategory, User

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    default_user = db.query(User).filter(User.id == 1).first()
    if not default_user:
        db.add(User(id=1, username="default", email="default@memoryos.local"))

    categories = ["Preference", "Goal", "Project", "Skill", "Fact", "Experience", "Relationship"]
    
    for cat_name in categories:
        exists = db.query(MemoryCategory).filter(MemoryCategory.name == cat_name).first()
        if not exists:
            db.add(MemoryCategory(name=cat_name))
    
    db.commit()
    db.close()
    print("Database initialized and categories seeded.")

if __name__ == "__main__":
    init_db()
