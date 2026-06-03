import os
import uvicorn

if __name__ == "__main__":
    # Use 8001 locally, fall back to Render's injected PORT in production
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
