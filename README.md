# Писарь
Программа для генерации документов ВС РФ для одного или нескольких военнослужащих.

Можно создавать группы документов по конкретным темам:
* Служебное разбирательство по факту грубого дисциплинарного проступка
	* Служебное разбирательство (сам документ)
	* Акт о невозможности получения копии протокола о ГДП
	* Акт о невозможности взять объяснение
	* Служебная характеристика
	
## Установка для Windows
Необходимо установить программное обеспечение (нужны права администратора):
* Python 3.10. Среда исполнения. Нужна именно 3.10, потому что более старшие версии имеют проблему совместимости с библиотекой. [Скачать](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe). На первом окне, что появляется во время установки, поставьте галочку "Add to PATH...". Это позволит запускать скрипты из командной строки.
* Git. Через эту систему контроля версий будут скачиваться обновления. [Скачать](https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.1/Git-2.41.0-64-bit.exe)	

Проверить правильность установки программного обеспечения можно так:
* В командной строке наберите: python --version. Будет напечатана строка: Python 3.10.
* В командной строке наберите: git --version. Будет напечатана строка: git version ... (установленная версия).


Установка Писаря происходит так:
1. Откройте поиск в Windows (значок лупы в левом нижнем углу, рядом с кнопкой "Пуск"). Наберите "cmd" и нажмите Enter. Запустится командная строка (черный экран с курсором).
2. Скопируйте: git clone https://github.com/ivasiliev/pisar.git c:/pisar
3. На командной строке (черный экран) нажмите правую кнопку мыши. Строка будет вставлена. Нажмите Enter.
4. Появится служебная информация касательно скачанных файлов и Писарь появится в `c:\pisar`.
5. Через Проводник Windows зайдите в папку `c:\pisar\pisar\install\`.
6. Двойным кликом левой кнопки мыши запустите файл `install.bat`.
7. Этот командный файл создаст две папки: `c:\pisar_data\` и `c:\pisar_output\`. В первую папку скопирует файлы настройки для документов и демо Штатного расписания. Вторая папка пуста: в ней будут создаваться сгенерированные документы. Помимо папок, командный файл установит необходимые библиотеки.
8. Кликните правой кнопкой мыши на файл `pisar.bat`, выберите "Отправить", "На рабочий стол (создать ярлык)".


Теперь Писарь готов к запуску.

## Начало работы
Двойным кликом левой кнопки мыши запустите ярлык на Рабочем столе (pisar.bat) либо же сам командный файл. Откроется командная строка (черный экран), а поверх него -- окно приложения. Не закрывайте командную строку! Все действия Писаря происходят в ней, а приложение лишь оболочка.

В приложении есть кнопка "Обновить". Рекомендуем запускать регулярное обновление программы. При этом в командной строке будет выведена информация. Если это "up to date", то вы используете последнюю версию программы. После обновления программы, перезапустите её. Тогда изменения вступят в силу.

Ниже расположены тематические группы документов. Рассмотрим первую из них в качестве примера ("Служебное разбирательство по факту грубого дисциплинарного проступка"). Работа с остальными аналогична.

В группе есть две кнопки: "Настройки" и "Запуск". Нажмите "Настройки". Откроется текстовый файл в формате json (произносится как "джейсон"). Эти данные, а также сведения из Штатного расписания будут подставляться в генерируемые документы. Вот что они означают:
* `personnel_path`. Путь к файлу Excel со Штатным расписанием ("personnel" переводится как "личный состав"). Вместе с Писарем поставляется демонстрационный набор данных. Все имена вымышлены. Нужно создать собственный файл с теми же столбцами и указать путь к нему. Максимальное количество военнослужащих в Штатном расписании составляет 2000.
* `soldier_ids`. В Штатном расписании первая колонка содержит номера военнослужащих. Здесь можно указать один или несколько номеров через запятую. Документы будут созданы для каждого военнослужащего.
* `date_of_event`. Дата происшествия в формате "ДД.ММ.ГГГГ".
* `military_unit`. Номер воинской части.
* `is_guard`. Если часть гвардейская, то True. Иначе, False. Это нужно для правильного вычисления званий военнослужащих.
* `nationality`. "Национальность" для Служебной характеристики. Со временем будет перенесено в Штатное расписание.
* `education`. "Образование" для Служебной характеристики. Со временем будет перенесено в Штатное расписание.
* `year_service_started`. "Год начала службы в ВС ДНР" для Служебной характеристики. Со временем будет перенесено в Штатное расписание.
* `commander_platoon`. Сведения о командире взвода для военнослужащего из `soldier_ids`. Если требуется создать документы для группы военнослужащих из разных взводов, то лучше делать это по очереди. 
* `commander_company`. Сведения о командире роты для военнослужащего из `soldier_ids`.
* `commander_1_level`, `commander_2_level`, `commander_3_level`, `commander_4_level`. Сведения о вышестоящих командирах.

Данные из файлов настройки и Штатного расписания не передаются на другие компьютеры. В званиях следует писать "рядовой", "лейтенант" и т.п., не прибавляя "гвардии". Это будет сделано автоматически.

Для командиров взводов и рот нет нужды указывать номер взвода и роты. Они будут взяты от военнослужащего `soldier_ids` из Штатного расписания.

Сохраните изменения и закройте файл настройки. Каждой группе документов соответствует свой файл настройки. Они находятся в каталоге `c:\pisar_data\`. Их можно редактировать вручную при помощи текстового редактора, не прибегая к запуску Писаря. Например, файл настройки для "Служебное разбирательство по факту грубого дисциплинарного проступка" называется batch_official_proceeding.json.

Когда файл настройки готов, нажмите кнопку "Запуск" и наблюдайте за окном с командной строкой. Там отображается подробная информация о создании документов. В случае успеха, документы появятся в каталоге `c:\pisar_output\`. В названии документа в скобках указано имя военнослужащего, которому он посвящён.

Если командир роты или взвода не задан, то будет выведена "заглушка" в виде [ФИО РОТНОГО КОМАНДИРА] и подобных. В таком случае сведения надо внести вручную. 

После генерации документов, внимательно их проверьте. Рекомендуем скопировать полученные документы в другую папку, потому что при следующей генерации они будут перезаписаны без дополнительных уведомлений.

**Ни при каких обстоятельствах не пересылайте Штатное расписание либо другие "чувствительные" данные разработчикам программы.**

## Известные проблемы и недостатки

Мы исправим их так скоро, как возможно.

* Некоторые слова склоняются неверно. Например, "стрелок". Необходимо проверять документы после генерации.
* Склонение имен производится корректно для лиц мужского пола. Для лиц женского пола могут быть ошибки.
* Персональные сведения "национальность", "образование", "год начала службы в ВС ДНР" должны быть перемещены в Штатное расписание. Однако эта возможность пока не поддерживается.
* Пока не удалось найти простого и удобного способа соединить военнослужащего с его командирами взвода и роты. Потому эти настройки из Штатного расписания перенесены в файл настройки.

## Обновления программы
**1.4 | 00.06.2023**

* Расшифровка аббревиатуры ВРИО в документе "Служебное разбирательство" в резолютивной части и правильное склонение.
* Исправлена ошибка с поиском несуществующего военнослужащего.

**1.3 | 15.06.2023**

* Отныне в файле Штатного расписания обязан присутствовать лист `ШБС`. На этом листе следует расположить таблицу с данными военнослужащих. Остальные листы книги Excel игнорируются. Файл personnel_demo.xlsx имеет правильную структуру.
* Существенно улучшена производительность программы при работе с большими файлами Штатного расписания.
* Нормализация имён военнослужащих. Например, "ФРОЛОВ ЕВГЕНИЙ МИХАЙЛОВИЧ" будет преобразован в "Фролов Евгений Михайлович". Это преобразование происходит только для людей из Штатного расписания.
* При обновлении программы файл personnel_demo.xlsx копируется в C:\pisar_data. Будьте осторожны -- это может перезаписать ваши данные. Не следует изменять файл personnel_demo.xlsx, поскольку он используется как образец. 
* При обновлении программа проверяет версию. Если версия изменилась, то в командной строке выводится приглашение перезапустить программу. Что и следует сделать.

**1.2 | 13.06.2023**

Отныне в номерах рот можно указывать буквы и цифры. Исправлена ошибка с чтением дат из ШР. Поддерживаются ячейки типа "Дата".

**1.1 | 10.06.2023**

Исправлена ошибка с неверным путем к файлу настройки.

**1.0 | 08.06.2023**

Первая версия

	