CREATE TABLE [dbo].[POSITION_DICT](
	[ID] [int] NOT NULL,
	[POSITION_FULL] [varchar](500) NOT NULL,
	[POSITION_SHORT] [varchar](200) NOT NULL,
	[POSITION] [varchar](200) NOT NULL,
	[UNIT1] [varchar](200) NOT NULL,
	[UNIT2] [varchar](200) NOT NULL,
	[PLATOON] [varchar](200) NOT NULL,
	[SQUAD] [varchar](200) NOT NULL,
	[MILITARY_POSITION] [varchar](300) NOT NULL,
 CONSTRAINT [PK_POSITION_DICT] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
) ON [PRIMARY]
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Полная должность' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'POSITION_FULL'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Сокр. Должн.' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'POSITION_SHORT'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Должность' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'POSITION'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Подразделение' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'UNIT1'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Подразделение 2' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'UNIT2'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Взвод' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'PLATOON'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Отделение' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'SQUAD'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Воинская должность' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'POSITION_DICT', @level2type=N'COLUMN',@level2name=N'MILITARY_POSITION'
GO