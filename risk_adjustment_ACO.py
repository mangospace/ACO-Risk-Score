# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 13:01:28 2022

@author: manas
"""

import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(page_title="MSSP ACO: Risk Adjustment", page_icon=":tada:")

header_container = st.container()
#side_container= st.sidebar()
defs_container = st.container()
main_container = st.container()
ref_container = st.container()

st.sidebar.header("ACO Risk Adjustments Basics ")

st.sidebar.subheader("**Groups**")
st.sidebar.write("""Two "groups" of ACO members are assigned annually:
- **Newly assigned beneficiaries**: A beneficiary assigned in the  performance year who neither was assigned to nor received a primary care service from any of the ACO’s participants during the assignment window for the most recent prior benchmark or performance year.
- **Continuously assigned beneficiaries**: A beneficiary in the current performance year who either was assigned to or received a primary care service from any of the ACO’s participants during the assignment window for the most recent prior benchmark or performance year.""")



st.sidebar.subheader("**Medicare enrollment type**")
st.sidebar.write("""Four "Medicare enrollment type" in which ACO members are divided on monthly basis (order based on number of members for typical ACO)
- **Aged Non-duals**
- **Aged Duals**
- **Disabled**
- **ESRD**""")


with header_container:
	# for example a logo or a image that looks like a website header
	# different levels of text you can include in your app
	st.title("CMS-HCC prospective risk adjustment")
	st.subheader("I welcome comments, feedback and opportunity to learn more or collaborate. Tweet @manas8u")
	st.markdown("This is working draft of my understanding of ACO Risk score. This is my best understanding of how risk scores for CMS MSSP ACO are calculated. This is subject to revision.This page was created on 9/2022. Please check with me (or others) to check for the relevance of this document.")

with main_container:
    st.write("Most ACOs have a small number of newly assigned beneficiaries. For brevity, the bulk of this discussion will focus on on continuously assigned beneficiaries.:")
    st.write("CMS uses MA risk adjustment weights published by CMS for curent year after removing the coding intensity adjustment that it applies for MA program.")
    st.write("CMS uses MA risk adjustment weights published by CMS for curent year after removing the coding intensity adjustment that it applies for MA program.")
    st.write("For each beneficiary, CMS uses risk score for **each month** in the enrollment category (e.g. ESRD, ND, Duals, Dis) to calculate beneficiaries average risk score for year.")
    st.write("Therefore, over an year, the risk scores used for beneficiaries in a Shared Savings Program enrollment status  (e.g., aged/non-dual eligible) may be derived from more than one risk adjustment model (e.g., community model versus institutional model versus new enrollee model.")
    st.write("At end of year, CMS calculates parameters to normalize aggregate risk scores such that that the mean national assignable FFS risk score for that enrollment type for that year equals 1.0. This is mean-centering around mean=1 and I think of this as standardization.")
    latext = r'''
    $$
    RiskScore_{enrollment-type} = \frac{x_{ACO} - \mu + 1}{\sigma}  
    $$ 
    '''
    st.write(latext)
    st.write("CMS applies parameters to each beneficiary’s **average** risk score") 
    st.write("CMS will also renormalize demographic risk scores (age, gender) by Medicare enrollment type for each year to ensure that the mean national assignable FFS risk score equals 1.0.")
    st.write("For each Medicare enrollment type and each performance year:")
    st.write("CMS will adjust the ACO’s benchmark to account for changes in health status and demographic factors for all beneficiaries.") 
    st.write("CMS will restate the ACO’s updated historical benchmark in the appropriate performance year risk to recognize changes in the level of risk among the ACO’s assigned beneficiaries. To me this means that if CMS uses clinical risk score or demographic risk score in person year based on assessment, it would use the same methodology for baseline year.")
    st.write("For the ACO’s continuously assigned beneficiaries, CMS will calculate:")
    st.write("1. CMS-HCC prospective risk scores, and")
    st.write("2. Demographic scores.")
    st.write("CMS will then determine whether a **prospective HCC or demographic risk adjustment will be used** for the **continuously assigned** population at the aggregate level (rather than within each Medicare enrollment type).")
    st.write("CMS will compare risk ratios for each continuously assigned beneficiary population in each Medicare enrollment type based on their CMS-HCC scores and demographic risk scores for the performance year relative to Baseline Year 3.")
    st.write("CMS will weight the risk ratios for each Medicare enrollment type relative to their respective person years and per capita benchmark dollars to obtain an overall dollar weighted average risk ratio.")

#https://www.milliman.com/en/insight/pathways-to-success-mssp-final-rule-financial-benchmark
    st.write("If the overall HCC risk ratio is less than one— thereby indicating the average HCC score for the continuously assigned beneficiaries has fallen relative to BY3— CMS applies HCC ratios to the continuously assigned population within each Medicare enrollment type.")
    st.write("Alternatively, if the overall risk ratio is greater than or equal to one, then the demographic ratios are applied to the continuously assigned population within each Medicare enrollment type.")

    st.write("")
    st.subheader("Worked example")

    st.write("Lets say that for a hypothetical ACO A452 with 100 members has the 'raw' risk scores for performance year as follows:")
    data = [['Aged Non-duals (AGND)', 1.05 , 80 ,'9,000' ,'7,200', 0.7182], 
            ['Aged Duals (AGDU)', 1.1, 15 ,'10,500', '1,575', 0.1687], 
            ['Disabled(Dis)', 0.9 , 3 ,'5,000' ,'150', 0.0128], 
            ['End Stage Renal Disease(ESRD)', 1.11, 2 ,'80,000' , '1,600', 0.16],              
            ['Total',np.nan ,100,np.nan ,'10,525',1.0644]
            ]

#    data = [['Aged Non-duals (AGND)', 1.05 , 80 ,9000 ,7200, 0.7182 ], ['Aged Duals (AGDU)', 1.1, 15 ,10500, 1575, 0.1646], ['Disabled(Dis)', 0.9 , 3 ,5000 ,150, 0.01282], ['End Stage Renal Disease(ESRD)', 1.11, 2 ,80000 , 1600, 0.1687], 'Total',np.nan ,100,np.nan ,10525,1.0644]
    df = pd.DataFrame(data, columns=['Medicare enrollment type', 'CMS HCC Risk Score PY','Person years contributed to ACO(%)','BY per capita expenses ($)', 'Person year weighted ACO per capital total expenses','Dollar weighted average risk ratio'])
    st.table(df)
 
    st.write("")
    st.write("Since Dollar weighted average risk ratio > 1.03 (CMS allows 3% higher compared to Baseline Year 3), therefore, CMS will apply the demographic ratios to the continuously assigned population within each Medicare enrollment type.")
    st.write("**Caveat: I am most probably not correct in understanding this because I can imagine that for this ACO demographic ratio might be <1 therefore, penalizing the ACO.**")
   
    st.write("CMS will then update the ACO’s historical benchmark risk scores for the continuously and newly assigned populations within each Medicare enrollment type based on the ratio of HCC or a combination of HCC and demographic scores in the performance period relative to BY3.")


with ref_container:
	# for example a logo or a image that looks like a website header
	# different levels of text you can include in your app
    st.subheader("References")
    st.write("Ref: Medicare Shared Savings Program: Shared Savings and Losses and Assigment methodology Specifications (2018) https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/sharedsavingsprogram/Downloads/Shared-Savings-Losses-Assignment-Spec-V6.pdf")
    st.write("Larson, A (2020) The increasing relevance of risk scores on MSSP ACOs https://www.medinsight.milliman.com/en/healthcare-analytics/the-increasing-relevance-of-risk-scores-on-mssp-acos")
    st.write('Gusland C, Herbold JS, Kramer MJ, Mills C "Pathways to Success” MSSP final rule: Financial benchmark (2019) https://www.milliman.com/en/insight/pathways-to-success-mssp-final-rule-financial-benchmark')

