from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Тут повинен бути ваш код
    # Перетворюємо словники у dataclass
    jobs = [PrintJob(**job) for job in print_jobs]
    limits = PrinterConstraints(**constraints)

    # Сортуємо за пріоритетом (1 — найвищий)
    jobs.sort(key=lambda x: x.priority)

    total_time = 0
    print_order = []

    i = 0
    n = len(jobs)

    while i < n:
        group = []
        group_volume = 0
        group_items = 0
        max_time = 0

        j = i
        while j < n:
            job = jobs[j]
            if (
                group_volume + job.volume <= limits.max_volume
                and group_items + 1 <= limits.max_items
            ):
                group.append(job)
                group_volume += job.volume
                group_items += 1
                max_time = max(max_time, job.print_time)
                j += 1
            else:
                break

        print_order.extend([job.id for job in group])
        total_time += max_time
        i += len(group)

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {
            "id": "M1",
            "volume": 100,
            "priority": 2,
            "print_time": 120
        },  # лабораторна
        {
            "id": "M2",
            "volume": 150,
            "priority": 1,
            "print_time": 90
        },  # дипломна
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150
        }  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
