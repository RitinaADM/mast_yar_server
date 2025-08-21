# 📌 YAR Mast — Server

Серверная часть тестового задания на **FastAPI** с использованием принципов **гексагональной архитектуры**.
Реализует REST API для сохранения и чтения записей с пагинацией.

---

## 🚀 Стек технологий

* [Python 3.12+](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/) — HTTP API
* [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
* [Pydantic](https://docs.pydantic.dev/) — валидация моделей
* [Uvicorn](https://www.uvicorn.org/) — ASGI сервер
* [Pytest](https://docs.pytest.org/) — тестирование
* [python-dotenv](https://pypi.org/project/python-dotenv/) — переменные окружения

---

## 📂 Структура проекта

```
server/
│── .env               # Переменные окружения (боевые)
│── .env.example       # Пример env-файла
│── main.py            # Точка входа (запуск FastAPI)
│── requirements.txt   # Зависимости
│── src/
│   ├── application/   # Сервисы и use cases
│   ├── domain/        # Доменные модели, порты, исключения
│   └── infrastructure/# Адаптеры, конфиг, DI
│── tests/             # Unit и integration тесты
```

---

## ⚙️ Установка и запуск

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/RitinaADM/yar_mast_server.git
   cd yar_mast_server
   ```

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создать `.env` (по примеру `.env.example`):

   ```ini
   HOST=127.0.0.1
   PORT=8000
   DB_URL=sqlite:///records.db
   ```

4. Запустить сервер:

   ```bash
   python main.py
   ```

   Сервер будет доступен по адресу:
   👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

5. Документация API доступна по адресу:
   👉 [Swagger UI](http://127.0.0.1:8000/docs)
   👉 [ReDoc](http://127.0.0.1:8000/redoc)

---

## 📡 API

### ➕ Создать запись

**POST** `/records`

```json
{
  "text": "example",
  "date": "2025-08-20",
  "time": "12:00:00",
  "click_number": 1
}
```

✅ Ответ:

```json
{"status": "success"}
```

---

### 📖 Получить записи (с пагинацией)

**GET** `/records?page=1&limit=10`
✅ Ответ:

```json
{
  "records": [
    {
      "id": 1,
      "text": "example",
      "date": "2025-08-20",
      "time": "12:00:00",
      "click_number": 1
    }
  ],
  "total": 1
}
```

---

## 🧪 Тесты

Запуск тестов:

```bash
pytest tests -v
```

---

## 🔑 Особенности реализации

* Архитектура: **Hexagonal (Ports & Adapters)**
* Полностью вынесенные конфигурации (`.env` + `settings.py`)
* Покрытие тестами: unit + integration
* Логирование запросов и ошибок

---

## 👨‍💻 Автор

**@RitinaADM**
👉 [GitHub](https://github.com/RitinaADM)

---