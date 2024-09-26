from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Depatment
from datetime import datetime
from django.db.models import Q

def view_all_employees(request):
    employees = Employee.objects.all()
    context = {
        'emps': employees  # Updated context variable name to match the template
    }
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')
        dept_id = request.POST.get('dept')
        role_id = request.POST.get('role')

        if not all([first_name, last_name, salary, bonus, phone, dept_id, role_id]):
            return HttpResponse('All fields are required.')

        try:
            salary = int(salary)
            bonus = int(bonus)
            dept_id = int(dept_id)
            role_id = int(role_id)
        except ValueError:
            return HttpResponse('Salary, Bonus, Department, and Role must be valid numbers.')

        try:
            department = Depatment.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
        except Depatment.DoesNotExist:
            return HttpResponse('Invalid department ID.')
        except Role.DoesNotExist:
            return HttpResponse('Invalid role ID.')

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            hire_date=datetime.now(),
            dept=department,
            role=role
        )
        employee.save()
        return HttpResponse('Employee Added Successfully')

    departments = Depatment.objects.all()
    roles = Role.objects.all()
    return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please enter a valid ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__id=dept)
        if role:
            emps = emps.filter(role__id=role)

        context = {
            'emps': emps
        }

        return render(request, 'view_all_emp.html', context)
    
    elif request.method == 'GET':
        departments = Depatment.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'filter_emp.html', context)

    else:
        return HttpResponse('An exception occurred')

def index(request):
    return render(request, 'index.html')
