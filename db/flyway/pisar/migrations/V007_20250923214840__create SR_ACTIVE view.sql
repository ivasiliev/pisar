CREATE VIEW dbo.SR_ACTIVE AS
SELECT 
P.SURNAME as "Фамилия"
, P.NAME as "Имя"
, P.FATHER_NAME as "Отчество"
, LS.PERSONAL_NUMBER as "Личный номер"
, PD.POSITION_FULL as "Полная должность"
, PD.POSITION_SHORT as "Сокр. должность"
, PD.POSITION as "Должность"
, PD.UNIT1 as "Подразделение"
, PD.UNIT2 as "Подразделение 2"
, PD.PLATOON as "Взвод"
, PD.SQUAD as "Отделение"
FROM dbo.PEOPLE P 
inner join dbo.SR SR on SR.PEOPLE_ID = P.ID
inner join dbo.POSITION_DICT PD on SR.POSITION_ID = PD.ID
inner join dbo.LS LS on LS.PEOPLE_ID = P.ID