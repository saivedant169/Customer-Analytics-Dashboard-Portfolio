import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Page configuration
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def main():
    st.title("🎯 Customer Analytics Dashboard")
    st.markdown("### Comprehensive RFM Analysis, Customer Segmentation & CLV Insights")
    
    # Load data
    df, stats = load_data()
    
    if df is None or stats is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose Analysis", 
                               ["Overview", "RFM Analysis", "Customer Segments", "Cluster Analysis"])
    
    # KPI Metrics
    st.markdown("## Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", f"{stats['total_customers']:,}")
    
    with col2:
        st.metric("Total Revenue", f"${stats['total_revenue']:,.2f}")
    
    with col3:
        st.metric("Avg Revenue/Customer", f"${stats['avg_monetary']:,.0f}")
    
    with col4:
        top_segment = max(stats['segment_distribution'], key=stats['segment_distribution'].get)
        st.metric("Top Segment", top_segment)
    
    st.markdown("---")
    
    if page == "Overview":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Customer Segment Distribution")
            segment_counts = df['Customer_Segment'].value_counts()
            fig = px.pie(values=segment_counts.values, names=segment_counts.index, 
                        title="RFM Customer Segments")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Cluster Distribution")
            cluster_counts = df['Cluster_Name'].value_counts()
            fig = px.pie(values=cluster_counts.values, names=cluster_counts.index, 
                        title="K-Means Clusters")
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "RFM Analysis":
        st.markdown("### RFM Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = px.histogram(df, x='Recency', title='Recency Distribution', 
                             labels={'Recency': 'Days Since Last Purchase'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(df, x='Frequency', title='Frequency Distribution',
                             labels={'Frequency': 'Number of Purchases'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = px.histogram(df, x='Monetary', title='Monetary Distribution',
                             labels={'Monetary': 'Total Spent ($)'})
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Customer Segments":
        st.markdown("### Customer Segment Analysis")
        
        # Segment statistics
        segment_stats = df.groupby('Customer_Segment').agg({
            'CustomerID': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2)
        segment_stats.columns = ['Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']
        
        st.dataframe(segment_stats, use_container_width=True)
        
        # Segment comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=segment_stats.index, y=segment_stats['Count'], 
                        title="Customers by Segment")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=segment_stats.index, y=segment_stats['Avg_Monetary'], 
                        title="Average Revenue by Segment")
            st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Cluster Analysis":
        st.markdown("### K-Means Cluster Analysis")
        
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
        fig = px.scatter(df, x='Recency', y='Monetary', color='Cluster_Name',
                        title="Customer Clusters: Recency vs Monetary",
                        labels={'Recency': 'Days Since Last Purchase', 'Monetary': 'Total Spent ($)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("**Customer Analytics Dashboard** | Powered by Streamlit")

if __name__ == "__main__":
    main()
