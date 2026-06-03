import subprocess
import time
import sys
import os
import socket

def find_free_port(preferred_port):
    preferred_port = int(preferred_port)
    for port in range(preferred_port, preferred_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("0.0.0.0", port))
                return str(port)
            except OSError:
                continue
    raise RuntimeError(f"No free port found from {preferred_port} to {preferred_port + 49}")

def start_services():
    # In Docker, use fixed ports. On local machine, find free ports
    is_docker = os.path.exists("/.dockerenv")
    
    backend_port_env = os.environ.get("MEMORYOS_BACKEND_PORT", "8001")
    frontend_port_env = os.environ.get("MEMORYOS_FRONTEND_PORT", "5173")
    
    backend_port = backend_port_env if is_docker else find_free_port(backend_port_env)
    frontend_port = frontend_port_env if is_docker else find_free_port(frontend_port_env)
    backend_url = f"http://localhost:{backend_port}"

    # 1. Start FastAPI Backend
    print(f"Starting FastAPI Backend on {backend_url}...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", str(backend_port)],
        env={**os.environ, "PYTHONPATH": "."}
    )
    
    # Wait for backend to start
    time.sleep(5)
    
    # 2. Start React Frontend
    print(f"Starting React Frontend on http://localhost:{frontend_port}...")
    npm_executable = "npm.cmd" if os.name == "nt" else "npm"
    try:
        frontend_process = subprocess.Popen(
            [npm_executable, "run", "dev", "--", "--host", "0.0.0.0", "--port", str(frontend_port)],
            cwd="frontend",
            env={
                **os.environ,
                "VITE_API_URL": backend_url,
            },
        )
    except FileNotFoundError as exc:
        print(
            "Failed to start the frontend: npm was not found on PATH. "
            "Make sure Node.js is installed and npm is available, then run the frontend manually from the frontend folder."
        )
        backend_process.terminate()
        raise exc
    
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Stopping services...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    start_services()
