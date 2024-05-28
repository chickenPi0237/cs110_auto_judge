class file_stat:
	def __init__(self):
		alpha_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','u','v','w','x','y','z']
		self.alpha_dict = dict.fromkeys(alpha_list, 0)
	def freqFile(self, file):
		for lines in file:
			for leter in lines:
				if leter.lower() in self.alpha_dict.keys():
					self.alpha_dict[leter.lower()] += 1
	def show_dict(self):
		print(self.alpha_dict)


if __name__ == '__main__':
	f = open('1234.c')
	fs = file_stat()
	fs.freqFile(f)
	fs.show_dict()
	f.close()

				