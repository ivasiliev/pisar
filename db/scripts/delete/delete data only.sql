use pisar

-- ВНИМАНИЕ! ЭТОТ СКРИПТ УДАЛЯЕТ ВСЕ ДАННЫЕ ИЗ БД, НЕ ТРОГАЯ СТРУКТУРУ
-- ЗАПУСКАЙТЕ ЕГО ТОЛЬКО ЕСЛИ СДЕЛАЛИ РЕЗЕРВНУЮ КОПИЮ!

BEGIN TRY
   delete from dbo.LS;
   delete from dbo.SR;
   delete from dbo.POSITION_DICT;
   delete from dbo.PEOPLE;
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
