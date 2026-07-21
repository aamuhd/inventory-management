from sqlmodel import Session, SQLModel, create_engine



def create_test_session() -> Session:
    engine = create_engine("sqlite:///:memory:")

    SQLModel.metadata.create_all(engine)

    return Session(engine)