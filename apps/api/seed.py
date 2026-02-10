from app.database import SessionLocal
from app.services import seed_example_data


def main() -> None:
    db = SessionLocal()
    try:
        seed_example_data(db)
    finally:
        db.close()


if __name__ == '__main__':
    main()
