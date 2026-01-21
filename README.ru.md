# Task Registry (Реестр Задач)

[English](README.md) | **Русский**

Универсальная система управления конфигурациями и реестрами для ML-проектов, построенная на базе Pydantic v2 и принципах динамической композиции.

## Особенности
- **Строгая валидация**: Использование Pydantic v2 для проверки типов и логической связности данных.
- **Динамическая композиция**: Поддержка различных источников кода (Local, Git, PyPI) через схему `DependencySource`.
- **Режимы исполнения (RUN_MODE)**: Бесшовное переключение между `dev` (локальная разработка с оверлеями) и `prod` (стабильные релизы).
- **Атомарность**: Каждый компонент (задача, датасет, метрика) описывается отдельным YAML-файлом.
- **LEGO-style архитектура**: Пакет полностью автономен и может быть использован в любом проекте независимо от VLMHyperBench.

## Установка
Требуется Python 3.13+ и [uv](https://github.com/astral-sh/uv).

```bash
uv pip install git+https://github.com/VLMHyperBenchTeam/task-registry.git
```

## Быстрый старт
Пример использования `RegistryManager`:

```python
from task_registry.manager import RegistryManager

# Инициализация менеджера (укажите путь к вашим YAML-реестрам)
manager = RegistryManager(root_dir="path/to/registries", run_mode="dev")

# Получение и валидация задачи
task = manager.get_task("VQA")
print(f"Загружена задача: {task.name}, точка входа: {task.entry_point}")
```

## Структура реестров
Рекомендуемая структура папок:
```text
registries/
├── packages/    # Описание источников пакетов
├── tasks/       # Типы задач (MLTask)
├── metrics/     # Инстансы метрик
├── datasets/    # Описание данных
└── runs/        # Конкретные запуски
```

## Лицензия
MIT