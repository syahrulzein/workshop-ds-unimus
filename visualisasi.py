import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            category_df['count'],
            labels=category_df['gender'],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Jenis Kelamin")
        st.pyplot(fig)
    
    with col2:
    #Persentase Hipertensi
        hyper_stroke_count = filtered_df['hypertension'].value_counts().reset_index()
        hyper_stroke_count.columns = ['hypertension', 'count']
        hyper_stroke_count['hypertension_label'] = hyper_stroke_count['hypertension'].map({0: 'Tidak', 1: 'Hipertensi'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            hyper_stroke_count['count'],
            labels=hyper_stroke_count['hypertension_label'],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Hipertensi pada Pasien")
        st.pyplot(fig)
    
    col1, col2 = st.columns([5,5])
    with col1:
    #Persentase Riwayat Merokok
        smoke_stroke_count = filtered_df['smoking_status'].value_counts(dropna=False).reset_index()
        smoke_stroke_count.columns = ['smoking_status', 'count']
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            smoke_stroke_count['count'],
            labels=smoke_stroke_count['smoking_status'],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Riwayat Merokok pada Pasien")
        st.pyplot(fig)
    
    with col2:
    #Persentase Tempat Tinggal
        residence_stroke_count = filtered_df['Residence_type'].value_counts().reset_index()
        residence_stroke_count.columns = ['Residence_type', 'count']
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            residence_stroke_count['count'],
            labels=residence_stroke_count['Residence_type'],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Tipe Tempat Tinggal Pasien")
        st.pyplot(fig)    

    #Histogram BMI
    sns.set_style("whitegrid")
    sns.set_palette("pastel")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(
        data=filtered_df,
        x='bmi',
        bins=30,
        kde=False,
        ax=ax
    )
    ax.set_title("Distribusi BMI Pasien")
    ax.set_xlabel("BMI")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

    #Scatter Plot
    #Glukosa vs BMI
    sns.set_style("whitegrid")
    sns.set_palette("pastel")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x='avg_glucose_level',
        y='bmi',
        hue='stroke',        # pengganti color=
        palette='viridis',   # opsional (warna lebih jelas)
        ax=ax
    )
    ax.set_title("Hubungan BMI dan Rata-rata Tingkat Glukosa")
    ax.set_xlabel("Rata-rata Glukosa")
    ax.set_ylabel("BMI")
    st.pyplot(fig)
    
    #Usia vs BMI
    sns.set_style("whitegrid")
    sns.set_palette("pastel")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_df,
        x='age',
        y='bmi',
        hue='stroke',        # sama seperti color='stroke'
        palette='viridis',   # opsional untuk warna lebih jelas
        ax=ax
    )
    ax.set_title("Hubungan BMI dan Usia")
    ax.set_xlabel("Usia")
    ax.set_ylabel("BMI")
    st.pyplot(fig)


    #Distribusi Stroke dengan Box Plot
    sns.set_style("whitegrid")
    sns.set_palette("pastel")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(
        data=filtered_df,
        x='stroke',
        y='age',
        ax=ax
    )
    ax.set_title("Distribusi Usia Pasien dengan Stroke")
    ax.set_xlabel("Stroke")
    ax.set_ylabel("Usia")
    st.pyplot(fig)

    #Distribusi Usia berdasarkan Kasus Stroke dengan Line Chart
    age_stroke_counts = filtered_df.groupby(['age', 'stroke']).size().reset_index(name='counts')
    sns.set_style("whitegrid")
    sns.set_palette("pastel")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(
        data=age_stroke_counts,
        x='age',
        y='counts',
        hue='stroke',
        marker='o',
        ax=ax
    )
    ax.set_title("Distribusi Usia berdasarkan Kasus Stroke")
    ax.set_xlabel("Usia")
    ax.set_ylabel("Jumlah Pasien")
    st.pyplot(fig)     

    #Perkembangan Penderita Stroke dan Perbandingan Berdasarkan Kategori
    col1, col2 = st.columns([5,5])
    with col1:
    #Berdasarkan BMI Category
        st.write('**Perkembangan Penderita Stroke**')
        bmi_stroke_counts = filtered_df.groupby(['bmi_category', 'stroke']).size().reset_index(name='counts')
        bmi_stroke_counts['stroke_label'] = bmi_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.lineplot(
            data=bmi_stroke_counts,
            x='bmi_category',
            y='counts',
            hue='stroke_label',
            marker='o',
            ax=ax
        )
        ax.set_title("Berdasarkan BMI Category")
        ax.set_xlabel("BMI Category")
        ax.set_ylabel("Jumlah Pasien")
        # Legend horizontal di atas grafik
        ax.legend(
            title="", 
            loc="lower center",
            bbox_to_anchor=(0.5, 1.02),
            ncol=2,
            frameon=False
        )
        st.pyplot(fig)

    
    #Berdasarkan kolom 'age_category'
        age_cat_stroke_counts = filtered_df.groupby(['age_category', 'stroke']).size().reset_index(name='counts')
        age_cat_stroke_counts['stroke_label'] = age_cat_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.lineplot(
            data=age_cat_stroke_counts,
            x='age_category',
            y='counts',
            hue='stroke_label',
            marker='o',
            ax=ax
        )
        ax.set_title("Berdasarkan Age Category")
        ax.set_xlabel("Age Category")
        ax.set_ylabel("Jumlah Pasien")
        ax.legend(
            title="",
            loc='lower center',
            bbox_to_anchor=(0.5, 1.02),
            ncol=2,
            frameon=False
        )
        st.pyplot(fig)
    
    #Berdasarkan Resiko Stroke
        risk_stroke_counts = filtered_df.groupby(['risk_score', 'stroke']).size().reset_index(name='counts')
        risk_stroke_counts['stroke_label'] = risk_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.lineplot(
            data=risk_stroke_counts,
            x='risk_score',
            y='counts',
            hue='stroke_label',
            marker='o',
            ax=ax
        )
        ax.set_title("Berdasarkan Risk Category")
        ax.set_xlabel("Risk Score")
        ax.set_ylabel("Jumlah Pasien")
        ax.legend(
            title="",
            loc='lower center',
            bbox_to_anchor=(0.5, 1.02),
            ncol=2,
            frameon=False
        )
        st.pyplot(fig)
    
    with col2:
        st.write('**Perbandingan Berdasarkan Kategori**')
    #Berdasarkan Tipe Pekerjaan
        work_stroke_counts = filtered_df.groupby(['work_type', 'stroke']).size().reset_index(name='counts')
        work_stroke_counts['stroke_label'] = work_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(
            data=work_stroke_counts,
            x='work_type',
            y='counts',
            hue='stroke_label',
            ax=ax
        )
        ax.set_title("Berdasarkan Tipe Pekerjaan")
        ax.set_xlabel("Tipe Pekerjaan")
        ax.set_ylabel("Jumlah Pasien")
        ax.legend(
            title="",
            loc='lower center',
            bbox_to_anchor=(0.5, 1.02),
            ncol=2,
            frameon=False
        )
        st.pyplot(fig)
    
    #Berdasarkan Kategori Glukosa
        glucose_stroke_counts = filtered_df.groupby(['glucose_category', 'stroke']).size().reset_index(name='counts')
        glucose_stroke_counts['stroke_label'] = glucose_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(
            data=glucose_stroke_counts,
            x='glucose_category',
            y='counts',
            hue='stroke_label',
            ax=ax
        )
        ax.set_title("Berdasarkan Kategori Glukosa")
        ax.set_xlabel("Kategori Glukosa")
        ax.set_ylabel("Jumlah Pasien")
        ax.legend(
            title="",
            loc="lower center",
            bbox_to_anchor=(0.5, 1.02),
            ncol=2,
            frameon=False
        )
        st.pyplot(fig)
    
    #Berdasarkan Life Style Risk
        lifestyle_stroke_counts = filtered_df.groupby(['lifestyle_risk', 'stroke']).size().reset_index(name='counts')
        lifestyle_stroke_counts['stroke_label'] = lifestyle_stroke_counts['stroke'].map({0: 'No Stroke', 1: 'Stroke'})
        sns.set_style("whitegrid")
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(
            data=lifestyle_stroke_counts,
            x='lifestyle_risk',
            y='counts',
            hue='stroke_label',
            ax=ax
        )
        ax.set_title("Berdasarkan Life Style Risk")
        ax.set_xlabel("Life Style Risk")
        ax.set_ylabel("Jumlah Pasien")
        ax.legend(
            title="",
            loc="lower center",
            bbox_to_anchor=(0.5, 1.02),
            ncol=2,
            frameon=False
        )
        st.pyplot(fig)