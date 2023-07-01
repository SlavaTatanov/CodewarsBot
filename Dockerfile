# Определяем базовый образ
FROM python:3.11-slim

# Устанавливаем переменную для поиска модулей приложения
ENV PYTHONPATH="$PYTHONPATH:/app"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения
COPY . .

# Запускаем бот
CMD python3 CodewarsTelegramBot/main.py