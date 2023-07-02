# Писарь
Программа для генерации документов ВС РФ.

Можно создавать группы документов:
* Служебное разбирательство по факту грубого дисциплинарного проступка (ГДП)
	* Служебное разбирательство (сам документ)
	* Протокол о ГДП
	* Акт о невозможности получения копии протокола о ГДП
	* Акт о невозможности взять объяснение
	* Служебная характеристика
	
* Служебное разбирательство по факту cамовольного оставления части (СОЧ)
	* Административное расследование по факту самовольного оставления части
	* Лист согласования
	* Письмо родственникам
	* Ориентировка
	* Приказ
	* Приказ Копия
	* Служебная карточка
	* Служебная характеристика
	* Справка
	
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

В приложении есть кнопка "Обновить". Рекомендуется запускать регулярное обновление программы. При этом в командной строке будет выведена информация. После обновления программы, перезапустите её. Тогда изменения вступят в силу.

Рядом с ней находятся кнопки "Войсковая часть" и "Военнослужащий". Нажатие на кнопку открывает соответствующий файл настройки. Оба файла находятся в каталоге C:\pisar_data\. Файл для военной части содержит общие реквизиты, используемые во всех документах. Файл для военнослужащего содержит информацию для конкретного человека, на которого создаются документы.

### Настройки "Войсковая часть" 
(файл  common_info.json)
* `personnel_path`. Путь к файлу Excel со Штатным расписанием ("personnel" переводится как "личный состав"). Вместе с Писарем поставляется демонстрационный набор данных. Все имена вымышлены. Нужно создать собственный файл с теми же столбцами и указать путь к нему. Максимальное количество военнослужащих в Штатном расписании составляет 2000.
* `output_path`. Путь к каталогу, где будут созданы документы.
* `military_unit`. Номер войсковой части.
* `military_unit_address`. Адрес войсковой части.
* `is_guard`. Если часть гвардейская, то True. Иначе, False. Это нужно для правильного вычисления званий военнослужащих.
* `battalion`. Батальон.
* `phone_contact_to_report`. Номер телефона, по которому следует сообщить о самовольно оставившем войсковую часть.
* `hr_officer`. Сведения о специалисте отдела кадров.
* `clerk`. Сведения о делопроизводителе.
* `commander_1_level`, `commander_2_level`, `commander_3_level`, `commander_4_level`. Сведения о вышестоящих командирах.

### Настройки "Военнослужащий"
(файл soldier_info.json)
* `soldier_ids`. В Штатном расписании первая колонка содержит номера военнослужащих. Здесь нужно указать номер военнослужащего.
* `date_of_event`. Дата происшествия в формате "ДД.ММ.ГГГГ".
* `nationality`. Национальность военнослужащего.
* `gender`. Пол военнослужащего. м = мужской. ж = женский.
* `education`. Уровень образования. Например, среднее специальное.
* `graduation_place`. Учебное заведение, которое окончил военнослужащий.
* `specialization`. Гражданская профессия.
* `occupation`. Сведения о местах работы.
* `foreign_languages`. Перечень иностранных языков, которыми владеет военнослужащий.
* `awards`. Перечень наград.
* `government_authority`. Является ли военнослужащий депутатом. Например, "да" или "нет".
* `foreign_countries_visited`. Перечень стран, которые посещал военнослужащий.
* `service_started`. Дата начала службы в ВС России, ДНР, ЛНР в формате "ДД.ММ.ГГГГ".
* `place_of_birth`. Место рождения.
* `home_address`. Домашний адрес.
* `passport`. Сведения о паспорте.
* `marital_status`. Семейный статус, например, холост.
* `criminal_status`. Сведения о криминальном прошлом, а также привлекался ли к дисциплинарной ответственности.
* `father_name`. ФИО отца военнослужащего. Может быть только имя и отчество.
* `mother_name`. ФИО матери военнослужащего. Может быть только имя и отчество.
* `commander_platoon`. Сведения о командире взвода. 
* `commander_company`. Сведения о командире роты.


