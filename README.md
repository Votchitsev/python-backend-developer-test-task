# Тестовое задание на позицию Python Backend Developer
###### https://kaliningrad.hh.ru/vacancy/78542200?from=main&hhtmFromLabel=applicant_recommended_vacancies&hhtmFrom=main

### Задание 
* Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку.
* После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
* Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
* Обязательно 100% покрытие тестами

### Описание выполненного задания
Скрипт запускается командой `python3 main.py`. В результате его выполнения в директории result создаются три директории: "Task1", "Task2", "Task3", которые содержат файлы содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration. В этой же директории создаётся файл `hash.txt`, который содержит хэш-суммы каждого файла.

Тесты запускаются командой `pytest`.