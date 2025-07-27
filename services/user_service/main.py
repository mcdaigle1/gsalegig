import os
import uvicorn

from shared_utils.config_util import settings

if __name__ == "__main__":    
    env = os.getenv("ENV", "local")
    if env == "local": 
        uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True, log_config=None)
    else:
        uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=False, log_config=None)