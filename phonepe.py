import streamlit as st
import pymysql
import pandas as pd
#import Pylance 
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="PhonePe Dashboard")

# MySQL Database Connection
import mysql.connector
connection = mysql.connector.connect (
    host =  "localhost",
    user = "root",
    password = "12345678",
    database = "phonepe"

)

cursor = connection.cursor()

# Navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Select Page:", ["Home Page", "Business Use Cases"])

if page_selection == "Home Page":
    st.title("🏦 PhonePe Dashboard - India")

    # Fetch Data from MySQL
    cursor.execute("SELECT SUM(Transaction_count) FROM aggregate_transaction")
    total_transactions = cursor.fetchone()[0]


    cursor.execute("SELECT COALESCE(SUM(Insurance_count), 0), COALESCE(SUM(Insurance_amount), 0) FROM aggregate_insurance")
    total_insurance, total_insurance_amount = cursor.fetchone()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Transactions", value=f"{total_transactions:,}")
    with col2:
        st.metric(label="Total Insurance Policies", value=f"{total_insurance:,}")
    with col3:
        st.metric(label="Total Insurance Amount", value=f"₹{total_insurance_amount:,.2f}")

    # Selection Buttons
    col1, col2 = st.columns(2)
    with col1:
        show_transactions = st.button("💰 Show Transactions")
    with col2:
        show_insurance = st.button("📝 Show Insurance")

    # Define default metric
    metric_selection = "Total Transactions"
    color_scale = "Sunset"
    label = "Total Transactions"
    query = """
        SELECT State, SUM(Transaction_count) AS Value
        FROM aggregate_transaction
        GROUP BY State
    """

    # Update metric based on button click
    
    metric_selection = "Total Insurance Policies"
    color_scale = "Tealrose"
    label = "Total Insurance Policies"
    query = """
            SELECT State, SUM(Insurance_count) AS Value
            FROM aggregate_insurance
            GROUP BY State
        """

    # Fetch Data from MySQL
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["State", "Value"])

    # Convert Value column to numeric
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # State Mapping
    map_state = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar',
        'andhra-pradesh': 'Andhra Pradesh',
        'arunachal-pradesh': 'Arunachal Pradesh',
        'assam': 'Assam',
        'bihar': 'Bihar',
        'chandigarh': 'Chandigarh',
        'chhattisgarh': 'Chhattisgarh',
        'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'delhi': 'Delhi',
        'goa': 'Goa',
        'gujarat': 'Gujarat',
        'haryana': 'Haryana',
        'himachal-pradesh': 'Himachal Pradesh',
        'jammu-&-kashmir': 'Jammu & Kashmir',
        'jharkhand': 'Jharkhand',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'ladakh': 'Ladakh',
        'madhya-pradesh': 'Madhya Pradesh',
        'maharashtra': 'Maharashtra',
        'manipur': 'Manipur',
        'meghalaya': 'Meghalaya',
        'mizoram': 'Mizoram',
        'nagaland': 'Nagaland',
        'odisha': 'Odisha',
        'puducherry': 'Puducherry',
        'punjab': 'Punjab',
        'rajasthan': 'Rajasthan',
        'sikkim': 'Sikkim',
        'tamil-nadu': 'Tamil Nadu',
        'telangana': 'Telangana',
        'tripura': 'Tripura',
        'uttar-pradesh': 'Uttar Pradesh',
        'uttarakhand': 'Uttarakhand',
        'west-bengal': 'West Bengal'
    }

    df["State"] = df["State"].str.lower().map(map_state)

    # Load GeoJSON and Create Map
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="State",
        color="Value",
        color_continuous_scale=color_scale,
        labels={'Value': label},
        hover_name="State",
        hover_data={"Value": True, "State": False}  # ✅ Display value & hide redundant state name
    )

    # ✅ Fix: Zoom in on India & Hide World Map
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
    )

    # ✅ Remove color scale (legend)
    fig.update_layout(
        width=1200,
        height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=True , # ✅ Hides the color scale completely
        legend=dict(orientation="v", x=1, y=0.5)  # ✅ Move legend to right
    )
    # Show India Map
    st.plotly_chart(fig, use_container_width=True)

    # 🏆 **Separate Top 10 Buttons**
    col4, col5 = st.columns(2)
    
    with col4:
        if st.button("🏆 Show Top 10 Transactions"):
            cursor.execute("""
                SELECT State, SUM(Transaction_count) AS Value
                FROM aggregate_transaction
                GROUP BY State
                ORDER BY Value DESC
                LIMIT 10
            """)
            top_10_transactions = pd.DataFrame(cursor.fetchall(), columns=["State", "Value"])
            st.subheader("🏆 Top 10 States by Transactions")
            st.table(top_10_transactions)


    with col5:
        if st.button("🏆 Show Top 10 Insurance Policies"):
            cursor.execute("""
                SELECT State, SUM(Insurance_count) AS Value
                FROM aggregate_insurance
                GROUP BY State
                ORDER BY Value DESC
                LIMIT 10
            """)
            top_10_insurance = pd.DataFrame(cursor.fetchall(), columns=["State", "Value"])
            st.subheader("🏆 Top 10 States by Insurance Policies")
            st.table(top_10_insurance)

