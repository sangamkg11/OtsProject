from django.db import models

# Create your models here.
class Candidate(models.Model):
    username=models.CharField(primary_key=True,max_length=20)
    password=models.CharField(null=False,max_length=30)
    name=models.CharField(null=False,max_length=30)
    test_attempt=models.IntegerField(default=0)
    points=models.FloatField(default=0.0)

class Question(models.Model):
    qid=models.BigAutoField(primary_key=True,auto_created=True)
    que=models.TextField()  #bcs charfiled support only 255 character 
    a=models.CharField(max_length=255)
    b=models.CharField(max_length=255)
    c=models.CharField(max_length=255)
    d=models.CharField(max_length=255)
    ans=models.CharField(max_length=255)

class Result(models.Model):
    resultid=models.BigAutoField(primary_key=True,auto_created=True)
    username=models.ForeignKey(Candidate,on_delete=models.CASCADE) 
        #method to made the foreign key and if delete perform then it should be done from every where like question and result as well

    date=models.DateField(auto_now=True)
    time=models.TimeField(auto_now=True)
    attempt=models.IntegerField()
    right=models.IntegerField()
    wrong=models.IntegerField()
    points=models.FloatField()

