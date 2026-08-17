class MyClass:
    def my_method(self, a):
        print(a)

    @staticmethod
    def my_second_method(a):
        print(a)

    def my_third_method(a):
        print(a)

my_instance = MyClass()
my_instance.my_method(2)          # Prints 2
MyClass.my_second_method(3)       # Prints 3
my_instance.my_third_method(4)    # Error
