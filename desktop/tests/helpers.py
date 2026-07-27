from sqlmodel import Session, SQLModel, create_engine


# Import ALL models so they are registered
# import app.modules.inventory.models

def create_test_session() -> Session:
    engine = create_engine("sqlite:///:memory:")

    SQLModel.metadata.create_all(engine)

    return Session(engine)