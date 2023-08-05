

    
class Student: 

    def __init__(self, first, last, age, major):
        self.first = first
        self.last = last
        self.age = age
        self.email = first + '.' + last + '@company.com'
        self.major = major 
    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    






stu_1 = Student('Noah', 'Povis', 23, 'DS')
stu_2 = Student('Izzy', 'Mac', 24, 'WebDev')


print(stu_1.email)
print(stu_2.major)
print(stu_2.fullname())
print(stu_2.age)

