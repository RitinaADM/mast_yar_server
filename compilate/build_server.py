import PyInstaller.__main__
import os

def build_server():
    # Define paths
    project_dir = os.path.dirname(os.path.abspath(__file__))  # Inside server/compilate/
    server_dir = os.path.dirname(project_dir)  # Parent directory (server/)
    env_file = os.path.join(server_dir, ".env")
    db_file = os.path.join(server_dir, "records.db")
    output_dir = os.path.join(project_dir, "dist", "server")  # Output to server/compilate/dist/server/

    # PyInstaller command
    PyInstaller.__main__.run([
        os.path.join(server_dir, "main.py"),  # Reference main.py in server/
        "--onedir",
        "--name=server",
        f"--add-data={env_file}{os.pathsep}.env",
        f"--add-data={db_file}{os.pathsep}records.db",
        f"--distpath={os.path.join(project_dir, 'dist')}",  # Output to server/compilate/dist/
        f"--workpath={os.path.join(project_dir, 'build')}",  # Build in server/compilate/build/
        f"--specpath={os.path.join(project_dir, 'spec')}",   # Spec in server/compilate/spec/
        "--noconfirm"
    ])

    print(f"Server built successfully in {output_dir}")

if __name__ == "__main__":
    build_server()