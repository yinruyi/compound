class A():
    def foo3(self):
        print "A"
class B(A):
    def foo2(self):
        pass

class C():
    def foo1(self):
        print "C"
        self.foo3()

class D(B, C):
    pass

d = D()
d.foo1()