class Eaow:
    def __init__(self):
        self.name = 'EaowEaow'
        self.lastname = 'DookieDic'
        self.nickname = 'Dook'
    def WhoAmI(self):
        '''
        this a functiom will show the name
        '''
        print('My name is: {}' .format(self.name))
        print('My nickname is: {}' .format(self.nickname))
        
    @property
    def email(self):
        return 'Email:{}.{}@gmail.com'.format(self.name.lower(),self.lastname.lower())

    def __str__(self):
        return 'This is a Eaow class'

if __name__ == '__main__':
    
myEaow = Eaow()
myEaow.WhoAmI()
print(myEaow)
print(myEaow.email)
print('______________')

mypee = Eaow()
mypee.name = 'PP'
mypee.lastname = 'Pookie'
mypee.nickname = 'PEE'
mypee.WhoAmI()
print(mypee.name)



    
    
   
