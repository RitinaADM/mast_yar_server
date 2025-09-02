"""
Скрипт сборки для создания автономного исполняемого файла серверного приложения.
"""
import PyInstaller.__main__
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_server():
    """Собирает серверное приложение в автономный исполняемый файл."""
    try:
        # Определение путей
        project_dir = os.path.dirname(os.path.abspath(__file__))  # Внутри server/compilate/
        server_dir = os.path.dirname(project_dir)  # Родительская директория (server/)
        env_file = os.path.join(server_dir, ".env")
        db_file = os.path.join(server_dir, "records.db")
        src_dir = os.path.join(server_dir, "src")
        hooks_dir = os.path.join(project_dir, "hooks")
        output_dir = os.path.join(project_dir, "dist", "server")  # Вывод в server/compilate/dist/server/

        # Подготовка аргументов для PyInstaller
        pyinstaller_args = [
            os.path.join(server_dir, "main.py"),  # Ссылка на main.py в server/
            "--onedir",
            "--name=server",
            f"--distpath={os.path.join(project_dir, 'dist')}",  # Вывод в server/compilate/dist/
            f"--workpath={os.path.join(project_dir, 'build')}",  # Сборка в server/compilate/build/
            f"--specpath={os.path.join(project_dir, 'spec')}",   # Spec в server/compilate/spec/
            f"--additional-hooks-dir={hooks_dir}",  # Добавляем наш хук
            "--noconfirm",
            "--clean",
            "--exclude-module=pytest",
            "--exclude-module=pytest_mock",
            "--exclude-module=httpx",
            "--exclude-module=_pytest"
        ]

        # Добавляем файлы данных, если они существуют
        if os.path.exists(env_file):
            pyinstaller_args.append(f"--add-data={env_file}{os.pathsep}.env")
        else:
            logger.warning(f"Файл окружения не найден: {env_file}")
            
        if os.path.exists(db_file):
            pyinstaller_args.append(f"--add-data={db_file}{os.pathsep}records.db")
        else:
            logger.info(f"Файл базы данных не найден (будет создан при первом запуске): {db_file}")
            
        # Добавляем директорию src
        if os.path.exists(src_dir):
            pyinstaller_args.append(f"--add-data={src_dir}{os.pathsep}src")
        else:
            logger.error(f"Директория с исходным кодом не найдена: {src_dir}")
            return False

        logger.info("Сборка серверного приложения...")
        
        # Команда PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)

        logger.info(f"Сервер успешно собран в {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Ошибка сборки сервера: {e}")
        return False

if __name__ == "__main__":
    success = build_server()
    if not success:
        sys.exit(1)