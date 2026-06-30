from django.shortcuts import render, redirect
from django.views import View
from finance.forms import RegisterForm, TransactionForm,GoalForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'finance/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful registration

        return render(request, 'finance/register.html', {'form': form}) 

class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        
        # Calculate totals
        income_sum = user.transaction_set.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense_sum = user.transaction_set.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = income_sum - expense_sum

        # Calculate goals with waterfall logic
        goals = list(user.goal_set.all().order_by('deadline'))
        
        remaining_savings = net_savings
        
        for goal in goals:
            if remaining_savings > 0:
                allocated = min(remaining_savings, goal.target_amount)
                goal.progress_percentage = (allocated / goal.target_amount) * 100 if goal.target_amount > 0 else 0
                remaining_savings -= allocated
            else:
                goal.progress_percentage = 0

        context = {
            'total_income': income_sum,
            'total_expenses': expense_sum,
            'net_savings': net_savings,
            'goals': goals,
        }
        return render(request, 'finance/dashboard.html', context)
    
class TranactionCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = TransactionForm()
        return render(request, 'finance/transaction_form.html',{'form': form})
    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard')
        return render(request, 'finance/transaction_form.html', {'form': form}) 

class TransactionListView(LoginRequiredMixin, View):
    def get(self, request):
        transactions = request.user.transaction_set.filter(user=request.user)
        return render(request,'finance/transaction_list.html',{'transactions': transactions}
        )

class GoalCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = GoalForm()
        return render(request, 'finance/goal_form.html',{'form': form})
    def post(self, request):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal added successfully!')
            return redirect('dashboard')
        return render(request, 'finance/goal_form.html', {'form': form}) 