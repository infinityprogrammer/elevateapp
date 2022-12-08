from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, nowdate, flt, cint, get_datetime_str, nowdate
from frappe import _
import json
import datetime


def test_fn(self, arg):
    
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
    
    je.append("accounts",{
            "account" : "1110 - Cash - INF",
            "party_type" : '',
            "party" : '',
            "debit_in_account_currency" : 120,
            "credit_in_account_currency" : 0,
            "cost_center" : 'Main - INF',
            "user_remark" : 'SALARY GRATUITY'
        })
    
    je.append("accounts",{
            "account" : "EMIRATES NBD 000 - INF",
            "party_type" : '',
            "party" : '',
            "debit_in_account_currency" : 0,
            "credit_in_account_currency" : 120,
            "cost_center" : 'Main - INF',
            "user_remark" : 'SALARY GRATUITY'
        })
    
    je.save(ignore_permissions=True)
    je.submit()