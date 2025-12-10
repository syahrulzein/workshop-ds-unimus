import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def chart():
    df = pd.read_excel('healthcare-dataset-stroke-data.xlsx')
    pasien_count = df.shape[0]
    pasien_stroke = df['stroke'].sum()
    stroke_rate = (pasien_stroke / pasien_count) * 100

    #Card Metrics dan Button Filter
    col1, col2, col3, col4, col5, col6 = st.columns([2,2,3,2,2,1])
    with col1:
        st.metric(label="Total Pasien", value = pasien_count)
    with col2:
        st.metric(label="Pasien Stroke", value = pasien_stroke)
    with col3:
        st.metric(label="Persentase", value = f"{stroke_rate:.2f}%")
    
    # Initialize session state untuk filter
    if 'selected_gender' not in st.session_state:
        st.session_state.selected_gender = None
    if 'selected_stroke' not in st.session_state:
        st.session_state.selected_stroke = None
    
    with col4:
        st.write('**Jenis Kelamin**')
        if st.button("Laki-laki"):
            st.session_state.selected_gender = 'Male'
        if st.button("Perempuan"):
            st.session_state.selected_gender = 'Female'
    with col5:
        st.write('**Status**')
        if st.button("Stroke"):
            st.session_state.selected_stroke = 1
        if st.button("No Stroke"):
            st.session_state.selected_stroke = 0
    
    # Reset button
    with col6:
        if st.button("🔄"):
            st.session_state.selected_gender = None
            st.session_state.selected_stroke = None
            st.rerun()
    
    # Apply filter
    filtered_df = df.copy()
    if st.session_state.selected_gender:
        filtered_df = filtered_df[filtered_df['gender'] == st.session_state.selected_gender]
    if st.session_state.selected_stroke is not None:
        filtered_df = filtered_df[filtered_df['stroke'] == st.session_state.selected_stroke]
    
    # Update metrics dengan filtered data
    filtered_count = filtered_df.shape[0]
    filtered_stroke = filtered_df['stroke'].sum()
    filtered_rate = (filtered_stroke / filtered_count * 100) if filtered_count > 0 else 0

    st.dataframe(df.head(5))
    
    #Pie Chart
    col1, col2 = st.columns([5,5])
    with col1:
    #Persentase Jenis Kelamin
        category_df = filtered_df['gender'].value_counts(dropna=False).reset_index()
        category_df.columns = ['gender', 'count']
        fig = px.pie(category_df, names='gender', values='count', title='Jenis Kelamin')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
    #Persentase Hipertensi
        hyper_stroke_count = filtered_df['hypertension'].value_counts().reset_index()
        hyper_stroke_count.columns = ['hypertension', 'count']
        hyper_stroke_count['hypertension_label'] = hyper_stroke_count['hypertension'].map({0: 'Tidak', 1: 'Hipertensi'})
        fig = px.pie(hyper_stroke_count, names='hypertension_label', values='count', title='Hipertensi pada Pasien')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns([5,5])
    with col1:
    #Persentase Riwayat Merokok
        smoke_stroke_count = filtered_df['smoking_status'].value_counts(dropna=False).reset_index()
        smoke_stroke_count.columns = ['smoking_status', 'count']
        fig = px.pie(smoke_stroke_count, names='smoking_status', values='count', title='Riwayat Merokok pada Pasien')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
    #Persentase Tempat Tinggal
        residence_stroke_count = filtered_df['Residence_type'].value_counts().reset_index()
        residence_stroke_count.columns = ['Residence_type', 'count']
        fig = px.pie(residence_stroke_count, names='Residence_type', values='count', title='Tipe Tempat Tinggal Pasien')
        st.plotly_chart(fig, use_container_width=True)    

    #Histogram BMI
    fig = px.histogram(filtered_df, x='bmi', nbins=30, title='Distribusi BMI Pasien')
    st.plotly_chart(fig, use_container_width=True)

    #Scatter Plot
    #Glukosa vs BMI
    fig = px.scatter(filtered_df, x='avg_glucose_level', y='bmi', 
                        color='stroke',
                        title='Hubungan BMI dan Rata-rata Tingkat Glukosa')
    st.plotly_chart(fig, use_container_width=True)
    
    #Usia vs BMI
    fig = px.scatter(filtered_df, x='age', y='bmi', 
                        color='stroke',
                        title='Hubungan BMI dan Usia')
    st.plotly_chart(fig, use_container_width=True)

    #Distribusi Stroke dengan Box Plot
    fig = px.box(filtered_df, x='stroke', y='age', 
                 title='Distribusi Usia Pasien dengan Stroke')
    st.plotly_chart(fig, use_container_width=True)

    #Distribusi Usia berdasarkan Kasus Stroke dengan Line Chart
    age_stroke_counts = filtered_df.groupby(['age', 'stroke']).size().reset_index(name='counts')
    fig = px.line(age_stroke_counts, x='age', y='counts', color='stroke',
                  title='Distribusi Usia berdasarkan Kasus Stroke')
    st.plotly_chart(fig, use_container_width=True)     

    #Perkembangan Penderita Stroke dan Perbandingan Berdasarkan Kategori
    col1, col2 = st.columns([5,5])
    with col1:
    #Berdasarkan BMI Category
        st.write('**Perkembangan Penderita Stroke**')
        bmi_stroke_counts = filtered_df.groupby(['bmi_category', 'stroke']).size().reset_index(name='counts')
        bmi_stroke_counts['stroke_label'] = bmi_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        fig = px.line(bmi_stroke_counts, x='bmi_category', y='counts', color='stroke_label',
                      title='Berdasarkan BMI Category')
        fig.update_layout(legend=dict(x=0.5, y=1.1, xanchor='right', yanchor='top', orientation='h'))
        st.plotly_chart(fig, use_container_width=True)
    
    #Berdasarkan kolom 'age_category'
        age_cat_stroke_counts = filtered_df.groupby(['age_category', 'stroke']).size().reset_index(name='counts')
        age_cat_stroke_counts['stroke_label'] = age_cat_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        fig = px.line(age_cat_stroke_counts, x='age_category', y='counts', color='stroke_label',
                      title='Berdasarkan Age Category')
        fig.update_layout(legend=dict(x=0.5, y=1.1, xanchor='right', yanchor='top', orientation='h'))
        st.plotly_chart(fig, use_container_width=True)
    
    #Berdasarkan Resiko Stroke
        risk_stroke_counts = filtered_df.groupby(['risk_score', 'stroke']).size().reset_index(name='counts')
        risk_stroke_counts['stroke_label'] = risk_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        fig = px.line(risk_stroke_counts, x='risk_score', y='counts', color='stroke_label',
                      title='Berdasarkan Risk Category')
        fig.update_layout(legend=dict(x=0.5, y=1.1, xanchor='right', yanchor='top', orientation='h'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write('**Perbandingan Berdasarkan Kategori**')
    #Berdasarkan Tipe Pekerjaan
        work_stroke_counts = filtered_df.groupby(['work_type', 'stroke']).size().reset_index(name='counts')
        work_stroke_counts['stroke_label'] = work_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        fig = px.bar(work_stroke_counts, x='work_type', y='counts', color='stroke_label',
                     title='Berdasarkan Tipe Pekerjaan', barmode='group')
        fig.update_layout(legend=dict(x=0.5, y=1.1, xanchor='right', yanchor='top', orientation='h'))
        st.plotly_chart(fig, use_container_width=True)
    
    #Berdasarkan Kategori Glukosa
        glucose_stroke_counts = filtered_df.groupby(['glucose_category', 'stroke']).size().reset_index(name='counts')
        glucose_stroke_counts['stroke_label'] = glucose_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        fig = px.bar(glucose_stroke_counts, x='glucose_category', y='counts', color='stroke_label',
                     title='Berdasarkan Kategori Glukosa', barmode='group')
        fig.update_layout(legend=dict(x=0.5, y=1.1, xanchor='right', yanchor='top', orientation='h'))
        st.plotly_chart(fig, use_container_width=True)
    
    #Berdasarkan Life Style Risk
        lifestyle_stroke_counts = filtered_df.groupby(['lifestyle_risk', 'stroke']).size().reset_index(name='counts')
        lifestyle_stroke_counts['stroke_label'] = lifestyle_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        fig = px.bar(lifestyle_stroke_counts, x='lifestyle_risk', y='counts', color='stroke_label',
                     title='Berdasarkan Life Style Risk', barmode='group')
        fig.update_layout(legend=dict(x=0.5, y=1.1, xanchor='right', yanchor='top', orientation='h'))
        st.plotly_chart(fig, use_container_width=True)