from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate
from frappe import _
import json
import datetime
from dateutil.relativedelta import relativedelta


def gratuity_journal(self, arg):
    
    join_date = frappe.db.get_value('Employee', self.employee, ['date_of_joining', 'status'], as_dict=1)
    
    last_payslip_start_month = get_payslip_start_month(self.start_date);
    last_payslip_end_mont = get_payslip_end_month(self.end_date);
    emp_join_month = get_emp_join_month(join_date.date_of_joining);
    
    check_eligible = range(last_payslip_start_month, last_payslip_end_mont+1)
    
    if emp_join_month in check_eligible:
        base_val = get_basic_pay_amount(self.name);
        emp_age = get_emp_age(join_date.date_of_joining, self.end_date)
        
        accural_gratuity = 0.00
        
        if emp_age < 5:
            accural_gratuity = (base_val/30)*21
        if emp_age >= 5:
            accural_gratuity = base_val
            
        # start_day_month = '{} {}'.format(last_payslip_start_month, last_payslip_start_date)
        # end_day_month = '{} {}'.format(last_payslip_end_mont, last_payslip_start_date)
    
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = 'Journal Entry'
        je.company = self.company
        je.posting_date = self.posting_date
        je.cheque_no = self.name
        je.cheque_date = self.posting_date
        je.due_date = self.posting_date
        je.user_remark = "SALARY GRATUITY"
        je.difference = 0
        # je.multi_currency = self.multi_currency
        je.remark = "SALARY GRATUITY"
        je.bill_no = self.name
        je.bill_date = self.posting_date
        # je.journal_entry_batch = self.name
        
        
        # Expense account
        je.append("accounts",{
                "account" : "Petty Cash - Others - INF",
                "party_type" : '',
                "party" : '',
                "debit_in_account_currency" : accural_gratuity,
                "credit_in_account_currency" : 0,
                "cost_center" : 'Main - INF',
                "user_remark" : 'SALARY GRATUITY'
            })
        
        # Liability account
        je.append("accounts",{
                "account" : "EMIRATES NBD - INF",
                "party_type" : 'Employee',
                "party" : self.employee,
                "debit_in_account_currency" : 0,
                "credit_in_account_currency" : accural_gratuity,
                "cost_center" : 'Main - INF',
                "user_remark" : 'SALARY GRATUITY'
            })
        
        je.save(ignore_permissions=True)
        je.submit()
        
        frappe.msgprint('Gratuity entry passed');


def get_payslip_start_month(start_date):
    s_month = frappe.db.sql(""" SELECT EXTRACT(MONTH FROM %(start_date)s) sm""",{'start_date':start_date},as_dict=1)
    return s_month[0].sm

def get_payslip_end_month(end_date):
    e_month = frappe.db.sql(""" SELECT EXTRACT(MONTH FROM %(end_date)s) sm""",{'end_date':end_date},as_dict=1)
    return e_month[0].sm

def get_emp_join_month(join_dt):
    j_month = frappe.db.sql(""" SELECT EXTRACT(MONTH FROM %(join_dt)s) sm""",{'join_dt':join_dt},as_dict=1)
    return j_month[0].sm

def get_date_join_month(start_date, end_date):
    j_month = frappe.db.sql(""" SELECT EXTRACT(MONTH FROM %(join_dt)s) sm""",{'join_dt':join_dt},as_dict=1)
    return j_month[0].sm

def get_basic_pay_amount(pay_slip):
    basic_amount = frappe.db.sql(""" SELECT amount FROM `tabSalary Detail` where parenttype = 'Salary Slip' and parent = %(pay_slip)s """,{'pay_slip':pay_slip},as_dict=1)
    return basic_amount[0].amount

def get_emp_age(doj, enddt):
    year_val = frappe.db.sql(""" select (DATEDIFF(%(enddt)s ,%(doj)s)/365) as amount""",{'enddt':enddt,'doj':doj},as_dict=1)
    return year_val[0].amount