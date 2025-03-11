## Логи автотестов (pytest)
============================= test session starts =============================
platform win32 -- Python 3.11.11, pytest-8.3.5, pluggy-1.5.0
rootdir: C:\Users\user\PycharmProjects\LLM-Based-Router
configfile: pyproject.toml
plugins: anyio-4.8.0, langsmith-0.3.13
collected 2 items

tests\test_code.py FF                                                    [100%]

================================== FAILURES ===================================
______________________________ test_correctness _______________________________

dataset = [['Что вообще нужно собрать для поступления в магистратуру?', '1'], ['Нужно ли делать портфолио, и что в него включать...ть документы на несколько программ сразу?', '1'], ['Можно ли подавать документы, если диплом еще не готов?', '1'], ...]

    def test_correctness(dataset):
        dataset_sample = random.sample(dataset, SAMPLE_SIZE)
        errors = []
        for row in dataset_sample:
            query = row[0]
            expected_topic = int(row[1])
            predicted_topic = router(query)
            time.sleep(1)
            if expected_topic != predicted_topic:
                errors.append(f"Для запроса \"{query}\" ожидалось {expected_topic}, получено {predicted_topic}")
>       assert len(errors) == 0, "\n".join(errors)
E       AssertionError: Для запроса "Какой объем практики предусмотрен в учебном плане?" ожидалось 3, получено 4
E         Для запроса "Можно ли сдавать испытания дистанционно?" ожидалось 2, получено 5
E         Для запроса "Будут ли курсы от ШАДа?" ожидалось 3, получено 4
E         Для запроса "Мне напишут, когда начнется сезон стажировок?" ожидалось 4, получено 2
E         Для запроса "Правда, что в маге можно выбирать дисциплины?" ожидалось 3, получено 2
E         Для запроса "Как подготовиться к практическим заданиям на вступительных испытаниях?" ожидалось 2, получено 3
E         Для запроса "Как часто набирают на стажировки?" ожидалось 4, получено 5
E         Для запроса "Какие темы охватываются в курсе машинного обучения?" ожидалось 3, получено 5
E       assert 8 == 0
E        +  where 8 = len(['Для запроса "Какой объем практики предусмотрен в учебном плане?" ожидалось 3, получено 4', 'Для запроса "Можно ли сд...', 'Для запроса "Как подготовиться к практическим заданиям на вступительных испытаниях?" ожидалось 2, получено 3', ...])

tests\test_code.py:23: AssertionError
______________________________ test_reliability _______________________________

dataset = [['Что вообще нужно собрать для поступления в магистратуру?', '1'], ['Нужно ли делать портфолио, и что в него включать...ть документы на несколько программ сразу?', '1'], ['Можно ли подавать документы, если диплом еще не готов?', '1'], ...]

    def test_reliability(dataset):
        row = dataset[0]
        query = row[0]
        result1 = router(query)
        time.sleep(1)
        result2 = router(query)
        time.sleep(1)
>       assert result1 == result2, f"Результат детекции не стабилен для запроса \"{query}\""
E       AssertionError: Результат детекции не стабилен для запроса "Что вообще нужно собрать для поступления в магистратуру?"
E       assert 4 == 1

tests\test_code.py:33: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_code.py::test_correctness - AssertionError: Для запроса "Ка...
FAILED tests/test_code.py::test_reliability - AssertionError: Результат детек...
============================= 2 failed in 12.09s ==============================

## Логи линтеров (ruff)
All checks passed!

## Структура проекта студента

- router.py

## Код проекта студент

Содержимое файла router.py
```Python
from typing import Literal, cast

Topic = Literal[1, 2, 3, 4, 5]


def router(query: str) -> Topic:
    return cast(Topic, 1)

```
