## Эксперименты с автоматическим оцениванием

**Установка библиотек:**
```bash
uv sync
```

**Просмотр JSON-файлов**: https://jsonviewer.stack.hu/


### Эксперимент 1: простой критериальный подход

По каждому критерию проверяется его соблюдение с использованием CoT+SO

**Запуск оценивания:**
```bash
uv run python -m experiments.exp1.run 
```

**Запуск тестов:**
```bash
uv run pytest experiments/exp1/test_solution.py -sv
```

### Эксперимент 2: оценка кода на метауровне


**Запуск оценивания:**
```bash
uv run python -m experiments.exp2.run 
```

