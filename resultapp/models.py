from django.db import models

# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, unique=True)
    username = models.CharField(max_length=100, unique=True, null=True, )
    password = models.CharField(max_length=20, null=True )

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, null=True, )
    password = models.CharField(max_length=20, null=True)
    admission_number = models.IntegerField(null=True, unique=True)
    address = models.CharField(max_length=100)
    DOB = models.DateField()
    enrolled_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name



class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=100)
    test_scores = models.IntegerField()
    exam_scores = models.IntegerField()
    total_scores = models.IntegerField(editable=True)

    @property
    def grade(self):
        if self.total_scores >= 90:
            return 'A'
        elif self.total_scores >= 80:
            return 'B'
        elif self.total_scores >= 70:
            return 'C'
        elif self.total_scores >= 60:
            return 'D'
        else:
            return 'F'
        
    # def save(self, *args, **kwargs):
    #     self.total_scores = self.test_scores + self.exam_scores  # calculate total_scores
    #     super().save(*args, **kwargs)  # call the original save method

    def __str__(self):
        return f'{self.student.name} - {self.subject}'