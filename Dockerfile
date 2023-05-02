FROM python:3.11-alpine3.17

COPY requirements.txt /temp/requirements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN pip install -r /temp/requirements.txt
# Создаем пользователя service-user без пароля
RUN adduser --disabled-password service-user

# Запуск команд от пользователя service-user
USER service-user