# Использовать официальный образ родительского образа / слепка.
FROM python:3.9

# Установка рабочей директории, откуда выполняются команды внутри контейнера.
WORKDIR /cardgame

# Скопировать все файлы с локальной машины внутрь файловой системы виртуального образа.
COPY /backend .

# Запустить команду внутри образа, установка зависимостей.
RUN pip install --upgrade pip && pip install -r requirements.txt
#RUN chmod +x run.sh
# RUN chmod +x run.sh
# RUN chmod +x wait.sh

# Добавить мета-информацию к образу для открытия порта к прослушиванию.
#EXPOSE 8000 80 81

#RUN
#ENTRYPOINT ["/cardgame/backend/run.sh"]
# CMD bash run.sh
