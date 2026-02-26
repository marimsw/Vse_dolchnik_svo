import json
import os
import pandas as pd
from datetime import datetime


def simple_filter_to_excel():
    print("=" * 60)
    print("ПРОСТАЯ ФИЛЬТРАЦИЯ JSONL → EXCEL")
    print("=" * 60)

    # Ввод пути
    input_file = input("Введите путь к JSONL файлу: ").strip()
    input_file = input_file.strip('"').strip("'")

    if not os.path.exists(input_file):
        print(f"❌ Файл не найден!")
        return

    # Выходной файл
    output_excel = input("Введите имя Excel файла [Enter для 'svo_result.xlsx']: ").strip()
    if not output_excel:
        output_excel = "svo_result.xlsx"

    print(f"\n🚀 Обработка файла...")

    svo_data = []
    total = 0

    start_time = datetime.now()

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                total += 1

                try:
                    data = json.loads(line.strip())
                    if data.get('группа') == "Должник СВО":
                        svo_data.append(data)

                        if len(svo_data) % 1000 == 0:
                            print(f"  Найдено {len(svo_data):,} записей...")

                except json.JSONDecodeError:
                    continue

                if total % 1000000 == 0:
                    print(f"  Обработано {total:,} строк...")

        elapsed = datetime.now() - start_time

        print(f"\n📊 Результаты:")
        print(f"   Всего строк: {total:,}")
        print(f"   Найдено 'Должник СВО': {len(svo_data):,}")

        if svo_data:
            # Создаем DataFrame
            df = pd.DataFrame(svo_data)

            # Сохраняем в Excel
            print("   Сохранение в Excel...")
            df.to_excel(output_excel, index=False, engine='openpyxl')

            print(f"✅ Файл сохранен: {output_excel}")
            print(f"📊 Размер: {os.path.getsize(output_excel) / (1024 ** 2):.2f} МБ")
        else:
            print("❌ Записи не найдены!")

        print(f"⏱️  Время: {elapsed}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Прервано")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    simple_filter_to_excel()
