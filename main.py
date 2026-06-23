from src.database import init_database


def main():
    init_database()
    print("Smart Clinic AI Agent project initialized successfully.")
    print("Database is ready.")


if __name__ == "__main__":
    main()