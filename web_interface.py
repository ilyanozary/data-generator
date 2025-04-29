import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from main import DataGenerator
import json
import yaml
import io
import base64
from typing import Dict, Any

# Page configuration
st.set_page_config(
    page_title="Advanced Data Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def get_table_download_link(df: pd.DataFrame, filename: str, file_type: str) -> str:
    """Generate a download link for the dataframe"""
    if file_type == 'csv':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    elif file_type == 'json':
        json_str = df.to_json(orient='records')
        b64 = base64.b64encode(json_str.encode()).decode()
        return f'<a href="data:application/json;base64,{b64}" download="{filename}.json">Download JSON</a>'

def main():
    # Initialize session state
    if 'generator' not in st.session_state:
        st.session_state.generator = DataGenerator()
    
    # Sidebar
    with st.sidebar:
        st.title("🎛️ Configuration")
        
        # Data Generation Settings
        st.header("Data Generation")
        num_users = st.slider("Number of Users", 1, 1000, 10)
        num_products = st.slider("Number of Products", 1, 1000, 20)
        num_orders = st.slider("Number of Orders", 1, 1000, 50)
        locale = st.selectbox("Locale", ["en_US", "fa_IR"])
        
        if st.button("Generate Data", key="generate"):
            with st.spinner("Generating data..."):
                st.session_state.generator = DataGenerator(locale=locale)
                st.session_state.generator.generate_data(num_users, num_products, num_orders)
                st.success("Data generated successfully!")
        
        # Export Settings
        st.header("Export Options")
        export_format = st.selectbox("Export Format", ["CSV", "JSON"])
        if st.button("Export Data", key="export"):
            with st.spinner("Exporting data..."):
                st.session_state.generator.export_data(export_format.lower())
                st.success(f"Data exported to {export_format} successfully!")

    # Main content
    st.title("📊 Advanced Data Generator Dashboard")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", len(st.session_state.generator.session.query(st.session_state.generator.User).all()))
    with col2:
        st.metric("Total Products", len(st.session_state.generator.session.query(st.session_state.generator.Product).all()))
    with col3:
        st.metric("Total Orders", len(st.session_state.generator.session.query(st.session_state.generator.Order).all()))
    
    # Data Tabs
    tab1, tab2, tab3 = st.tabs(["Users", "Products", "Orders"])
    
    with tab1:
        st.header("Users Data")
        users = st.session_state.generator.session.query(st.session_state.generator.User).all()
        users_df = pd.DataFrame([user.__dict__ for user in users])
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            active_filter = st.selectbox("Active Status", ["All", "Active", "Inactive"])
        with col2:
            age_range = st.slider("Age Range", 0, 100, (18, 65))
        
        # Apply filters
        if active_filter != "All":
            users_df = users_df[users_df['is_active'] == (active_filter == "Active")]
        
        # Display data
        st.dataframe(users_df)
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(users_df, x='birth_date', title='User Age Distribution')
            st.plotly_chart(fig)
        with col2:
            fig = px.pie(users_df, names='is_active', title='Active vs Inactive Users')
            st.plotly_chart(fig)
        
        # Export
        st.markdown(get_table_download_link(users_df, "users", "csv"), unsafe_allow_html=True)
    
    with tab2:
        st.header("Products Data")
        products = st.session_state.generator.session.query(st.session_state.generator.Product).all()
        products_df = pd.DataFrame([product.__dict__ for product in products])
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.multiselect("Categories", products_df['category'].unique())
        with col2:
            price_range = st.slider("Price Range", 
                                  float(products_df['price'].min()), 
                                  float(products_df['price'].max()), 
                                  (float(products_df['price'].min()), 
                                   float(products_df['price'].max())))
        
        # Apply filters
        if category_filter:
            products_df = products_df[products_df['category'].isin(category_filter)]
        products_df = products_df[(products_df['price'] >= price_range[0]) & 
                                (products_df['price'] <= price_range[1])]
        
        # Display data
        st.dataframe(products_df)
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            fig = px.box(products_df, y='price', title='Product Price Distribution')
            st.plotly_chart(fig)
        with col2:
            fig = px.bar(products_df.groupby('category').size().reset_index(name='count'),
                        x='category', y='count', title='Products by Category')
            st.plotly_chart(fig)
        
        # Export
        st.markdown(get_table_download_link(products_df, "products", "csv"), unsafe_allow_html=True)
    
    with tab3:
        st.header("Orders Data")
        orders = st.session_state.generator.session.query(st.session_state.generator.Order).all()
        orders_df = pd.DataFrame([order.__dict__ for order in orders])
        
        # Join with users and products
        users_df = pd.DataFrame([user.__dict__ for user in st.session_state.generator.session.query(st.session_state.generator.User).all()])
        products_df = pd.DataFrame([product.__dict__ for product in st.session_state.generator.session.query(st.session_state.generator.Product).all()])
        
        orders_df = orders_df.merge(users_df[['id', 'name']], left_on='user_id', right_on='id', suffixes=('', '_user'))
        orders_df = orders_df.merge(products_df[['id', 'name']], left_on='product_id', right_on='id', suffixes=('', '_product'))
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Order Status", orders_df['status'].unique())
        with col2:
            date_range = st.date_input("Date Range", 
                                     [datetime.now() - timedelta(days=30), 
                                      datetime.now()])
        
        # Apply filters
        if status_filter:
            orders_df = orders_df[orders_df['status'].isin(status_filter)]
        orders_df = orders_df[(orders_df['created_at'].dt.date >= date_range[0]) & 
                            (orders_df['created_at'].dt.date <= date_range[1])]
        
        # Display data
        st.dataframe(orders_df)
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(orders_df, names='status', title='Orders by Status')
            st.plotly_chart(fig)
        with col2:
            fig = px.line(orders_df.groupby(orders_df['created_at'].dt.date)['total_price'].sum().reset_index(),
                         x='created_at', y='total_price', title='Daily Revenue')
            st.plotly_chart(fig)
        
        # Export
        st.markdown(get_table_download_link(orders_df, "orders", "csv"), unsafe_allow_html=True)

if __name__ == "__main__":
    main() 