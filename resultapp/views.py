from django.shortcuts import render, redirect,get_object_or_404
from django.db import IntegrityError
from .models import *
from django.http import HttpResponse,HttpResponseBadRequest, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Create your views here.


def index(request):

    n = Student.objects.all()
    m = Result.objects.all()

    o = Class.objects.filter(name='Jss1a')
    # t = Teacher.objects.filter()
    return render(request, 'index.html')

def test(request):

    n = Student.objects.all()
    m = Result.objects.all()

    o = Class.objects.filter(name='Jss1a')
    # t = Teacher.objects.filter()
    return render(request, 'index.html', {'student': n, 'results': m, 'class': o})

def login_p(request):
    if 'logged_in_user' in request.session:
        return redirect('login')
    elif 'logged_in_teacher' in request.session:
        return redirect('teacher_db')
    else:
        if request.method == 'POST':
            try:
                admission_num = request.POST['admission_num']
                password = request.POST['password']
            except Exception:
                return render(request, 'login.html', {'error': "Admission Number is not a character"})
            if not admission_num or not password:
                return render(request, 'login.html', {'error': "Admission Number and Password IS REQUIRED"})
            else:
                pass
            try:
                user = Student.objects.get(admission_number=admission_num)
            except Student.DoesNotExist:
                return render(request, 'login.html', {'error': "Invalid Admission Number or Password"})
                # Checking if the password matches the password for the username
            if user.password == password:
                request.session['logged_in_user'] = admission_num
                # this will help when the redirecting url has a parameter 'next'
                new_redirect = request.GET.get('next', 'home') 
                return redirect(new_redirect)
            else:
                return render(request ,'login.html', {'error': 'Invalid username or password'})

        return render(request, 'login.html') 




def dbd(request):
    if 'logged_in_user' in request.session:
        admission_num = request.session['logged_in_user']
        try:
            user = Student.objects.get(admission_number=admission_num)
            result = Result.objects.filter(student=user)
            return render(request, 'dashboard.html', {'result': result, 'user': user})
        except Student.DoesNotExist:
            pass
    else:
        return redirect('login')  # Redirect to the login page if not logged in

def user_logout(request):
    logout(request)
    return redirect('index')

def teacher_logout(request):
    logout(request)
    return redirect('index')


def login_t(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'login1.html', {'error': "Username and Password IS REQUIRED"})
        else:
             pass
        try:
            user = Teacher.objects.get(username=username)
        except Student.DoesNotExist:
            return render(request, 'login.html', {'error': "Invalid Username Number or Password"})
            # Checking if the password matches the password for the username
        if user.password == password:
            request.session['logged_in_teacher'] = username
            # this will help when the redirecting url has a parameter 'next'
            new_redirect = request.GET.get('next', 'teacher_db') 
            return redirect(new_redirect)
        else:
            return render(request ,'login1.html', {'error': 'Invalid username or password'})

    return render(request, 'login1.html') 

def t_dbd(request):
    if 'logged_in_teacher' in request.session:
        username = request.session['logged_in_teacher']
        try:
            teacher = Teacher.objects.get(username=username)
            assigned_class = teacher.assigned_class
            students = Student.objects.filter(enrolled_class=assigned_class)
            return render(request, 't_dashb.html', {'teacher': teacher, 'students': students})
        except Teacher.DoesNotExist:
             return render(request, 't_dashb.html', {'user': username})
    else:

        return redirect('login')  # Redirect to the login page if not logged in





def add_student(request):
    if 'logged_in_teacher' in request.session:
        username = request.session['logged_in_teacher']
        user = Teacher.objects.get(username=username)
        assigned_class = user.assigned_class
        students = Student.objects.filter(enrolled_class=assigned_class)
        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            password = request.POST['password']
            admission_number = request.POST['admission_number']
            address = request.POST['address']
            enrolled_class = request.POST['enrolled_class']
            year = request.POST['year']
            month = request.POST['month']
            day = request.POST['day']

            # creating and saving the model instance
            DOB = year + '-' + month + '-' + day
           
            new_student = Student(name=name, username=username, password=password, admission_number=admission_number, address=address, DOB=DOB, enrolled_class=user.assigned_class)

            new_student.save()

            return redirect('teacher_db')
        
        return render(request, 'add_stu.html' , {'user': user, 'students': students})
    

def update_student(request,student_id):
    if 'logged_in_teacher' in request.session:
        username = request.session['logged_in_teacher']
        try:
            user = Teacher.objects.get(username=username)
            assigned_class = user.assigned_class
            student = Student.objects.get(enrolled_class=assigned_class,id=student_id)
            results = Result.objects.filter(student=student)
            if request.method == 'POST':
                subject = request.POST['subject1']
                test = request.POST['test']
                exams = request.POST['exams']
               
                if not subject or not test or not exams:
                    return render(request, 'update_stu.html', {'results': results, 'user': user, 'students': student,'error': "All fields are required"})
                else:
                    testint = int(test)
                    examint = int(exams)
                    total_score = testint + examint
                    new_result = Result(student=student, subject=subject, test_scores=test, exam_scores=exams, total_scores=total_score)
                    new_result.save()
                    return redirect('update_student', student_id)
                
            return render(request, 'update_stu.html', { 'results': results, 'user': user, 'students': student})
        
        except Teacher.DoesNotExist:
            return render(request, 'update_stu.html', {'error': 'An error occurred'})
        
        
    return redirect('login') 

def delete_result(request,student_id, result_id):
    if 'logged_in_teacher' in request.session:
        username = request.session['logged_in_teacher']
        
        try:
            user = Teacher.objects.get(username=username)
            assigned_class = user.assigned_class
            student = Student.objects.get(enrolled_class=assigned_class,id=student_id)
            results = Result.objects.filter(student=student, id=result_id)
            results.delete()
            # Ensure the task belongs to the logged-in user
            # if not results:
            #     return render(request, 'update_stu.html', {'error': 'An error occurred'})
           
        except (Student.DoesNotExist, Result.DoesNotExist):
            # Handle case where the user or task does not exist
            pass

        return redirect('update_student', student_id)
    else:
        return redirect('login')


def delete_student(request,student_id):
    if 'logged_in_teacher' in request.session:
        username = request.session['logged_in_teacher']
        
        try:
            user = Teacher.objects.get(username=username)
            assigned_class = user.assigned_class
            student = Student.objects.get(enrolled_class=assigned_class,id=student_id)
            
            student.delete()
            
           
        except (Student.DoesNotExist):
        
            pass

        return redirect('teacher_db')
    else:
        return redirect('login')



def result(request):
    
    return render(request, 'result.html')