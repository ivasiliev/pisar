USE [pisar]
GO

BEGIN TRY
    BEGIN TRAN;

    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(1, null, 'Степень родства');

    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(3, 1, 'Отец');
    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(4, 1, 'Мать');
    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(5, 1, 'Братья сестры');
    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(6, 1, 'Дети');
    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(7, 1, 'Знакомые, друзья, товарищи');

    ------------------------------------------------

    INSERT INTO [dbo].[GENERIC_DICT]([ID],[PARENT_ID],[NAME])VALUES(2, null, 'Воинское звание');

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
    BEGIN
        ROLLBACK TRAN;
    END

    SELECT
        ERROR_NUMBER()    AS ErrorNumber,
        ERROR_SEVERITY()  AS Severity,
        ERROR_STATE()     AS State,
        ERROR_PROCEDURE() AS ProcedureName,
        ERROR_LINE()      AS LineNumber,
        ERROR_MESSAGE()   AS ErrorMessage;

    -- re-throw to caller preserving error info
    THROW;
END CATCH;