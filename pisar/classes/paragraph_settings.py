class ParagraphSettings:
	def __init__(self):
		self.is_bold = False
		self.align_left = False
		self.align_center = False
		self.align_right = False
		self.align_justify = False
		self.first_line_indent = -1
		self.left_indent = -1
		self.right_indent = -1

	def has_markup(self):
		return self.is_bold or self.align_left or self.align_center or self.align_right or self.align_justify or self.first_line_indent > 0 or self.left_indent > 0 or self.right_indent > 0
