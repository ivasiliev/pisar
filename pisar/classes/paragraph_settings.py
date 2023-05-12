class ParagraphSettings:
	def __init__(self):
		self.is_bold = False
		self.align_left = False
		self.align_center = False
		self.align_right = False
		self.align_justify = False

	def has_markup(self):
		return self.is_bold or self.align_left or self.align_center or self.align_right or self.align_justify
