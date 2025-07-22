class student:
    _id_counter=1
    def __init__(self,name):
        self.name=name
        self.student_id=student._id_counter
        student._id_counter+=1
        self.grade={}#courses grades
        self.enrolled_courses=[]
    def __str__(self):
        return f"student id: {self.student_id}, name{self.name}"




s1=student('fares')
print(s1.__str__())
print(s1._id_counter)