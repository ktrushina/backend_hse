# Ad Moderation API

Минимальный HTTP API на FastAPI для предсказания нарушений в объявлении.

## Логика

`POST /predict` принимает JSON с полями `seller_id`, `is_verified_seller`, `item_id`, `name`, `description`, `category` и `images_qty`. Ответ — одно JSON булево значение:

- `false` — нарушений по наивному правилу нет;
- `true` — объявление считается нарушающим правило.

Подтверждённый продавец всегда получает `false`. Для неподтверждённого продавца результат `true` только при `images_qty == 0`.

## Структура

- `routers/predict.py` — HTTP-обработчик и перевод ошибок в HTTP-ответы;
- `services/predict.py` — сервисный слой;
- `repositories/prediction.py` — текущая реализация простого предсказания;
- `schemas/predict.py` — строгая проверка входных данных.

Ошибки валидации возвращаются с кодом `400`, непредвиденные ошибки предсказания — с кодом `500`.

## Установка и запуск

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
fastapi dev
```

Swagger UI доступен по адресу `http://127.0.0.1:8000/docs`.

## Тесты

```bash
pytest
```
