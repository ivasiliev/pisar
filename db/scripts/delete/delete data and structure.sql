use pisar

-- ВНИМАНИЕ! ЭТОТ СКРИПТ УДАЛЯЕТ ВСЕ ДАННЫЕ И СТРУКТУРУ (ТАБЛИЦЫ, VIEW И ТД.)
-- ЗАПУСКАЙТЕ ЕГО ТОЛЬКО ЕСЛИ СДЕЛАЛИ РЕЗЕРВНУЮ КОПИЮ!

BEGIN TRY
    DROP VIEW [dbo].[LS_FULL_INFO];
    DROP VIEW [dbo].[SR_ACTIVE];
    -----
    DROP TABLE [dbo].[RELATIVE_PERSON];
    DROP TABLE [dbo].[ADDRESS];
    DROP TABLE [dbo].[DOCUMENT];    
    DROP TABLE [dbo].[LS];
    DROP TABLE [dbo].[SR];
    DROP TABLE [dbo].[POSITION_DICT];
    DROP TABLE [dbo].[PEOPLE];
    DROP TABLE [dbo].[GENERIC_DICT];
END TRY
BEGIN CATCH
    SELECT
        ERROR_NUMBER()    AS ErrorNumber,
        ERROR_SEVERITY()  AS Severity,
        ERROR_STATE()     AS ErrorState,
        ERROR_PROCEDURE() AS ProcedureName,
        ERROR_LINE()      AS ErrorLine,
        ERROR_MESSAGE()   AS ErrorMessage;
END CATCH;
