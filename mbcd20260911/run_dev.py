"""
Единая точка запуска для локальной разработки: поднимает backend (uvicorn) и бота
(maxapi) одновременно.

Технически это два отдельных процесса, а не один — у бота и backend одноимённые
пакеты `app`, так что "по-настоящему" слить их в один процесс с общим импортом
нельзя. Зато по отдельным процессам всё устроено ровно так же, как в проде: bot
и backend — разные сервисы, просто здесь их запускает и следит за ними один скрипт.

Запуск:
    python run_dev.py

Остановка:
    Ctrl+C — оба процесса завершатся вместе.
"""
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / "backend"
BOT_DIR = PROJECT_ROOT / "bot"


def main() -> None:
    python_exe = sys.executable

    print("Запускаю backend (uvicorn, http://localhost:8000)...")
    backend_proc = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "api_app.main:app", "--reload", "--port", "8000"],
        cwd=str(BACKEND_DIR),
    )

    print("Запускаю бота (maxapi)...")
    bot_proc = subprocess.Popen(
        [python_exe, "-m", "bot_app.main"],
        cwd=str(BOT_DIR),
    )

    print(f"\nbackend PID={backend_proc.pid}")
    print(f"bot PID={bot_proc.pid}")
    print("Нажмите Ctrl+C, чтобы остановить оба процесса.\n")

    try:
        while True:
            if backend_proc.poll() is not None:
                print(f"backend неожиданно завершился с кодом {backend_proc.returncode}")
                break
            if bot_proc.poll() is not None:
                print(f"бот неожиданно завершился с кодом {bot_proc.returncode}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстанавливаю оба процесса...")
    finally:
        for proc in (backend_proc, bot_proc):
            if proc.poll() is None:
                proc.terminate()
        for proc in (backend_proc, bot_proc):
            proc.wait()
        print("Оба процесса остановлены.")


if __name__ == "__main__":
    main()
