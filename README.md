 # Задание 1
 # Эмулятор оболочки ОС

Этот проект представляет собой эмулятор оболочки ОС, который работает с виртуальной файловой системой, запакованной в формате zip. Эмулятор поддерживает несколько команд и запускается из реальной командной строки.

## Требования

- Python 3.x
- Библиотека `unittest` (входит в стандартную библиотеку Python)

## Установка

Скачайте или клонируйте репозиторий:

Убедитесь, что у вас установлен Python 3.x.

## Конфигурация

Создайте файл config.csv с конфигурацией эмулятора. Пример содержимого файла:

```sh
username,hostname,vfs_path,startup_script
user,virtualhost,vfs.zip,/startup.sh
```
## Виртуальная файловая система

Создайте архив vfs.zip, содержащий виртуальную файловую систему. Пример структуры архива:

vfs.zip

├── startup.sh

├── testfile.txt

└── dir1

  └── file1.txt
    

Пример содержимого файлов:

startup.sh

ls /

uname

testfile.txt


line1

line2

line3

dir1/file1.txt


This is a test file in dir1.

## Запуск эмулятора

Запустите эмулятор, указав путь к файлу конфигурации:
```sh
python virtual_shell.py config.csv
```
## Команды

Эмулятор поддерживает следующие команды:

ls: Список файлов и директорий.
cd: Смена текущей директории.

exit: Выход из эмулятора.

uname: Вывод имени операционной системы.

tac: Вывод содержимого файла в обратном порядке строк.

rev: Вывод содержимого файла в обратном порядке символов.

## Тестирование
Для запуска тестов используйте следующую команду:

```sh
python test_virtual_shell.py
```
Тесты проверяют работу команд ls, cd, uname, tac и rev.


# Домашнее задание №2 Вариант 5

## Описание
Данный проект представляет собой набор функций на Python, предназначенных для работы с Git-репозиториями. Программа позволяет извлекать информацию о коммитах, измененных файлах и формировать граф коммитов в формате, удобном для визуализации. Проект использует стандартные библиотеки Python, такие как subprocess и configparser, что делает его легким в использовании и интеграции.

## Описание функций

### Функции:
- load_config(config_path): Читает конфигурационный файл и возвращает настройки в виде словаря.
  
- get_git_commits(repo_path): Получает список всех коммитов в репозитории с их сообщениями, возвращая их в виде списка строк.

- get_files_from_commit(commit, repo_path): Извлекает измененные файлы для конкретного коммита, возвращая их в виде списка строк.

- build_mermaid_graph(repo_path): Строит граф коммитов в формате Mermaid, возвращая его в виде списка строк. Граф включает коммиты и их родительские связи.

- save_graph_to_file(graph, output_file): Сохраняет код графа в указанный файл.
git add .
git commit -m "commit1"
python3 DependencyVisualizer.py

git add . 
git commit -m "commit2" 
python3 DependencyVisualizer.py

git add . 
git commit -m "commit3" 
python3 DependencyVisualizer.py


repo_path и output_path зависят от того, где директория проекта сохраняется.

## Переменные и настройки
- config_path: Путь к конфигурационному файлу config.ini, содержащему настройки для визуализации и путь к репозиторию.
- visualization_path: Путь к программе для визуализации графов.
- repo_path: Путь к Git-репозиторию, из которого извлекается информация о коммитах.
- output_path: Путь к файлу, в который будет сохранен код графа.
-graphviz_path=/usr/bin/dot


## Описание команд для сборки проекта
Для работы с проектом вам потребуется Python, установленный на вашей системе.

### Установка зависимостей
Не требуется установка дополнительных библиотек, так как используются стандартные библиотеки Python.

### Запуск приложения
1. Убедитесь, что у вас есть доступ к Git-репозиторию с необходимыми объектами. Важно: имена папок внутри Git-репозитория должны быть написаны латиницей!
2. Сохраните код в файл, например, git_graph.py.
3. Создайте конфигурационный файл config.ini с необходимыми параметрами.
4. Откройте терминал или командную строку и выполните команду:
   
   python git_graph.py
   
   Замените git_graph.py на имя вашего файла с кодом.


## Тестирование
### Тесты функциональности:
- Тест load_config: Функция корректно загружает настройки из конфигурационного файла.
- Тест get_git_commits: Успешное получение списка всех коммитов с сообщениями.
- Тест get_files_from_commit: Корректное извлечение измененных файлов для указанного коммита.
- Тест build_mermaid_graph: Успешное построение графа коммитов с правильными родительскими связями.
- Тест save_graph_to_file: Корректное сохранение графа в указанный файл.

### Результат работы программы-тестировщика:
![](https://github.com/AntoshkA-30I/config-2/blob/main/images/test%20program.png) 
### Ручное тестирование:









# Домашнее задание №3 Вариант 5 

## Описание

Данный инструмент командной строки предназначен для преобразования текстовых конфигураций, написанных на учебном конфигурационном языке, в формат yaml. Инструмент принимает входной текст из файла, путь к которому задается через ключ командной строки. Если в процессе обработки входного текста возникают синтаксические ошибки, инструмент выдает соответствующие сообщения об ошибках.

## Синтаксис учебного конфигурационного языка

Однострочные комментарии:
// Это однострочный комментарий

Словари:
struct {
    имя = значение,
    имя = значение,
    имя = значение,
    ...
}

Имена:
[_a-zA-Z][_a-zA-z0-9]*

Значения:
- Числа
- Словари

Объявление констант на этапе трансляции:
const имя = значение

Вычисление констант на этапе трансляции:
[имя]
global имя=значение


## Сборка и запуск проекта

Чтобы запустить инструмент, используйте следующую команду, указывая путь к вашему входному файлу с текстом на учебном конфигурационном языке: python emulator.py <config_path> Где <config_path> — это путь к входному файлу .txt.

## Примеры конфигурации сети

; Это пример конфигурации сети
global ip 19216801
global subnet_mask 2552552550

struct {
    hostname router,
    address [ip],
    mask [subnet_mask]
}


### Конфигурация пользователей
; Конфигурация пользователей
global default_password 1234

struct {
    user1 JohnDoe,
    password [default_password]
}


# Комментарий
о приложении #|
struct {
    app_name MyApp,
    settings struct {
        theme dark,
        version 1
    }
}



address: 19216801
hostname: router
mask: 2552552550

password: 1234
user1: JohnDoe


password: 1234
user1: JohnDoe








## Результаты тестирования
В процессе тестирования были созданы как обычные тесты, так и тесты на проверку ошибок. Все тесты прошли успешно, что подтверждает корректность работы инструмента и его устойчивость к различным сценариям использования. <br />

