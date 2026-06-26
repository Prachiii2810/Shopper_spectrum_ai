import streamlit as st
import pandas as pd
import pickle

# 1. Page Configuration & Custom Theme
st.set_page_config(
    page_title="Shopper Spectrum Pro", 
    page_icon="🛍️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS styling for premium UI look
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid #4A90E2;
    }
    .recommendation-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }
    .recommendation-box:hover {
        transform: translateY(-2px);
        border-color: #4A90E2;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Optimized Data Loading
@st.cache_resource
def load_data():
    with open("app_data.pkl", "rb") as f:
        return pickle.load(f)

try:
    data = load_data()
    rfm_df = data['rfm_data']
    reco_map = data['recommendations']
    products = data['product_list']
except FileNotFoundError:
    st.error("❌ 'app_data.pkl' not found! Please run 'python pipeline.py' first in your terminal.")
    st.stop()

# 3. Interactive Sidebar Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    st.title("Control Panel")
    st.markdown("Customize your view settings below.")
    
    # Global visual toggle
    show_raw_data = st.checkbox("Show Raw Segment Database Table", value=False)
    
    st.markdown("---")
    st.markdown("### Segment Quick Stats")
    segment_counts = rfm_df['Segment'].value_counts()
    for seg, count in segment_counts.items():
        st.caption(f"**{seg}**: {count} users")

# 4. Main App Layout Header
st.title("🛍️ Shopper Spectrum: Enterprise Intelligence AI")
st.markdown("Evaluate customer lifecycles and trigger precision cross-selling recommendations instantly.")

# Create main tab structure
tab1, tab2 = st.tabs(["🎯 Customer Intelligence Hub", "📦 Next-Best-Item Recommendation Engine"])

# ==========================================
# TAB 1: ADVANCED CUSTOMER SEGMENTATION
# ==========================================
with tab1:
    st.markdown("### Live Behavioral Profile Lookup")
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.info("💡 Pick an existing client ID to auto-populate historical traits, or input mock values manually.")
        mode = st.radio("Search Selection Mode:", ["Select Existing Customer ID", "Manual Parameter Profile Input"])
        
        if mode == "Select Existing Customer ID":
            cust_id = st.selectbox("Search Customer ID Matrix:", [""] + list(rfm_df.index))
            if cust_id != "":
                row = rfm_df.loc[cust_id]
                rec = int(row['Recency'])
                freq = int(row['Frequency'])
                mon = float(row['Monetary'])
                segment = row['Segment']
            else:
                rec, freq, mon, segment = 0, 0, 0.0, None
        else:
            rec = st.slider("Recency (Days since last order):", min_value=1, max_value=365, value=30)
            freq = st.slider("Frequency (Total invoices placed):", min_value=1, max_value=100, value=5)
            mon = st.number_input("Monetary Value Overall Spends ($):", min_value=0.1, max_value=100000.0, value=500.0)
            
            if rec <= 30 and freq >= 5: segment = "High Value Customer"
            elif rec <= 90: segment = "Regular Customer"
            elif rec <= 180: segment = "Occasional Customer"
            else: segment = "At-Risk Customer"

    with col2:
        if segment:
            st.subheader("Customer Status Summary")
            
            colors = {
                "High Value Customer": "#2ecc71", 
                "Regular Customer": "#3498db", 
                "Occasional Customer": "#f1c40f", 
                "At-Risk Customer": "#e74c3c"
            }
            
            # Interactive Styled Banner Box using single-line string injection
            banner_style = f"background-color:{colors[segment]}15; padding:25px; border-radius:12px; border:2px dashed {colors[segment]}; text-align:center;"
            st.markdown(f'<div style="{banner_style}"><h2 style="margin:0; color:{colors[segment]}; font-weight:bold;">{segment}</h2><p style="margin:8px 0 0 0; color:#444; font-size:15px;">Target this profile with customized marketing strategies.</p></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Interactive Native KPI Metric Cards Layout
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="⏱️ Recency Interval", value=f"{rec} Days")
            with m_col2:
                st.metric(label="🔄 Transaction Frequency", value=f"{freq} Orders")
            with m_col3:
                st.metric(label="💰 Net Customer Value", value=f"${mon:,.2f}")
                
            # Fixed Dynamic Action Items Recommendation Accordion (Line 140 fix)
            with st.expander("🚀 Recommended Marketing Actions for This Customer"):
                if segment == "High Value Customer":
                    st.success("• Enroll in VIP Rewards Program\n\n• Provide exclusive first-look access to new collection arrivals.")
                elif segment == "Regular Customer":
                    st.info("• Send standard milestone multi-buy bundle offer codes\n\n• Upsell high-margin accessories.")
                elif segment == "Occasional Customer":
                    st.warning("• Distribute re-engagement discount vouchers\n\n• Send customized product drop updates based on preferences.")
                else:
                    st.error("• Trigger Win-Back email campaign series immediately\n\n• Request feedback via short surveys with incentive codes.")

    # Interactive Global Data Table Section Triggered by Sidebar Toggle
    if show_raw_data:
        st.markdown("---")
        st.markdown("### Raw Client Analytics Database Matrix View")
        search_filter = st.text_input("⚡ Quick Filter Table by Segment Label Name (e.g., At-Risk):", "")
        if search_filter:
            filtered_rfm = rfm_df[rfm_df['Segment'].str.contains(search_filter, case=False)]
        else:
            filtered_rfm = rfm_df
            
        st.dataframe(filtered_rfm, use_container_width=True)

# ==========================================
# TAB 2: PRODUCT RECOMMENDATIONS
# ==========================================
with tab2:
    st.markdown("### Basket Association Discovery")
    st.write("Pick an item from the searchable selection engine below to unlock real-time predictions for complementary items.")
    
    selected_item = st.selectbox("🔍 Search or Type Product Description Name:", [""] + products)
    
    if selected_item:
        st.markdown(f"#### 🎯 Top 5 Smart Cross-Sell Recommendations For: `'{selected_item}'`")
        recommendations = reco_map.get(selected_item, [])
        
        if recommendations:
            cols = st.columns(len(recommendations))
            for i, item in enumerate(recommendations):
                with cols[i]:
                    box_html = f'<div class="recommendation-box"><span style="font-size: 24px;">📦</span><br><br><span style="font-size: 14px; font-weight: 600; color: #2C3E50; display: block; min-height: 50px;">{item}</span></div>'
                    st.markdown(box_html, unsafe_allow_html=True)
                    
                    if st.button(f"Analyze Rank {i+1}", key=f"btn_{i}"):
                        st.toast(f"Analyzing warehouse inventory logs for: {item}", icon="⏳")
        else:
            st.warning("⚠️ No distinct item association purchase history metrics exist for this item description catalog entry yet.")