Данные из файлов настройки и Штатного расписания не передаются на другие компьютеры.

В званиях следует писать "рядовой", "лейтенант" и т.п., не прибавляя "гвардии". Это будет сделано автоматически.

Для командиров взводов и рот нет нужды указывать номер взвода и роты. Они будут взяты из Штатного расписания относительно заданного военнослужащего.

Когда файлы настройки готовы, нажмите кнопку "Запуск" и наблюдайте за окном с командной строкой. Там отображается подробная информация о создании документов. В случае успеха, документы появятся в каталоге `c:\pisar_output\`. В названии документа в скобках указано имя военнослужащего, которому он посвящён.

Если командир роты или взвода не задан, то будет выведена "заглушка" в виде [ФИО РОТНОГО КОМАНДИРА] и подобных. В таком случае сведения надо внести вручную. 

После генерации документов, внимательно их проверьте. Рекомендуется скопировать полученные документы в другую папку, потому что при следующей генерации они будут перезаписаны без дополнительных уведомлений.

**Ни при каких обстоятельствах не пересылайте Штатное расписание либо другие "чувствительные" данные разработчикам программы.**

## Известные проблемы и недостатки

* В документе "Протокол о ГДП" необходимо вручную ввести подчеркивания в нужные строки.
* Некоторые слова склоняются неверно. Например, "стрелок". Необходимо проверять документы после генерации.
* Персональные сведения "национальность", "образование" и подобные должны быть перемещены в Штатное расписание. Однако эта возможность пока не поддерживается.
* Пока не удалось найти простого и удобного способа соединить военнослужащего с его командирами взвода и роты. Потому эти настройки из Штатного расписания перенесены в файл настройки.

## Обновления программы
**1.9 | 02.07.2023**

* Документы выгружаются в подкаталог с ФИО военнослужащего. Подкаталоги по-прежнему располагаются в `c:\pisar_output\`.
* Каждый офицер из файла настройки "Войсковая часть", а также взводный и ротный из файла настройки "Военнослужащий" имеют личный признак `is_guard` (гвардеец = True, не гвардеец = False). Войсковая часть также имеет этот признак. 


**1.8 | 30.06.2023**

* Добавлена группа "Служебное разбирательство по факту cамовольного оставления части" и 9 документов в ней.
* Добавлены новые ключи в файлы конфигурации для поддержки группы документов "Служебное разбирательство по факту cамовольного оставления части".

**1.7 | 27.06.2023**

* Добавлена новая группа "Служебное разбирательство по факту cамовольного оставления части" и её первый документ "Административное расследование по факту самовольного оставления части".
* В настройки Войсковой части добавлены ключи: батальон и номер телефона (см. выше в списке параметров).

**1.6 | 26.06.2023**

* В группу "Служебное разбирательство по факту грубого дисциплинарного проступка" добавлен документ "Протокол о ГДП".
* Отныне вместо одного файла настройки используются два: soldier_info.json (данные о военнослужащем) и common_info.json (данные о войсковой части).
* Правильное склонение имён военнослужащих женского пола.

**1.5 | 23.06.2023**

* Оптимизирован поиск военнослужащего.
* Добавлен файл personnel_data_massive.xlsx с 2000 военнослужащих. Данные созданы случайным образом.

**1.4 | 20.06.2023**

* Исправлена ошибка с названием листа. Было "ШБС", стало -- "ШДС".
* Расшифровка аббревиатуры ВРИО в документе "Служебное разбирательство" в резолютивной части и правильное склонение.
* Исправлена ошибка с поиском несуществующего военнослужащего.

**1.3 | 15.06.2023**

* Отныне в файле Штатного расписания обязан присутствовать лист `ШДС`. На этом листе следует расположить таблицу с данными военнослужащих. Остальные листы книги Excel игнорируются. Файл personnel_demo.xlsx имеет правильную структуру.
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

	