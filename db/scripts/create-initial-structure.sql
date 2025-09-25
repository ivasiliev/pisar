CREATE TABLE [dbo].[PEOPLE](
	[ID] [int] NOT NULL,
	[SURNAME] [varchar](100) NOT NULL,
	[NAME] [varchar](50) NOT NULL,
	[FATHER_NAME] [varchar](100) NULL,
	[DOB] [date] NULL,
	[GENDER] [int] NULL,
 CONSTRAINT [PK_PEOPLE] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'0 male, 1 female' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'PEOPLE', @level2type=N'COLUMN',@level2name=N'GENDER'
GO

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

CREATE TABLE [dbo].[SR](
	[ID] [int] NOT NULL,
	[PEOPLE_ID] [int] NOT NULL,
	[POSITION_ID] [int] NOT NULL,
 CONSTRAINT [PK_SR] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[SR]  WITH CHECK ADD  CONSTRAINT [FK_SR_PEOPLE] FOREIGN KEY([PEOPLE_ID])
REFERENCES [dbo].[PEOPLE] ([ID])
GO

ALTER TABLE [dbo].[SR] CHECK CONSTRAINT [FK_SR_PEOPLE]
GO

CREATE TABLE [dbo].[LS](
	[PEOPLE_ID] [int] NOT NULL,
	[PERSONAL_NUMBER] [varchar](50) NOT NULL,
 CONSTRAINT [PK_LS] PRIMARY KEY CLUSTERED 
(
	[PEOPLE_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[LS]  WITH CHECK ADD  CONSTRAINT [FK_LS_PEOPLE] FOREIGN KEY([PEOPLE_ID])
REFERENCES [dbo].[PEOPLE] ([ID])
GO

ALTER TABLE [dbo].[LS] CHECK CONSTRAINT [FK_LS_PEOPLE]
GO

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Личный номер (государственный уникальный код военнослужащего)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'LS', @level2type=N'COLUMN',@level2name=N'PERSONAL_NUMBER'
GO

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

GO