import app as app

server = app.server


if __name__ == "__main__":
    server.run(debug=False, host = "0.0.0.0", port=8080)