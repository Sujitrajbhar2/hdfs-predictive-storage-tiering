"""
views/about.py

About DataTierAI
"""

import streamlit as st
from utils.components import chart_card


def render():

    st.markdown(
        '<div class="page-title">About DataTierAI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Enterprise AI-Powered Storage Lifecycle Analytics Platform</div>',
        unsafe_allow_html=True,
    )

    with chart_card(key="chartcard_about"):

        st.markdown(
            '<div class="chart-card-title">Project Overview</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div style="color:#1E293B; font-size:16px; line-height:1.8;">

<h2 style="color:#1E3A8A;">🚀 What is DataTierAI?</h2>

<p>
<b>DataTierAI</b> is an AI-powered Enterprise Storage Lifecycle Analytics Platform that helps organizations analyze enterprise storage metadata, monitor storage utilization, predict storage tiers using Machine Learning, and optimize storage resources through intelligent recommendations.
</p>

<p>
The platform combines Data Engineering, Machine Learning, Apache Spark, HDFS, and interactive analytics to identify inactive files, improve storage efficiency, and reduce infrastructure costs.
</p>

<hr>

<h2 style="color:#1E3A8A;">🎯 Key Features</h2>

<ul>
<li>📊 Executive Dashboard with Enterprise KPIs</li>
<li>🤖 AI-powered Storage Tier Prediction</li>
<li>📈 Advanced Analytics & Interactive Charts</li>
<li>💾 Intelligent Storage Optimization</li>
<li>📂 Enterprise Data Explorer</li>
<li>📑 Department-wise Reports</li>
<li>🚨 Rule-based Alert Monitoring</li>
<li>📤 CSV Report Export</li>
</ul>

<hr>

<h2 style="color:#1E3A8A;">🤖 Machine Learning Module</h2>

<p>
The Machine Learning module predicts the storage tier of enterprise files using a trained classification model.
</p>

<b>Prediction Classes</b>

<ul>
<li>🔥 HOT Storage</li>
<li>🌤️ WARM Storage</li>
<li>❄️ COLD Storage</li>
</ul>

<b>Prediction Parameters</b>

<ul>
<li>File Size</li>
<li>File Age</li>
<li>Last Modified Days</li>
<li>Activity Score</li>
<li>Enterprise Score</li>
</ul>

<hr>

<h2 style="color:#1E3A8A;">⚙️ Technology Stack</h2>

<ul>
<li>🐍 Python</li>
<li>📊 Streamlit</li>
<li>📈 Plotly</li>
<li>🐼 Pandas</li>
<li>🤖 Scikit-learn</li>
<li>⚡ Apache Spark</li>
<li>🗄️ Hadoop HDFS</li>
<li>🔄 Apache Airflow</li>
<li>💾 Joblib</li>
</ul>

<hr>

<h2 style="color:#1E3A8A;">📁 Enterprise Dataset</h2>

<p>
The platform analyzes enterprise metadata collected from multiple enterprise systems.
</p>

<ul>
<li>File Name</li>
<li>Department</li>
<li>Category</li>
<li>Storage Tier</li>
<li>File Size</li>
<li>Activity Score</li>
<li>Enterprise Score</li>
<li>Business Score</li>
<li>File Age</li>
<li>Last Modified Date</li>
<li>Storage Label</li>
</ul>

<hr>

<h2 style="color:#1E3A8A;">📌 Enterprise Workflow</h2>

<ol>
<li>Collect Enterprise Metadata</li>
<li>ETL Processing</li>
<li>Data Preprocessing</li>
<li>Feature Engineering</li>
<li>Apache Spark Processing</li>
<li>Machine Learning Prediction</li>
<li>Interactive Dashboard Visualization</li>
<li>Storage Optimization Recommendations</li>
</ol>

<hr>

<h2 style="color:#1E3A8A;">💡 Project Objective</h2>

<p>
DataTierAI aims to help enterprises automate storage lifecycle management by reducing storage costs, identifying inactive files, predicting storage tiers, improving storage utilization, and providing actionable business insights through analytics and Artificial Intelligence.
</p>

<hr>

<h2 style="color:#1E3A8A;">👨‍💻 Developed Using</h2>

<p>
CDAC PG-Diploma Major Project<br>
Enterprise Data Engineering • Machine Learning • Big Data Analytics
</p>

</div>
            """,
            unsafe_allow_html=True,
        )