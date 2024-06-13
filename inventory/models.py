from django.db import models


class Inventory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=2, null=False)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    quantity_sold = models.IntegerField(null=False, blank=False)
    sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_date = models.DateField(auto_now_add=True)
    last_sale_date = models.DateField(auto_now=True)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi')
    ), default='pending')

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.IntegerField()
    comments = models.TextField()
