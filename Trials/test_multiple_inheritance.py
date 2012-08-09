class A():
	def __init__(self):
		print 'initA'

class B(A):
	def __init__(self):
		print 'initB'

class C(A):
	def __init__(self):
		print 'initC'
		A.__init__(self)

class D(B,C):
	def __init__(self):
		print 'initD'
		B.__init__(self)
		C.__init__(self)

d = D()
