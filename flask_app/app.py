from models import Base, engine
from server import app


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    app.run(debug=True)
