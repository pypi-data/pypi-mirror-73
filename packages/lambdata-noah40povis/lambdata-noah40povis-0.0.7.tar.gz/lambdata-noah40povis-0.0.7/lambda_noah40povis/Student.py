

#!/usr/bin/env python    
class Student: 

    def __init__(self, first, last, age, major):
        self.first = first
        self.last = last
        self.age = age
        self.email = first + '.' + last + '@company.com'
        self.major = major 
    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    







