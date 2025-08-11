"""
Customer Analy# Page# Page configuration
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)uration
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)teractive Dashboard
A comprehensive Streamlit application for exploring customer analytics insights

Author: AI Assistant
Created: 2025-08-11
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .segment-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load customer analytics data"""
    try:
        # Load main dataset
        data_path = '/Users/saivedanthava/Desktop/DA/customer-analytics-portfolio/data/customer_analytics_data.csv'
        df = pd.read_csv(data_path)
        
        # Load statistics
        stats_path = '/Users/saivedanthava/Desktop/DA/customer-analytics-portfolio/data/dashboard_stats.json'
        with open(stats_path, 'r') as f:
            stats = json.load(f)
        
        return df, stats
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def create_metric_cards(stats):
    """Create KPI metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Customers",
            value=f"{stats['total_customers']:,}",
            help="Total number of customers analyzed"
        )
    
    with col2:
        st.metric(
            label="Total Revenue",
            value=f"${stats['total_revenue']:,.0f}",
            help="Total historical revenue from all customers"
        )
    
    with col3:
        st.metric(
            label="Average Revenue",
            value=f"${stats['avg_monetary']:,.0f}",
            help="Average revenue per customer"
        )
    
    with col4:
        # Find the segment with most customers
        top_segment = max(stats['segment_distribution'], key=stats['segment_distribution'].get)
        st.metric(
            label="Top Segment",
            value=top_segment,
            help="Most valuable customer segment"
        )

def create_rfm_analysis(df):
    """Create RFM analysis visualizations"""
    st.subheader("RFM Analysis")
    
    # RFM Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # RFM Segment Distribution
        segment_counts = df['Segment'].value_counts()
        fig_pie = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="RFM Customer Segments",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # RFM Scores Distribution
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=df['R_Score'], name='Recency', opacity=0.7, bingroup=1))
        fig_hist.add_trace(go.Histogram(x=df['F_Score'], name='Frequency', opacity=0.7, bingroup=1))
        fig_hist.add_trace(go.Histogram(x=df['M_Score'], name='Monetary', opacity=0.7, bingroup=1))
        fig_hist.update_layout(
            title="RFM Scores Distribution",
            xaxis_title="Score (1-5)",
            yaxis_title="Number of Customers",
            barmode='overlay'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # RFM Scatter Plot
    st.subheader("Customer Behavior Patterns")
    
    # Let user select which dimensions to plot
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X-Axis", ['Recency', 'Frequency', 'Monetary'], index=0)
    with col2:
        y_axis = st.selectbox("Y-Axis", ['Recency', 'Frequency', 'Monetary'], index=1)
    
    if x_axis != y_axis:
        fig_scatter = px.scatter(
            df, 
            x=x_axis, 
            y=y_axis,
            color='Segment',
            size='Monetary',
            hover_data=['CustomerID', 'CLV_Predictive'],
            title=f"{x_axis} vs {y_axis} by Customer Segment",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

def create_clv_analysis(df):
    """Create CLV analysis visualizations"""
    st.subheader("Customer Lifetime Value Analysis")
    
    # CLV Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_clv = df['CLV_Predictive'].mean()
        st.metric("Average CLV", f"${avg_clv:,.0f}")
    
    with col2:
        total_clv = df['CLV_Predictive'].sum()
        st.metric("Total Predicted CLV", f"${total_clv:,.0f}")
    
    with col3:
        top_clv = df['CLV_Predictive'].max()
        st.metric("Highest CLV", f"${top_clv:,.0f}")
    
    # CLV Distribution and Segments
    col1, col2 = st.columns(2)
    
    with col1:
        # CLV Distribution
        fig_hist_clv = px.histogram(
            df, 
            x='CLV_Predictive',
            nbins=50,
            title="CLV Distribution",
            labels={'CLV_Predictive': 'Predicted CLV ($)', 'count': 'Number of Customers'}
        )
        fig_hist_clv.add_vline(
            x=df['CLV_Predictive'].mean(), 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Mean: ${df['CLV_Predictive'].mean():,.0f}"
        )
        st.plotly_chart(fig_hist_clv, use_container_width=True)
    
    with col2:
        # CLV Segments
        clv_segment_counts = df['CLV_Segment'].value_counts()
        colors = {'Diamond': '#FFD700', 'Platinum': '#E5E4E2', 'Gold': '#FFD700', 
                  'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
        
        fig_clv_pie = px.pie(
            values=clv_segment_counts.values,
            names=clv_segment_counts.index,
            title="CLV Segment Distribution",
            color=clv_segment_counts.index,
            color_discrete_map=colors
        )
        st.plotly_chart(fig_clv_pie, use_container_width=True)
    
    # CLV vs Historical Value
    st.subheader("Predicted vs Historical Value")
    
    fig_scatter_clv = px.scatter(
        df,
        x='Monetary',
        y='CLV_Predictive',
        color='CLV_Segment',
        size='Frequency',
        hover_data=['CustomerID', 'Segment'],
        title="Historical Spend vs Predicted CLV",
        labels={'Monetary': 'Historical Spend ($)', 'CLV_Predictive': 'Predicted CLV ($)'},
        color_discrete_map=colors
    )
    
    # Add perfect prediction line
    max_val = max(df['Monetary'].max(), df['CLV_Predictive'].max())
    fig_scatter_clv.add_shape(
        type="line",
        x0=0, y0=0, x1=max_val, y1=max_val,
        line=dict(color="red", dash="dash"),
    )
    
    st.plotly_chart(fig_scatter_clv, use_container_width=True)

def create_kmeans_analysis(df):
    """Create K-Means clustering analysis"""
    st.subheader("K-Means Clustering Analysis")
    
    # Cluster Overview
    cluster_summary = df.groupby('KMeans_Cluster').agg({
        'CustomerID': 'count',
        'Monetary': 'mean',
        'CLV_Predictive': 'mean',
        'Frequency': 'mean',
        'Recency': 'mean'
    }).round(2)
    
    cluster_summary.columns = ['Count', 'Avg_Monetary', 'Avg_CLV', 'Avg_Frequency', 'Avg_Recency']
    cluster_summary['Percentage'] = (cluster_summary['Count'] / len(df) * 100).round(1)
    
    st.dataframe(cluster_summary, use_container_width=True)
    
    # Cluster Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Cluster Distribution
        cluster_counts = df['KMeans_Cluster'].value_counts().sort_index()
        fig_cluster_bar = px.bar(
            x=[f"Cluster {i}" for i in cluster_counts.index],
            y=cluster_counts.values,
            title="K-Means Cluster Distribution",
            labels={'x': 'Cluster', 'y': 'Number of Customers'}
        )
        st.plotly_chart(fig_cluster_bar, use_container_width=True)
    
    with col2:
        # Cluster Value Distribution
        fig_cluster_box = px.box(
            df,
            x='KMeans_Cluster',
            y='CLV_Predictive',
            title="CLV Distribution by Cluster",
            labels={'KMeans_Cluster': 'Cluster', 'CLV_Predictive': 'Predicted CLV ($)'}
        )
        st.plotly_chart(fig_cluster_box, use_container_width=True)

def create_customer_explorer(df):
    """Create customer search and exploration tool"""
    st.subheader("Customer Explorer")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        segment_filter = st.multiselect(
            "RFM Segments",
            options=df['Segment'].unique(),
            default=df['Segment'].unique()[:3]
        )
    
    with col2:
        clv_segment_filter = st.multiselect(
            "CLV Segments",
            options=df['CLV_Segment'].unique(),
            default=df['CLV_Segment'].unique()[:3]
        )
    
    with col3:
        cluster_filter = st.multiselect(
            "K-Means Clusters",
            options=sorted(df['KMeans_Cluster'].unique()),
            default=sorted(df['KMeans_Cluster'].unique())[:3]
        )
    
    # Apply filters
    filtered_df = df[
        (df['Segment'].isin(segment_filter)) &
        (df['CLV_Segment'].isin(clv_segment_filter)) &
        (df['KMeans_Cluster'].isin(cluster_filter))
    ]
    
    st.info(f"Showing {len(filtered_df):,} customers out of {len(df):,} total")
    
    # CLV range filter
    col1, col2 = st.columns(2)
    with col1:
        min_clv = st.number_input(
            "Minimum CLV ($)",
            min_value=0,
            max_value=int(df['CLV_Predictive'].max()),
            value=0
        )
    
    with col2:
        max_clv = st.number_input(
            "Maximum CLV ($)",
            min_value=min_clv,
            max_value=int(df['CLV_Predictive'].max()),
            value=int(df['CLV_Predictive'].max())
        )
    
    # Apply CLV filter
    filtered_df = filtered_df[
        (filtered_df['CLV_Predictive'] >= min_clv) &
        (filtered_df['CLV_Predictive'] <= max_clv)
    ]
    
    # Display filtered customers
    display_columns = [
        'CustomerID', 'Segment', 'CLV_Segment', 'KMeans_Cluster',
        'Monetary', 'CLV_Predictive', 'Frequency', 'Recency', 'AOV'
    ]
    
    existing_display_cols = [col for col in display_columns if col in filtered_df.columns]
    
    st.dataframe(
        filtered_df[existing_display_cols].sort_values('CLV_Predictive', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Download filtered data
    if st.button("Download Filtered Data"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"customer_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def create_business_recommendations(df):
    """Create business recommendations section"""
    st.subheader("Business Recommendations")
    
    # Segment-specific recommendations
    segments_info = {
        'Diamond': {
            'color': '#FFD700',
            'icon': 'Diamond',
            'recommendations': [
                "Provide VIP customer service and dedicated account managers",
                "Offer exclusive products and early access to new releases",
                "Implement personalized marketing campaigns",
                "Create loyalty rewards programs with premium benefits"
            ]
        },
        'Platinum': {
            'color': '#E5E4E2',
            'icon': 'Platinum',
            'recommendations': [
                "Develop retention programs to prevent churn",
                "Upsell premium products and services",
                "Provide priority customer support",
                "Offer referral bonuses for bringing new customers"
            ]
        },
        'Gold': {
            'color': '#DAA520',
            'icon': 'Gold',
            'recommendations': [
                "Focus on increasing purchase frequency",
                "Implement cross-selling strategies",
                "Send targeted promotional campaigns",
                "Provide excellent customer service to build loyalty"
            ]
        },
        'Silver': {
            'color': '#C0C0C0',
            'icon': 'Silver',
            'recommendations': [
                "Re-engagement campaigns to increase activity",
                "Value-driven offers and discounts",
                "Educational content about product benefits",
                "Regular communication to stay top-of-mind"
            ]
        },
        'Bronze': {
            'color': '#CD7F32',
            'icon': 'Bronze',
            'recommendations': [
                "Win-back campaigns with special offers",
                "Deep discounts to encourage repurchase",
                "Survey to understand pain points",
                "Simplified onboarding for easier engagement"
            ]
        }
    }
    
    # Display recommendations for each segment
    for segment, info in segments_info.items():
        if segment in df['CLV_Segment'].unique():
            segment_count = len(df[df['CLV_Segment'] == segment])
            segment_pct = (segment_count / len(df)) * 100
            avg_clv = df[df['CLV_Segment'] == segment]['CLV_Predictive'].mean()
            
            with st.expander(f"{info['icon']} {segment} Customers ({segment_count:,} customers, {segment_pct:.1f}%)"):
                st.markdown(f"**Average CLV: ${avg_clv:,.0f}**")
                st.markdown("**Recommended Actions:**")
                for rec in info['recommendations']:
                    st.markdown(f"• {rec}")

def main():
    """Main dashboard application"""
    # Header
    st.markdown('<div class="main-header">Customer Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Comprehensive insights into customer behavior, segmentation, and lifetime value**")
    
    # Load data
    df, stats = load_data()
    
    if df is None or stats is None:
        st.error("Failed to load data. Please check the data files.")
        return
    
    # Sidebar
    st.sidebar.header("Navigation")
    
    # Main navigation
    page = st.sidebar.selectbox(
        "Choose Analysis",
        ["Executive Summary", "RFM Analysis", "CLV Analysis", 
         "K-Means Clustering", "Customer Explorer", "Recommendations"]
    )
    
    # Display KPI metrics at the top
    st.markdown("## Key Performance Indicators")
    create_metric_cards(stats)
    st.markdown("---")
    
    # Main content based on page selection
    if page == "Executive Summary":
        st.markdown("## Executive Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Customer Segmentation Overview")
            segment_counts = df['Customer_Segment'].value_counts()
            fig = px.pie(values=segment_counts.values, names=segment_counts.index, 
                        title="Customer Value Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Revenue Distribution")
            revenue_by_segment = df.groupby('Customer_Segment')['Monetary'].sum().sort_values(ascending=False)
            fig = px.bar(x=revenue_by_segment.index, y=revenue_by_segment.values,
                        title="Total CLV by Segment")
            st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("### Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            diamond_pct = len(df[df['CLV_Segment'] == 'Diamond']) / len(df) * 100
            st.metric("Diamond Customers", f"{diamond_pct:.1f}%", "Top value tier")
        
        with col2:
            repeat_customers = len(df[df['Frequency'] > 1]) / len(df) * 100
            st.metric("Repeat Customers", f"{repeat_customers:.1f}%", "Customer retention")
        
        with col3:
            avg_frequency = df['Frequency'].mean()
            st.metric("Avg Orders per Customer", f"{avg_frequency:.1f}", "Purchase frequency")
    
    elif page == "RFM Analysis":
        create_rfm_analysis(df)
    
    elif page == "CLV Analysis":
        create_clv_analysis(df)
    
    elif page == "K-Means Clustering":
        create_kmeans_analysis(df)
    
    elif page == "Customer Explorer":
        create_customer_explorer(df)
    
    elif page == "Recommendations":
        create_business_recommendations(df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        Customer Analytics Dashboard | Built with Streamlit | Data Science Portfolio Project
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