elif page_selection == "Business Use Cases":
    st.title("Business Use Cases Analysis")
    business_cases = [
        "Decoding Transaction Dynamics on PhonePe",
        "Insurance Penetration and Growth Potential Analysis",
        "Transaction Analysis for Market Expansion",
        "Insurance Engagement Analysis",
        "User Engagement and Growth Strategy"
       
    ]
    selected_case = st.selectbox("Select a Business Use Case", business_cases)
    st.write(f"### Analysis for: {selected_case}")
    st.write("(Detailed insights will be displayed based on the selected business use case)")
    
    if selected_case == "Decoding Transaction Dynamics on PhonePe":
        st.write(f"### Scenario:")
        st.write(f"PhonePe, a leading digital payments platform, has recently identified significant variations in transaction behavior across states, quarters, and payment categories. While some regions and transaction types demonstrate consistent growth, others show stagnation or decline. The leadership team seeks a deeper understanding of these patterns to drive targeted business strategies.")
        query = """
            SELECT Year,State, Quarter, Transaction_type, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount
            FROM aggregate_transaction
            GROUP BY Year,State, Quarter, Transaction_type
        """
        cursor.execute(query)
        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=["Year", "State", "Quarter", "Transaction_Type", "Total Transactions", "Total Amount"])

        # Convert Total Transactions to numeric
        df["Total Transactions"] = pd.to_numeric(df["Total Transactions"], errors="coerce")
                
        st.subheader("Transaction Trends Across States")
        fig = px.bar(df, x="State", y="Total Transactions", color="Transaction_Type", barmode="group",
                     title="Transaction Count by State and Payment Category")
        st.plotly_chart(fig)

        # Convert Year and Quarter to Period format
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", states)
        df_filtered = df[df["State"] == selected_state]
        
        # Line Chart for Yearly and Quarterly Trends
        st.subheader("Yearly and Quarterly Trends for State Wise Selection")
        fig_line = px.line(df_filtered, x="Period", y="Total Transactions", title=f"Transaction Trends in {selected_state}", markers=True)
        st.plotly_chart(fig_line)

        # Pie Chart for Payment Category
        st.subheader("Transaction Distribution by Payment Category")
        df_pie = df_filtered.groupby("Transaction_Type")["Total Transactions"].sum().reset_index()
        fig_pie = px.pie(df_pie, names="Transaction_Type", values="Total Transactions", title=f"Payment Category Distribution in {selected_state}")
        st.plotly_chart(fig_pie)
        
    elif selected_case == "Insurance Penetration and Growth Potential Analysis":
        st.write(f"### Scenario:")
        st.write(f"PhonePe has ventured into the insurance domain, providing users with options to secure various policies. With increasing transactions in this segment, the company seeks to analyze its growth trajectory and identify untapped opportunities for insurance adoption at the state level. This data will help prioritize regions for marketing efforts and partnerships with insurers.")
        query = """
            SELECT Year, State, Quarter, SUM(Insurance_count) AS Total_Policy, SUM(Insurance_amount) AS Total_Amount
            FROM aggregate_insurance
            GROUP BY Year, State, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["Year", "State", "Quarter", "Total_Policy", "Total Amount"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # Bar Chart - Total Insurance Transactions by State
        st.subheader("Total Insurance Transactions Across States")
        fig_bar = px.bar(df.groupby("State")["Total_Policy"].sum().reset_index(), x="State", y="Total_Policy", title="Total Insurance Policy Vs. State", color="Total_Policy")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
            
        # Line Chart - Growth Trend of Insurance Transactions Over Time
        st.subheader(f"Insurance Policy Growth Over Time For {selected_state}")
        fig_line = px.line(df.groupby("Period")["Total_Policy"].sum().reset_index(), x="Period", y="Total_Policy", title="Insurance Transactions Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Bar Chart - Insurance Amount by Year/Quarter
        st.subheader(f"Insurance Amount Trends Over Time For {selected_state}")
        fig_insurance_amount = px.bar(df.groupby("Period")["Total Amount"].sum().reset_index(), x="Period", y="Total Amount", title="Insurance Amount by Year/Quarter", color="Total Amount")
        st.plotly_chart(fig_insurance_amount, use_container_width=True)

    elif selected_case == "Transaction Analysis for Market Expansion":
        st.write(f"### Scenario:")
        st.write(f"PhonePe operates in a highly competitive market, and understanding transaction dynamics at the state level is crucial for strategic decision-making. With a growing number of transactions across different regions, the company seeks to analyze its transaction data to identify trends, opportunities, and potential areas for expansion.")
        query = """
            SELECT State, District, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount, Year, Quarter
            FROM map_transaction
            GROUP BY State, District, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["State", "District", "Total Transactions", "Total Amount", "Year", "Quarter"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
        
        # Line Chart - Transaction Trends by Type
        st.subheader(f"Transaction Trends Over Time by District - {selected_state}")
        fig_line = px.line(df, x="Period", y="Total Transactions", color="District", title="Transaction Trends Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Bar Chart - Transactions by Type
        st.subheader(f"Total Transactions by District - {selected_state}")
        fig_bar = px.bar(df, x="District", y="Total Transactions", title="Total Transactions by Type", color="District")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Bubble Chart - Transactions by Type and Amount
        st.subheader(f"Transactions by Type and Amount - {selected_state}")
        fig_bubble = px.scatter(df, x="Total Transactions", y="Total Amount", color="District", size="Total Amount", hover_name="District", title="Transactions by Policy and Amount", size_max=50)
        st.plotly_chart(fig_bubble, use_container_width=True)

    elif selected_case == "Insurance Engagement Analysis":
        st.write(f"### Scenario:")
        st.write(f"PhonePe aims to analyze insurance transactions across various states and districts to understand the uptake of insurance services among users. This analysis will provide insights into user behavior, market demand, and potential areas for growth in insurance offerings.")
        query = """
            SELECT State, District, SUM(Insurance_count) AS Total_Insurance, SUM(Insurance_amount) AS Total_Amount, Year, Quarter
            FROM map_insurance
            GROUP BY State, District, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=["State", "District", "Total Insurance", "Total Amount", "Year", "Quarter"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
        
        # Ensure numeric values for aggregation
        df["Total Insurance"] = pd.to_numeric(df["Total Insurance"], errors="coerce").fillna(0)
        df["Total Amount"] = pd.to_numeric(df["Total Amount"], errors="coerce").fillna(0)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
        
        # Sunburst Chart - Insurance Distribution by State and District
        st.subheader("Insurance Distribution by State and District")
        fig_sunburst = px.sunburst(df, path=["State", "District"], values="Total Insurance")
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Scatter Plot - Insurance Count vs. Amount by District
        st.subheader("Insurance Count vs. Amount by District")
        fig_scatter = px.scatter(df, x="Total Insurance", y="Total Amount", color="State", hover_name="District")
        st.plotly_chart(fig_scatter, use_container_width=True)

    elif selected_case == "User Engagement and Growth Strategy":
        st.write(f"### Scenario:")
        st.write(f"PhonePe has ventured into identifying how many users per district are using Phonepe and based on this they will work on strategies to increase the user count on less used districts. Also this will help the company to understand active users based on district.")
        query = """
            SELECT State, District, sum(registeredUsers) as Registered_users_count, sum(appOpens) as App_Opened, Year, Quarter
            FROM map_user 
            GROUP BY State, District, Year, Quarter
        """
        cursor.execute(query)
        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=["State", "District", "Registered users count", "App Opened", "Year", "Quarter"])
        df["Period"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)

        # Ensure numeric values for aggregation
        df["Registered users count"] = pd.to_numeric(df["Registered users count"], errors="coerce").fillna(0)
        df["App Opened"] = pd.to_numeric(df["App Opened"], errors="coerce").fillna(0)
        

          # Bar Chart - Registered Users Count by State
        st.subheader("Registered Users Count Across States")
        fig_bar = px.bar(df.groupby("State")["Registered users count"].sum().reset_index(), x="State", y="Registered users count", title="Registered Users Count Vs. State", color="Registered users count")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # State Selection Filter
        states = df["State"].unique().tolist()
        selected_state = st.selectbox("Select State", ["All"] + states)
        
        if selected_state != "All":
            df = df[df["State"] == selected_state]
            
        # Line Chart - App Opened by Users Over Time
        st.subheader(f"App Opened by Users Over Time For {selected_state}")
        fig_line = px.line(df.groupby("Period")["App Opened"].sum().reset_index(), x="Period", y="App Opened", title="App Opened by Users Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
        
      
# Close Database Connection
cursor.close()
connection.close()


