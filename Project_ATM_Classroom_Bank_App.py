import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Project ATM: Classroom Bank",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Project ATM: Classroom Bank & Account Portal")
st.caption("Pinoma Elementary School - SDO Cauayan City | Grade 4 Advisory Class")

# Student Database Initializer
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

# Initialize Session State
if 'balances' not in st.session_state:
    st.session_state.balances = {s['acc']: 50 for s in STUDENTS} # Initial 50 Merits starter bonus

if 'transactions' not in st.session_state:
    st.session_state.transactions = []
    for s in STUDENTS:
        st.session_state.transactions.append({
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Account": s['acc'],
            "Name": s['name'],
            "Particulars": "Initial Account Opening Bonus",
            "Earned": 50,
            "Spent": 0,
            "Balance": 50
        })

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/bank-building.png", width=80)
st.sidebar.title("ATM Navigation")
menu = st.sidebar.radio("Select Portal:", ["🔍 Student Balance Lookup", "🏆 Top Savers Leaderboard", "👩‍🏫 Teacher Admin Panel"])

if menu == "🔍 Student Balance Lookup":
    st.header("🔍 Check Account Balance")
    student_names = [f"{s['name']} ({s['acc']})" for s in STUDENTS]
    selected_student_str = st.selectbox("Select or Search Student Name / Account Number:", student_names)
    
    # Get selected student info
    acc_no = selected_student_str.split("(")[1].replace(")", "").strip()
    student_info = next(s for s in STUDENTS if s['acc'] == acc_no)
    curr_balance = st.session_state.balances[acc_no]
    
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("💳 **ATM CARD DETAILS**")
        st.markdown(f"**Cardholder:** {student_info['name']}")
        st.markdown(f"**Account No:** `{student_info['acc']}`")
        st.markdown(f"**Student ID:** `{student_info['lrn']}`")
        st.markdown(f"**Gender:** {student_info['gender']}")
        
    with col2:
        st.metric(label="CURRENT MERIT BALANCE", value=f"{curr_balance} Merits", delta="Active Account")
        
    st.subheader("📖 Passbook Transaction History")
    tx_df = pd.DataFrame(st.session_state.transactions)
    student_tx = tx_df[tx_df['Account'] == acc_no]
    st.dataframe(student_tx[['Date', 'Particulars', 'Earned', 'Spent', 'Balance']], use_container_width=True)

elif menu == "🏆 Top Savers Leaderboard":
    st.header("🏆 Top Savers Leaderboard")
    leaderboard_data = []
    for s in STUDENTS:
        leaderboard_data.append({
            "Student Name": s['name'],
            "Gender": s['gender'],
            "Account Number": s['acc'],
            "Current Merit Balance": st.session_state.balances[s['acc']]
        })
    df_lb = pd.DataFrame(leaderboard_data).sort_values(by="Current Merit Balance", ascending=False).reset_index(drop=True)
    df_lb.index += 1
    st.dataframe(df_lb, use_container_width=True)

elif menu == "👩‍🏫 Teacher Admin Panel":
    st.header("👩‍🏫 Teacher Admin Panel")
    pin = st.text_input("Enter Teacher Admin PIN:", type="password")
    
    if pin == "1234": # Default PIN
        st.success("Admin Authenticated!")
        student_names = [f"{s['name']} ({s['acc']})" for s in STUDENTS]
        selected_student_str = st.selectbox("Select Student to Deposit/Deduct:", student_names)
        acc_no = selected_student_str.split("(")[1].replace(")", "").strip()
        student_info = next(s for s in STUDENTS if s['acc'] == acc_no)
        
        st.write(f"Updating balance for: **{student_info['name']}** (Current: `{st.session_state.balances[acc_no]}` Merits)")
        
        action_type = st.radio("Transaction Type:", ["➕ Deposit Merits (Reward)", "➖ Deduct Merits (Store Purchase / Demerit)"])
        
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
        
        if preset_reason == "Custom Reason":
            reason = st.text_input("Custom Reason Description:")
        else:
            reason = preset_reason
            
        amount = st.number_input("Merit Amount:", min_value=1, value=10)
        
        if st.button("Submit Transaction"):
            if "Deposit" in action_type:
                st.session_state.balances[acc_no] += amount
                earned, spent = amount, 0
            else:
                st.session_state.balances[acc_no] -= amount
                earned, spent = 0, amount
                
            new_bal = st.session_state.balances[acc_no]
            st.session_state.transactions.append({
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Account": acc_no,
                "Name": student_info['name'],
                "Particulars": reason,
                "Earned": earned,
                "Spent": spent,
                "Balance": new_bal
            })
            st.success(f"Transaction Recorded! New Balance for {student_info['name']}: {new_bal} Merits.")
    elif pin != "":
        st.error("Incorrect Teacher PIN Code.")
