class PersFullNameSettings:
	def __init__(self, declension_type, battalion_only, militaryman_required, position_required, dob_required,
	             military_unit_required, is_dob_short, person_name_required=True, rank_required=True, address_required=True):
		self.declension_type = declension_type  # 1
		self.battalion_only = battalion_only  # 2
		self.militaryman_required = militaryman_required  # 3
		self.position_required = position_required  # 4
		self.dob_required = dob_required  # 5
		self.military_unit_required = military_unit_required  # 6
		self.is_dob_short = is_dob_short  # 7
		self.person_name_required = person_name_required  # 8
		self.rank_required = rank_required  # 9
		self.address_required = address_required  # 10
