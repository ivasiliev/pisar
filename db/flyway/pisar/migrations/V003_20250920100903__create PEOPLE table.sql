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