from django.views import generic
from .models import Payment, PaymentCategory, Income, IncomeCategory
from .forms import PaymentSearchForm, IncomeSearchForm, PaymentCreateForm, IncomeCreateForm, TransitionGraphSearchForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from .plugin_plotly import GraphGenerator


class PaymentList(generic.ListView):
    """支出一覧"""
    template_name = 'kakeibo/payment_list.html'
    model = Payment
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PaymentSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            # 何も選択されていないときは0の文字列が入るため、除外
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

            greater_than = form.cleaned_data.get('greater_than')
            if greater_than:
                queryset = queryset.filter(price__gte=greater_than)

            less_than = form.cleaned_data.get('less_than')
            if less_than:
                queryset = queryset.filter(price__lte=less_than)

            key_word = form.cleaned_data.get('key_word')
            if key_word:
                # 空欄で区切り、順番に絞る、and検索
                if key_word:
                    for word in key_word.split():
                        queryset = queryset.filter(description__icontains=word)

            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        return context


class IncomeList(generic.ListView):
    """収入一覧"""
    template_name = 'kakeibo/income_list.html'
    model = Income
    ordering = '-date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = IncomeSearchForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get('year')
            if year and year != '0':
                queryset = queryset.filter(date__year=year)

            month = form.cleaned_data.get('month')
            if month and month != '0':
                queryset = queryset.filter(date__month=month)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        return context


class PaymentCreate(generic.CreateView):
    """支出登録"""
    template_name = 'kakeibo/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                      f'支出を登録しました\n'
                      f'日付:{payment.date}\n'
                      f'カテゴリ:{payment.category}\n'
                      f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeCreate(generic.CreateView):
    """収入登録"""
    template_name = 'kakeibo/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入登録'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      f'収入を登録しました\n'
                      f'日付:{income.date}\n'
                      f'カテゴリ:{income.category}\n'
                      f'金額:{income.price}円')
        return redirect(self.get_success_url())


class PaymentUpdate(generic.UpdateView):
    """支出更新"""
    template_name = 'kakeibo/register.html'
    model = Payment
    form_class = PaymentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def form_valid(self, form):
        self.object = payment = form.save()
        messages.info(self.request,
                      f'支出を更新しました\n'
                      f'日付:{payment.date}\n'
                      f'カテゴリ:{payment.category}\n'
                      f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeUpdate(generic.UpdateView):
    """収入更新"""
    template_name = 'kakeibo/register.html'
    model = Income
    form_class = IncomeCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入更新'
        return context

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def form_valid(self, form):
        self.object = income = form.save()
        messages.info(self.request,
                      f'収入を更新しました\n'
                      f'日付:{income.date}\n'
                      f'カテゴリ:{income.category}\n'
                      f'金額:{income.price}円')
        return redirect(self.get_success_url())


class PaymentDelete(generic.DeleteView):
    """支出削除"""
    template_name = 'kakeibo/delete.html'
    model = Payment

    def get_success_url(self):
        return reverse_lazy('kakeibo:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '支出削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = payment = self.get_object()

        payment.delete()
        messages.info(self.request,
                      f'支出を削除しました\n'
                      f'日付:{payment.date}\n'
                      f'カテゴリ:{payment.category}\n'
                      f'金額:{payment.price}円')
        return redirect(self.get_success_url())


class IncomeDelete(generic.DeleteView):
    """収入削除"""
    template_name = 'kakeibo/delete.html'
    model = Income

    def get_success_url(self):
        return reverse_lazy('kakeibo:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = '収入削除確認'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = income = self.get_object()
        income.delete()
        messages.info(self.request,
                      f'収入を削除しました\n'
                      f'日付:{income.date}\n'
                      f'カテゴリ:{income.category}\n'
                      f'金額:{income.price}円')
        return redirect(self.get_success_url())


class MonthDashboard(generic.TemplateView):
    """月間支出ダッシュボード"""
    template_name = 'kakeibo/month_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        context['year_month'] = f'{year}年{month}月'

        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        if month == 12:
            next_year = year + 1
            next_month = 1
        else:
            next_year = year
            next_month = month + 1
        context['prev_year'] = prev_year
        context['prev_month'] = prev_month
        context['next_year'] = next_year
        context['next_month'] = next_month

        queryset = Payment.objects.filter(date__year=year)
        queryset = queryset.filter(date__month=month)
        # 後の工程でエラーになるため、クエリセットが何もない時はcontextを返す
        if not queryset:
            return context

        df = read_frame(queryset,
                        fieldnames=['date', 'price', 'category'])

        gen = GraphGenerator()

        df_pie = pd.pivot_table(df, index='category', values='price', aggfunc=np.sum)
        pie_labels = list(df_pie.index.values)
        pie_values = [val[0] for val in df_pie.values]
        plot_pie = gen.month_pie(labels=pie_labels, values=pie_values)
        context['plot_pie'] = plot_pie

        context['table_set'] = df_pie.to_dict()['price']

        context['total_payment'] = df['price'].sum()

        df_bar = pd.pivot_table(df, index='date', values='price', aggfunc=np.sum)
        dates = list(df_bar.index.values)
        heights = [val[0] for val in df_bar.values]
        plot_bar = gen.month_daily_bar(x_list=dates, y_list=heights)
        context['plot_bar'] = plot_bar

        return context


class TransitionView(generic.TemplateView):
    """月毎の収支推移"""
    template_name = 'kakeibo/transition.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_queryset = Payment.objects.all()
        income_queryset = Income.objects.all()
        self.form = form = TransitionGraphSearchForm(self.request.GET or None)
        context['search_form'] = self.form

        graph_visible = None
        months_payment = None
        payments = None
        months_income = None
        incomes = None

        if form.is_valid():
            payment_category = form.cleaned_data.get('payment_category')
            if payment_category:
                payment_queryset = payment_queryset.filter(category=payment_category)
            income_category = form.cleaned_data.get('income_category')
            if income_category:
                income_queryset = income_queryset.filter(category=income_category)

            graph_visible = form.cleaned_data.get('graph_visible')

        # forms.pyで表示グラフ名を定義
        if not graph_visible or graph_visible == 'Payment':
            payment_df = read_frame(payment_queryset,
                                    fieldnames=['date', 'price'])
            payment_df['date'] = pd.to_datetime(payment_df['date'])
            payment_df['month'] = payment_df['date'].dt.strftime('%Y-%m')
            payment_df = pd.pivot_table(payment_df, index='month', values='price', aggfunc=np.sum)
            months_payment = list(payment_df.index.values)
            payments = [y[0] for y in payment_df.values]

        if not graph_visible or graph_visible == 'Income':
            income_df = read_frame(income_queryset,
                                   fieldnames=['date', 'price'])
            income_df['date'] = pd.to_datetime(income_df['date'])
            income_df['month'] = income_df['date'].dt.strftime('%Y-%m')
            income_df = pd.pivot_table(income_df, index='month', values='price', aggfunc=np.sum)
            months_income = list(income_df.index.values)
            incomes = [y[0] for y in income_df.values]

        gen = GraphGenerator()
        context['transition_plot'] = gen.transition_plot(x_list_payment=months_payment,
                                                         y_list_payment=payments,
                                                         x_list_income=months_income,
                                                         y_list_income=incomes)

        return context
