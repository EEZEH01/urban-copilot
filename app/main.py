from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.environ.get("PORT", 5000))

    print(f"✅ Urban Copilot is running at http://localhost:{port} | Debug mode: {debug_mode}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)


