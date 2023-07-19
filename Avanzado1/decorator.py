
_password = '123456'

def password_requerid(fun):
    def wrapper():
        password = input('what is your password')

        if _password == password:
            return fun()
        else:
            print('The password is wrong')
        
    return wrapper

@password_requerid
def needs_password():
    print('The pasword is ok')

def upper(func):
    def wrapper(*args , **kwargs):
        result = func(*args,**kwargs)
        return result.upper()

    return wrapper
    
@upper
def say_my_name(name):    
    return 'Hello, {}'.format(name)

if __name__ ==  '__main__':
    needs_password()
    print(say_my_name("john"))
