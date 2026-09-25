import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Page configuration
st.set_page_config(
    page_title="Project ATM: Classroom Bank",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Project ATM: Classroom Bank & Account Portal")
st.caption("Pinoma Elementary School - SDO Cauayan City | Grade 4 Advisory Class")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Function to load current balances & transactions from Google Sheets
@st.cache_data(ttl=5) # refresh every 5 seconds for real-time sync across devices
def load_data():
    try:
        df_balances = conn.read(worksheet="Balances", ttl=5)
        df_tx = conn.read(worksheet="Transactions", ttl=5)
        return df_balances, df_tx
    except Exception as e:
        st.error("Connecting to Google Sheets... Please ensure your Google Sheet connection is configured in Streamlit Secrets.")
        return None, None

df_balances, df_tx = load_data()

# Fallback Student Database if sheet is initializing
STUDENTS = [
    {"name": "FERNANDEZ, CHRISTAN LEE RAMOS", "gender": "Male", "acc": "4020-2026-0001", "lrn": "PES-G4-0001"},
    {"name": "MANUEL, JOHN FHILIP PARIÑAS", "gender": "Male", "acc": "4020-2026-0002", "lrn": "PES-G4-0002"},
    {"name": "MOLINA, JOMAR EJADA", "gender": "Male", "acc": "4020-2026-0003", "lrn": "PES-G4-0003"},
    {"name": "MOLINA, RICHMOND -", "gender": "Male", "acc": "4020-2026-0004", "lrn": "PES-G4-0004"},
    {"name": "VALIENTES, RAINIER CABANG", "gender": "Male", "acc": "4020-2026-0005", "lrn": "PES-G4-0005"},
    {"name": "AGUYEN, APRIL JOY JAVIER", "gender": "Female", "acc": "4020-2026-0006", "lrn": "PES-G4-0006"},
    {"name": "ALCANTARA, MEGAN FAITH LEDDA", "gender": "Female", "acc": "4020-2026-0007", "lrn": "PES-G4-0007"},
    {"name": "BALIGAT, PRIZHIA KEITH MAURICIO", "gender": "Female", "acc": "4020-2026-0008", "lrn": "PES-G4-0008"},
    {"name": "BUSTO, ELLAH FAYE LIBUNAO", "gender": "Female", "acc": "4020-2026-0009", "lrn": "PES-G4-0009"},
    {"name": "CABATBAT, JAMICA MAE CARBONEL", "gender": "Female", "acc": "4020-2026-0010", "lrn": "PES-G4-0010"},
    {"name": "CAPINDING, JOSLYN FAITH BUSLIG", "gender": "Female", "acc": "4020-2026-0011", "lrn": "PES-G4-0011"},
    {"name": "CARLIT, JAN ELLAH GHEIL MUNOZ", "gender": "Female", "acc": "4020-2026-0012", "lrn": "PES-G4-0012"},
    {"name": "DELA PENA, JULIA PABICO", "gender": "Female", "acc": "4020-2026-0013", "lrn": "PES-G4-0013"},
    {"name": "GOTANGO, CHARITY JOY DURAN", "gender": "Female", "acc": "4020-2026-0014", "lrn": "PES-G4-0014"},
    {"name": "JAMISON, CHARLENE MIA DRAPITE", "gender": "Female", "acc": "4020-2026-0015", "lrn": "PES-G4-0015"},
    {"name": "MANGUPIT, ANDREA ELLEN CONTADO", "gender": "Female", "acc": "4020-2026-0016", "lrn": "PES-G4-0016"},
    {"name": "MAURICIO, QUEEN ISABELLA LACBAYAN", "gender": "Female", "acc": "4020-2026-0017", "lrn": "PES-G4-0017"},
    {"name": "QUEDDING, MARY JOY MOLINA", "gender": "Female", "acc": "4020-2026-0018", "lrn": "PES-G4-0018"},
    {"name": "TANGONAN, ALTHEA CLAIRE CUNANAN", "gender": "Female", "acc": "4020-2026-0019", "lrn": "PES-G4-0019"},
    {"name": "VENTURA, JIANA MORALES", "gender": "Female", "acc": "4020-2026-0020", "lrn": "PES-G4-0020"}
]

# Sidebar Menu
st.sidebar.title("ATM Navigation")
menu = st.sidebar.radio("Select Portal:", ["🔍 Student Balance Lookup", "🏆 Top Savers Leaderboard", "👩‍🏫 Teacher Admin Panel"])

if df_balances is not None and df_tx is not None:
    if menu == "🔍 Student Balance Lookup":
        st.header("🔍 Check Account Balance")
        student_names = [f"{s['name']} ({s['acc']})" for s in STUDENTS]
        selected_student_str = st.selectbox("Select or Search Student Name / Account Number:", student_names)
        
        acc_no = selected_student_str.split("(")[1].replace(")", "").strip()
        student_info = next(s for s in STUDENTS if s['acc'] == acc_no)
        
        # Get balance from Google Sheets
        st_row = df_balances[df_balances['Account'] == acc_no]
        curr_balance = st_row['Balance'].values[0] if not st_row.empty else 50
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("💳 **ATM CARD DETAILS**")
            st.markdown(f"**Cardholder:** {student_info['name']}")
            st.markdown(f"**Account No:** `{student_info['acc']}`")
            st.markdown(f"**Student ID:** `{student_info['lrn']}`")
            st.markdown(f"**Gender:** {student_info['gender']}")
            
        with col2:
            st.metric(label="CURRENT MERIT BALANCE (Synced Cloud)", value=f"{curr_balance} Merits")
            
        st.subheader("📖 Passbook Transaction History")
        student_tx = df_tx[df_tx['Account'] == acc_no]
        st.dataframe(student_tx[['Date', 'Particulars', 'Earned', 'Spent', 'Balance']], use_container_width=True)

    elif menu == "🏆 Top Savers Leaderboard":
        st.header("🏆 Top Savers Leaderboard (Real-Time)")
        df_lb = df_balances.sort_values(by="Balance", ascending=False).reset_index(drop=True)
        df_lb.index += 1
        st.dataframe(df_lb[['Name', 'Gender', 'Account', 'Balance']], use_container_width=True)

    elif menu == "👩‍🏫 Teacher Admin Panel":
        st.header("👩‍🏫 Teacher Admin Panel (Cloud Sync)")
        pin = st.text_input("Enter Teacher Admin PIN:", type="password")
        
        if pin == "1234":
            st.success("Admin Authenticated!")
            student_names = [f"{s['name']} ({s['acc']})" for s in STUDENTS]
            selected_student_str = st.selectbox("Select Student:", student_names)
            acc_no = selected_student_str.split("(")[1].replace(")", "").strip()
            student_info = next(s for s in STUDENTS if s['acc'] == acc_no)
            
            action_type = st.radio("Transaction Type:", ["➕ Deposit Merits (Reward)", "➖ Deduct Merits (Store / Demerit)"])
            preset_reason = st.selectbox("Quick Preset Reason:", [
                "Perfect Weekly Attendance (+10)",
                "Daily Class Job Duty (+20)",
                "Academic Achievement / Quiz (+50)",
                "Good Deed / Character Star (+50)",
                "Active Class Participation (+10)",
                "Classroom Store Purchase (-)",
                "Classroom Disruption Demerit (-)",
                "Custom Reason"
            ])
            
            reason = st.text_input("Reason Description:") if preset_reason == "Custom Reason" else preset_reason
            amount = st.number_input("Merit Amount:", min_value=1, value=10)
            
            if st.button("Submit Transaction (Sync Across All Devices)"):
                st_row = df_balances[df_balances['Account'] == acc_no]
                old_bal = int(st_row['Balance'].values[0]) if not st_row.empty else 50
                
                if "Deposit" in action_type:
                    new_bal = old_bal + amount
                    earned, spent = amount, 0
                else:
                    new_bal = old_bal - amount
                    earned, spent = 0, amount
                
                # Update Balance in df
                df_balances.loc[df_balances['Account'] == acc_no, 'Balance'] = new_bal
                
                # New transaction row
                new_tx = pd.DataFrame([{
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Account": acc_no,
                    "Name": student_info['name'],
                    "Particulars": reason,
                    "Earned": earned,
                    "Spent": spent,
                    "Balance": new_bal
                }])
                
                updated_tx = pd.concat([df_tx, new_tx], ignore_index=True)
                
                # Write back to Google Sheets
                conn.update(worksheet="Balances", data=df_balances)
                conn.update(worksheet="Transactions", data=updated_tx)
                
                st.cache_data.clear()
                st.success(f"🎉 Cloud Synced! New Balance for {student_info['name']}: {new_bal} Merits. Check your tablet/laptop!")
        elif pin != "":
            st.error("Incorrect PIN Code.")
