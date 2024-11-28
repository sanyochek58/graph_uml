Проект с построением графа зависимостей


https://github.com/sanyochek58/graph_uml


Задание 


Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. 
Сторонние средства дляполучения зависимостей использовать нельзя.
Зависимости определяются для git-репозитория. Для описания графа зависимостей используется представление PlantUML. 
Визуализатор должен выводить результат в виде сообщения об успешном выполнении и сохранять графв файле формата png.


Построить граф зависимостей для коммитов, в узлах которого находятся
списки файлов и папок. Граф необходимо строить для ветки с заданным именем.
Конфигурационный файл имеет формат csv и содержит:


• Путь к программе для визуализации графов.


• Путь к анализируемому репозиторию.


• Путь к файлу с изображением графа зависимостей.


• Имя ветки в репозитории.


Все функции визуализатора зависимостей должны быть покрыты тестами.


Структура файлов в проекте:


main.py - Главный файл с кодом, где мы заполняем файл с зависимости коммитов, которыми в процессе будем составлять граф


tests.py - Файл с тестами 


config.csv - Конфигурационный файл с путями к : визуализатору(plantuml), гит-репозиторию, созданию картинки графа, название ветки


plantuml.jar - Визуализатор графа


graph.uml - Файл зависимостей графа


Запустим тесты и посмотрим корректность работы программы:


![Снимок экрана 2024-11-20 231351](https://github.com/user-attachments/assets/7602891a-71d2-4618-addf-677d170bf738)


Выведем картинку графа:


![graph](https://github.com/user-attachments/assets/72e6cc5a-0fcc-44c3-b0ed-bb39bb9fc0d6)





![graph](https://github.com/user-attachments/assets/2b5dc906-8d5c-491e-944d-f31593ffa5f2)
