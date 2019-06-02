import plex

class ParseError(Exception):
	pass

class MyParser:
	def __init__(self):
		space = plex.Any(" \n\t")
		paren = plex.Str('(',')')
		letter = plex.Range('azAZ')
		Digit = plex.Range('09')
		Name = letter+plex.Rep(letter|Digit)
		bit = plex.Range('01')
		bits = plex.Rep1(bit)
		keyword = plex.Str('print','PRINT')
		space = plex.Any(" \n\t")
		Equal=plex.Str('=')
		XOR = plex.Str('xor')
		OR = plex.Str('or')
		AND = plex.Str('and')
		self.st = {}
		self.lexicon = plex.Lexicon([
			(Equal,plex.TEXT),
			(XOR,plex.TEXT),
			(OR,plex.TEXT),
			(AND,plex.TEXT),
			(bits, 'BIT_TOKEN'),
			(keyword,'PRINT'),
			(paren,plex.TEXT),
			(Name,'IDENTIFIER'),
			(space,plex.IGNORE)
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("Give a diffrent ")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()

	def stmt_list(self):
		if self.la == 'IDENTIFIER' or self.la == 'PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("Change the input file")
	def stmt(self):
		if self.la == 'IDENTIFIER':
			varName = self.text
			self.match('IDENTIFIER')
			self.match('=')
			e = self.expr()
			self.st[varName] = e
		elif self.la == 'PRINT':
			self.match('PRINT')
			e = self.expr()
			print('{:b}'.format(e))
		else:
			raise ParseError("Change the input file")
	def expr(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
			t = self.term()
			while self.la == 'xor':
				self.match('xor')
				t2 = self.term()
				t ^= t2
			if self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
					return t
			else:
					raise ParseError("Change the input file")
		else:
			raise ParseError("Change the input file")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la == 'BIT_TOKEN':
			t=self.factor()
			while self.la == 'or':
				self.match('or')
				t2 = self.factor()
				t |= t2
			if self.la == 'xor' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la==')':
				return t
			else:
				print(self.la)
				raise ParseError("Change the input file")
		else:
			raise ParseError("Change the input file")
	def factor(self):
		if self.la=='(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
			t=self.atom()
			while self.la == 'and':
				self.match('and')
				t2 = self.atom()
				t &= t2
			if self.la == 'xor' or self.la == 'or' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la==')':
				return t
			else:
				print(self.la)
				raise ParseError("Change the input file")
		else:
			raise ParseError("Change the input file")
	def atom(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varName = self.text
			self.match('IDENTIFIER')
			if varName in self.st:
				return self.st[varName]
			raise ParseRun("Change the input file")
		elif self.la=='BIT_TOKEN':
			value=int(self.text,2)
			self.match('BIT_TOKEN')
			return value
		else:
			raise ParseError("Change the input file")
parser = MyParser()
with open('input.txt','r') as fp:
	parser.parse(fp)
