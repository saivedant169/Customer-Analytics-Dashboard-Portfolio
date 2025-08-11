import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and professional styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Custom metric styling */
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #3a4a5c;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00d4aa;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #b8c5d1;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid #3a4a5c;
    }
    
    .dashboard-title {
        color: #00d4aa;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .dashboard-subtitle {
        color: #b8c5d1;
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        text-align: center;
    }
    
    /* Section headers */
    .section-header {
        color: #00d4aa;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #00d4aa;
        padding-bottom: 0.5rem;
    }
    
    /* Streamlit tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2a5298;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        border: 1px solid #3a4a5c;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d4aa !important;
        color: #1a1a2e !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load customer data and statistics"""
    try:
        # Load customer data
        df = pd.read_csv('data/customer_analytics_data.csv')
        
        # Load statistics
        with open('data/dashboard_stats.json', 'r') as f:
            stats = json.load(f)
        
        return df, stats
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def create_metric_card(title, value, format_type="number"):
    """Create a styled metric card"""
    if format_type == "currency":
        if isinstance(value, (int, float)):
            display_value = f"${value:,.0f}"
        else:
            display_value = f"${value}"
    elif format_type == "percentage":
        display_value = f"{value}%"
    else:
        if isinstance(value, (int, float)):
            display_value = f"{value:,.0f}"
        else:
            display_value = str(value)
    
    return f"""
    <div class="metric-card">
        <p class="metric-value">{display_value}</p>
        <p class="metric-label">{title}</p>
    </div>
    """

def create_donut_chart(values, labels, title, colors=None):
    """Create a modern donut chart"""
    if colors is None:
        colors = ['#00d4aa', '#2a5298', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color='#1a1a2e', width=2)),
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#00d4aa'), x=0.5),
        showlegend=True,
        legend=dict(font=dict(color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=20, l=20, r=20),
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="dashboard-title">Customer Analytics Dashboard</h1>
        <p class="dashboard-subtitle">Comprehensive RFM Analysis, Customer Segmentation & CLV Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df, stats = load_data()
    
    if df is None or stats is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 RFM Analysis", "👥 Customer Segments", "🎯 Cluster Analysis"])
    
    with tab1:
        st.markdown('<p class="section-header">Key Performance Indicators</p>', unsafe_allow_html=True)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Total Customers", stats['total_customers']), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("Total Revenue", stats['total_revenue'], "currency"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Avg Revenue/Customer", stats['avg_monetary'], "currency"), unsafe_allow_html=True)
        
        with col4:
            top_segment = max(stats['segment_distribution'], key=stats['segment_distribution'].get)
            st.markdown(create_metric_card("Top Segment", top_segment, "text"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            segment_counts = df['Customer_Segment'].value_counts()
            fig = create_donut_chart(
                segment_counts.values, 
                segment_counts.index, 
                "Customer Segment Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            cluster_counts = df['Cluster_Name'].value_counts()
            fig = create_donut_chart(
                cluster_counts.values, 
                cluster_counts.index, 
                "Cluster Distribution",
                colors=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown('<p class="section-header">RFM Analysis Distribution</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = px.histogram(
                df, x='Recency', 
                title='Recency Distribution',
                nbins=30,
                color_discrete_sequence=['#00d4aa']
            )
            fig.update_layout(
                title=dict(font=dict(size=16, color='#00d4aa'), x=0.5),
                xaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(text='Days Since Last Purchase', font=dict(color='#b8c5d1'))),
                yaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                df, x='Frequency', 
                title='Frequency Distribution',
                nbins=30,
                color_discrete_sequence=['#2a5298']
            )
            fig.update_layout(
                title=dict(font=dict(size=16, color='#00d4aa'), x=0.5),
                xaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(text='Number of Purchases', font=dict(color='#b8c5d1'))),
                yaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = px.histogram(
                df, x='Monetary', 
                title='Monetary Distribution',
                nbins=30,
                color_discrete_sequence=['#ff6b6b']
            )
            fig.update_layout(
                title=dict(font=dict(size=16, color='#00d4aa'), x=0.5),
                xaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(text='Total Spent ($)', font=dict(color='#b8c5d1'))),
                yaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown('<p class="section-header">Customer Segment Analysis</p>', unsafe_allow_html=True)
        
        # Segment statistics
        segment_stats = df.groupby('Customer_Segment').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        segment_stats.columns = ['Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']
        
        st.dataframe(segment_stats, use_container_width=True)
        
        # Segment comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                x=segment_stats.index, 
                y=segment_stats['Count'], 
                title="Customers by Segment",
                color_discrete_sequence=['#00d4aa']
            )
            fig.update_layout(
                title=dict(font=dict(size=16, color='#00d4aa'), x=0.5),
                xaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                yaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=segment_stats.index, 
                y=segment_stats['Avg_Monetary'], 
                title="Average Revenue by Segment",
                color_discrete_sequence=['#2a5298']
            )
            fig.update_layout(
                title=dict(font=dict(size=16, color='#00d4aa'), x=0.5),
                xaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                yaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(font=dict(color='#b8c5d1'))),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown('<p class="section-header">K-Means Cluster Analysis</p>', unsafe_allow_html=True)
        
        # Cluster statistics
        cluster_stats = df.groupby('Cluster_Name').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        cluster_stats.columns = ['Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']
        
        st.dataframe(cluster_stats, use_container_width=True)
        
        # Scatter plot
        fig = px.scatter(
            df, x='Recency', y='Monetary', color='Cluster_Name',
            title="Customer Clusters: Recency vs Monetary Value",
            color_discrete_sequence=['#00d4aa', '#2a5298', '#ff6b6b', '#4ecdc4']
        )
        fig.update_layout(
            title=dict(font=dict(size=16, color='#00d4aa'), x=0.5),
            xaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(text='Days Since Last Purchase', font=dict(color='#b8c5d1'))),
            yaxis=dict(color='white', gridcolor='#3a4a5c', title=dict(text='Total Spent ($)', font=dict(color='#b8c5d1'))),
            legend=dict(font=dict(color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #b8c5d1; font-size: 0.9rem;">Customer Analytics Dashboard | Powered by Streamlit</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
