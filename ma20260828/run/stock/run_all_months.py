from __future__ import annotations

import subprocess
import sys
import time
import signal
from datetime import datetime

# ======================================================
# СПИСОК СКРИПТОВ
# ======================================================

SCRIPTS = [
    "01_run_stock_m1_yanvar.py",
    "02_run_stock_m1_fevral.py",
    "03_run_stock_m1_mart.py",
    "04_run_stock_m1_aprel.py",
    "05_run_stock_m1_mai.py",
    "06_run_stock_m1_iyun.py",
    "07_run_stock_m1_iyul.py",
    "08_run_stock_m1_avgust.py",
    "09_run_stock_m1_sentyabr.py",
    "10_run_stock_m1_oktyabr.py",
    "11_run_stock_m1_noyabr.py",
    "12_run_stock_m1_dekabr.py",
]

PAUSE_SECONDS = 20

# ======================================================
# ОБРАБОТКА СИГНАЛОВ ОСТАНОВКИ (Ctrl+C)
# ======================================================

stop_requested = False
current_process: subprocess.Popen | None = None


def signal_handler(signum, frame):
    global stop_requested, current_process
    print(f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] ПОЛУЧЕН СИГНАЛ ОСТАНОВКИ. Завершаем...")
    stop_requested = True
    if current_process and current_process.poll() is None:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Отправляем сигнал завершения дочернему процессу...")
        current_process.terminate()
        try:
            current_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Дочерний процесс не остановился, убиваем...")
            current_process.kill()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# ======================================================
# ЗАПУСК СКРИПТОВ
# ======================================================

def run_scripts():
    total = len(SCRIPTS)
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] НАЧАЛО ЗАПУСКА {total} СКРИПТОВ")
    print("=" * 70)

    for i, script in enumerate(SCRIPTS, start=1):
        if stop_requested:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ОСТАНОВКА ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ")
            break

        print(f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] ЗАПУСК [{i}/{total}]: {script}")
        print("-" * 70)

        start_time = time.time()

        try:
            # Запускаем скрипт, передавая ему вывод в реальном времени
            current_process = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            # Читаем и печатаем вывод скрипта в реальном времени
            for line in current_process.stdout:
                if stop_requested:
                    break
                print(line, end="", flush=True)

            current_process.wait()
            elapsed = time.time() - start_time

            if current_process.returncode == 0:
                print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ✅ УСПЕШНО ЗАВЕРШЕН: {script} (за {elapsed:.1f}с)")
            else:
                print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ❌ ОШИБКА (код {current_process.returncode}): {script}")

        except Exception as e:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 💥 КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ {script}: {e}")

        current_process = None

        # Пауза между скриптами (кроме последнего)
        if i < total and not stop_requested:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ⏸️  ПАУЗА {PAUSE_SECONDS} СЕКУНД...")
            for remaining in range(PAUSE_SECONDS, 0, -1):
                if stop_requested:
                    print(f"\n[{datetime.now():%Y-%m-%d %H:%M:%S}] Пауза прервана.")
                    break
                print(f"\r[Осталось: {remaining}с]   ", end="", flush=True)
                time.sleep(1)
            if not stop_requested:
                print()  # Перевод строки после таймера

    print("\n" + "=" * 70)
    if stop_requested:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ЗАПУСК ПРЕРВАН ПОЛЬЗОВАТЕЛЕМ")
    else:
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ВСЕ СКРИПТЫ ОБРАБОТАНЫ")


if __name__ == "__main__":
    run_scripts()