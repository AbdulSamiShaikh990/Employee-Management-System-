from django.db import models

class Depatment(models.Model):
    name=models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
   
    
class Role(models.Model):
    name = models.CharField(max_length=100,null=False)
    
    def __str__(self) -> str:
        return self.name
    


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    salary = models.IntegerField()
    bonus = models.IntegerField()
    phone = models.CharField(max_length=15)
    hire_date = models.DateTimeField()
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='employees')
    dept = models.ForeignKey('Depatment', on_delete=models.CASCADE, related_name='employees')


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



    
    
    