from app import app as flask

if __name__ == "__main__":
    flask.run(debug=True, load_dotenv=True, host="0.0.0.0", port=5000)
