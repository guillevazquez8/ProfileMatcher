from app.app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")

# TODO: add data initialization method (create campaign and player)
# TODO: improve a bit exception handling
# TODO: create README to explain how to start application and call endpoints
