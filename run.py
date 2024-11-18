from app.app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")

# TODO: improve a bit exception handling of important methods
# TODO: create README to explain how to start application and call endpoints
