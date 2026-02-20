import uvicorn
import os
port = int(os.environ.get("PORT", 8000))  # Railway автоматически задаёт PORT

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=port, reload=True)
