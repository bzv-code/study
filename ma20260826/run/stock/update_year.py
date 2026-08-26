import os
import re

# ======================================================
# 🎯 УКАЖИТЕ НУЖНЫЙ ГОД ЗДЕСЬ
# ======================================================

NEW_YEAR = 2011

# ======================================================
# СПИСОК ЦЕЛЕВЫХ ФАЙЛОВ
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


def main():
    print("=" * 60)
    print("🛠  УТИЛИТА МАССОВОЙ ЗАМЕНЫ ПЕРЕМЕННОЙ YEAR")
    print("=" * 60)
    print(f"\n📅 Установленный год: {NEW_YEAR}")

    # Регулярное выражение для строгого поиска
    pattern = re.compile(r'^(\s*YEAR\s*=\s*)\d{4}\b', re.MULTILINE)

    updated_count = 0
    skipped_count = 0
    missing_count = 0

    print("\n" + "-" * 60)

    # Обработка файлов
    for filename in SCRIPTS:
        if not os.path.exists(filename):
            print(f"⚠️  Файл не найден: {filename}")
            missing_count += 1
            continue

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Проверяем, есть ли что заменять
            if pattern.search(content):
                # Заменяем, сохраняя оригинальные пробелы
                new_content = pattern.sub(rf'\g<1>{NEW_YEAR}', content)

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"✅ Обновлено: {filename}")
                updated_count += 1
            else:
                print(f"⏭️  Пропущено (переменная YEAR не найдена): {filename}")
                skipped_count += 1

        except Exception as e:
            print(f"❌ Ошибка при обработке {filename}: {e}")

    # Итоговый отчет
    print("-" * 60)
    print("📊 ИТОГИ:")
    print(f"   ✅ Успешно обновлено файлов: {updated_count}")
    print(f"   ⏭️  Пропущено (не найдено YEAR): {skipped_count}")
    print(f"   ⚠️  Не найдено в папке: {missing_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()