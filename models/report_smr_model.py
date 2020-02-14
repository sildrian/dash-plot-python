# pydata stack
import pandas as pd
from setting.conn_db_smtel import conn

import dash_core_components as dcc
import plotly.graph_objs as go
from random import randint

import random
import string

###########################
# Data Manipulation / Model
###########################

def fetch_data(q):
    result = pd.read_sql(
        sql=q,
        con=conn()
    )
    return result


def get_operator():
    '''Returns the list of operators that are stored in the database'''

    operator_query = (
        f'''
        SELECT DISTINCT vgrp_operator as operator
        FROM daily_sales_perdenom
        '''
    )
    operators = fetch_data(operator_query)
    operators = list(operators['operator'].sort_values(ascending=True))
    return operators

def get_product_by_productcode(startdate='', enddate='', productcode=''):
    '''Returns match results for the selected prompts'''

    results_query = (
        f'''
        select a.kode_produk, sum(a.laba_kotor) as laba_kotor, a.tanggal
        FROM report_to_smr a
        where a.kode_produk='{productcode}' and date(a.tanggal)>=DATE('{startdate}') and date(a.tanggal)<=DATE('{enddate}')
        group by a.kode_produk, a.tanggal
        order by a.kode_produk, a.tanggal ASC
        '''
    )
    product_results = fetch_data(results_query)
    return product_results

def get_date_by_range(startdate='', enddate=''):
    '''Returns match results for the selected prompts'''

    results_query = (
        f'''
        select distinct a.tanggal
        FROM report_to_smr a
        where substr(a.kode_produk,1,1)='S' and substr(a.kode_produk,1,2)!='SM' and date(a.tanggal)>=DATE('{startdate}') and date(a.tanggal)<=DATE('{enddate}')
        order by a.tanggal ASC
        '''
    )
    product_results = fetch_data(results_query)
    return product_results

def get_productcode_by_tsel(startdate='', enddate=''):
    '''Returns match results for the selected prompts'''

    results_query = (
        f'''
        select distinct a.kode_produk
        FROM report_to_smr a
        where substr(a.kode_produk,1,1)='S' and substr(a.kode_produk,1,2)!='SM' and date(a.tanggal)>=DATE('{startdate}') and date(a.tanggal)<=DATE('{enddate}')
        group by a.kode_produk, a.tanggal
        order by a.kode_produk, a.tanggal ASC
        '''
    )
    product_results = fetch_data(results_query)
    return product_results

def get_product_by_operator(startdate='', enddate='',operator=''):
    '''Returns match results for the selected prompts'''

    results_query = (
        f'''
        SELECT a.ptype as kode_produk, sum(a.laba_kotor) as laba_kotor, a.tanggal as tanggal 
        FROM( select a.*, c.kode_produk, c.laba_kotor, c.profit_margin from
                (select * from report.daily_sales_perdenom where 
                        vgrp_operator='{operator}' 
                        and date(tanggal)>=DATE('{startdate}') 
                        and date(tanggal)<=DATE('{enddate}')
                )as a
                left join (select kode_produk, laba_kotor, profit_margin, tanggal
                                from report.report_to_smr where 
                                date(tanggal)>=DATE('{startdate}') 
                                and date(tanggal)<=DATE('{enddate}') 
                        ) as c on a.ptype=c.kode_produk and date(a.tanggal) = date(c.tanggal) 
                )as a
        group by a.ptype, date(a.tanggal)
        order by a.ptype, date(a.tanggal) ASC
        '''
    )
    product_results = fetch_data(results_query)
    return product_results

def get_productcode_by_operator(startdate='', enddate='',operator=''):
    '''Returns match results for the selected prompts'''

    results_query = (
        f'''
        SELECT distinct a.ptype as kode_produk
        FROM( select a.*, c.kode_produk, c.laba_kotor, c.profit_margin from
                (select * from report.daily_sales_perdenom where 
                        vgrp_operator='{operator}' 
                        and date(tanggal)>=DATE('{startdate}') 
                        and date(tanggal)<=DATE('{enddate}')
                )as a
                left join (select kode_produk, laba_kotor, profit_margin, tanggal
                                from report.report_to_smr where 
                                date(tanggal)>=DATE('{startdate}') 
                                and date(tanggal)<=DATE('{enddate}') 
                        ) as c on a.ptype=c.kode_produk and date(a.tanggal) = date(c.tanggal) 
                )as a
        group by a.ptype, date(a.tanggal)
        order by a.ptype, date(a.tanggal) ASC
        '''
    )
    product_results = fetch_data(results_query)
    return product_results


def draw_product_points_graph(temp_results='',daterange_arr='',operator='',daterangearray=''):
    showresult = []
    all_results = []

    for i in range(len(temp_results)):
        for j in range(len(daterange_arr)):
            codeproduct = temp_results[i][0][0]
            try:
                if temp_results[i][j][1]:
                    showresult.append(temp_results[i][j][1])
            except:
                showresult.append(0)

        all_results.append(
            go.Scatter(x=daterangearray, y=showresult, mode='lines+markers', name=codeproduct,
                line=dict(color='rgb(%d,%d,%d)' % (randint(0,255), randint(0,255), randint(0,255)), width=2)
            ),
        ) 
        showresult = []
        codeproduct = ''

    figure = go.Figure(
        data=all_results,
        # layout=go.Layout(
        #     title='Report Benefit',
        #     showlegend=False
        # )
        layout=go.Layout(
            title='Graph of Benefit '+operator,
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30)
        )
    )

    return figure