import os
from website import create_app

if not os.path.exists("instance"):
    os.makedirs("instance")

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(debug=False, host="0.0.0.0", port=port)