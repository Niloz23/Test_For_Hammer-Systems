# Устанавливаем базовый образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для доступа
EXPOSE 8000

# Команда запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
