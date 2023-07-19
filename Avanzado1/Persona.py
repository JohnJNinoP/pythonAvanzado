

class Person:
    def __init__(self,name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print('hello my name is {} and I am {} years ols'.format(self.name,self.age))


if __name__ == '__main__':
    person = Person('John' , 34)
    person.say_hello()
    print(person.age)
    print(person.name)
