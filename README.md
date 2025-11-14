# Маленький сервис расчёта стоимости изделия

# Как запустить

## Клонируйте репозиторий

```
git clone https://github.com/Nikitkosss/cost_product_api.git
cd cost_product_api
```

## Убедитесь, что у вас есть .env файл с переменными:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
POSTGRES_PORT=port
POSTGRES_SERVER=host
```

## Запуск через Docker

```
docker compose up --build
```

## Или создайте и активируйте виртуальное окружение python 3.11 (рекомендуется)

```
python -m venv venv
source venv/bin/activate    # Linux/macOS
# или
venv\Scripts\activate       # Windows
```

## Установите зависимости

```
pip install -r requirements.txt
```

## Запустите сервер

```
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Сервер будет доступен по адресу: http://127.0.0.1:8000
### Документация Swagger UI: http://127.0.0.1:8000/docs 

## Доступные эндпоинты:
### Расчёта стоимости изделия
```curl -X 'POST' \
  'http://127.0.0.1:8000/api/product/calc' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "materials": [
    {"name": "steel", "qty": 120, "price_rub": 54.5},
    {"name": "copper", "qty": 12.3, "price_rub": 640.0}
  ]
}'
```
### Ответ:
```
{
  "total_cost_rub": 14412
}
```
### Возвращает 10 последних расчётов отсортированных по дате (default = 10, в примере limit: Optional[int] = 1)
```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/product/calc?limit=1' \
  -H 'accept: application/json'
```
### Ответ:
```
[
  {
    "id": 9,
    "total_cost_rub": 14412,
    "created_at": "2025-11-14T08:15:35.788620"
  }
]
```
# Ответы на вопросы:

## Вопрос №1

### 1. Структура каталогов сервиса
```
cost_product_api/
├── logs/
│   └── .gitkeep
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── calc_routers.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── calc_schemas.py
│   │   └── extended_base_model.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── calc_service.py
│   │   └── uow.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── middleware.py
│   │   └── setup_logger.py
│   ├── __init__.py
│   └── main.py
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── config.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```
### 2. Где должна находиться бизнес-логика и почему

Ответ: Бизнес-логика должна находиться в папке services/.

Почему:

Это позволяет изолировать логику, что упрощает тестирование отдельно от API. Также позволяет использовать функции повторно.

### 3. Как организовать конфигурацию (env)

Ответ: Использовать к примеру BaseSettings которая позволяет читать переменные окружения в виде Pydantic-моделей


### 4. Как и чем логировать

Ответ: К примеру использовать logging.
Логировать вход/выход из эндпоинтов или прокидывать по всему кудо логи, если нужно остлеживать более сложную логику выполнения


### 5. Как обрабатывать ошибки (ошибки валидации / ошибки БД)

Ответ: Ошибки валидации можно отлавливать через Pydantic, прочие ошибки можно отлавливать через middleware

## Вопрос №2

### 1. Почему здесь есть проблема со стоимостью?

Ответ: 100 kg по 23.5 = 2350, 0.1 ton = 100 kg, но по цене 2.35, т.е. 0.1 ton стоит 0.235 — это противоречие.
Цена за тонну (2350) != цена за 100 кг (2350), но в строке с ton цена за 100 кг указана как 2.35 — непоследовательность.

### 2. Как привести unit к единой системе?

Ответ: Привести все unit к базовой единице (например, kg):
1 ton = 1000 kg
1 kg = 1 kg
Пересчитать unit_cost относительно kg.

### 3. Куда в архитектуре должен быть вынесен мэппинг единиц измерения?

Ответ: В отдельную таблицу в БД, чтобы:
Не хардкодить в коде.
Либо если мэппинг чуть-чуть можно вынести в config, чтобы не раскидывать по коду и иметь быстрый доступ. 

### 4. Как убедиться, что новые данные не сломают консистентность?

Ответ:
Использовать Pydantic
Использовать ограничения в БД (CHECK, FK).
Писать тесты
