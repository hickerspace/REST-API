from logger import log

class LedTicker(object):
	"""
	LedTicker

	This code converts your text (420 chars max per message) into a valid
	protocol message the LED ticker understands and displays.
	"""
	ASCII2ISO8859_15 = {
			0x0A: 0x20,  0x0D: 0x20,  0xC3: 0x7F,  0xC2: 0x80,
			0xC1: 0x81,  0xC0: 0x82,  0xC4: 0x83,  0xC5: 0x84,
			0xC6: 0x85,  0xDF: 0x86,  0xC7: 0x87,  0xD0: 0x88,
			0xC9: 0x89,  0xCA: 0x8A,  0xC8: 0x8B,  0xCB: 0x8C,
			0xCD: 0x8D,  0xCC: 0x8E,  0xCE: 0x8F,  0xCF: 0x90,
			0xD1: 0x91,  0xD3: 0x92,  0xD4: 0x93,  0xD2: 0x94,
			0xD6: 0x95,  0xD5: 0x96,  0xD8: 0x97,  0xDE: 0x98,
			0xDA: 0x99,  0xD9: 0x9A,  0xDB: 0x9B,  0xDC: 0x9C,
			0xBE: 0x9D,  0xDD: 0x9E,  0xE3: 0x9F,  0xE2: 0xA0,
			0xE1: 0xA1,  0xE0: 0xA2,  0xE4: 0xA3,  0xE5: 0xA4,
			0xE6: 0xA5,  0xE7: 0xA6,  0xE9: 0xA7,  0xEA: 0xA8,
			0xE8: 0xA9,  0xEB: 0xAA,  0xED: 0xAB,  0xEC: 0xAC,
			0xEE: 0xAD,  0xEF: 0xAE,  0xF1: 0xAF,  0xF3: 0xB0,
			0xF4: 0xB1,  0xF2: 0xB2,  0xF6: 0xB3,  0xF5: 0xB4,
			0xF8: 0xB5,  0xFE: 0xB6,  0xFA: 0xB7,  0xF9: 0xB8,
			0xFB: 0xB9,  0xFC: 0xBA,  0xFF: 0xBB,  0xFD: 0xBC,
			0xA5: 0xBD,  0xA3: 0xBE,  0xA4: 0xBF }

	def __init__(self, ledfile=None, sign_id=20):
		"""
		Constructor.

		@param string text file holding messages
		@param integer sign id
		"""
		self.ledfile = ledfile
		self.items = []

		# sign id between 1 and 255 (hex: 01 to FF)
		self.sign_id = sign_id

	def get_output(self):
		"""
		Public function to get the current output

		@return string Output formatted for the ledticker
		"""
		input_ = self.get_next_text()

		return self.create_output(input_)

	def add_item(self, text):
		"""
		Public function to add a new item to the messagestack

		Needs some sanityfu
		@param string $text the message
		"""
		self.items.append(text)
		self.write_items()

	def items_available(self):
		"""
		Returns number of available message items

		@return integer number of available messages
		"""
		self.update_items()
		return len(self.items)

	def get_next_text(self):
		"""
		Gets the next item

		This function deletes the current item and gets the next one

		@param array all items
		@return string the text to be displayed
		"""
		self.update_items()
		result = self.items.pop()
		self.write_items()
		return result

	def write_items(self):
		if self.ledfile:
			filestream = open(self.ledfile, "w")
			for item in self.items:
				filestream.write(item.encode("utf-8") + "\n")
			filestream.close()

	def create_output(self, input_=""):
		"""
		Creates a string for the led ticker

		Converts a given string suitable for the hickerspace led ticker

		@param string $input the input string (optional)
		@return string the string to be sent to the ticker display
		"""
		input_ = input_.decode("UTF-8", "ignore").encode("ISO-8859-15", "replace")
		text = "<L1><PB><FE><MC><WC><FE>"
		for char in input_:
			text += self.utf8_to_iso8859_15(char)

		return "<ID%x>%s%s<E>" % (self.sign_id, text,
				self.calculate_checksum(text))

	def update_items(self):
		if self.ledfile:
			self.items = [l.rstrip() for l in open(self.ledfile, "r")]

	def calculate_checksum(self, text):
		"""
		Calculates checksum

		Calculates the checksum of given text.

		@param string $text the input text
		@return string the calculated checksum
		"""
		checksum = 0
		for i in range(len(text)):
			checksum ^= ord(text[i])

		return "%x" % (checksum % 256)

	def utf8_to_iso8859_15(self, utf8char):
		"""
		Converts a UTF-8 char to iso8859_15, if possible.

		Needs some kind of blacklist for unconvertable chars.

		@return string converted character, if available. Otherwise given character.
		"""
		try:
			return chr(self.ASCII2ISO8859_15[ord(utf8char)])
		except KeyError:
			return utf8char

	def set_sign_id(self):
		"""
		Gives the ledticker an id.

		@return string the string to be sent to the ticker display
		"""
		return "<ID><%x><E>" % self.sign_id

