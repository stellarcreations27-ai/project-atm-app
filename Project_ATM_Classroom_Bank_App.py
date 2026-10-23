import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Project ATM: Classroom Bank",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Project ATM: Classroom Bank & Account Portal")
st.caption("Marabulig 2 Elementary School - SDO Cauayan City | Grade 6 - Iris Advisory Class")

SHEET_ID = "1VONM8quKrJ6eGdh8eLz5796ll63h2zXjCkCxA2QAVeo"
BALANCES_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Balances"
TRANSACTIONS_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Transactions"

STUDENTS = [{'name': 'ANCHETA, IVAN GABONI', 'gender': 'Male', 'acc': '6020-2026-0001', 'lrn': 'M2ES-G6I-0001'}, {'name': 'BALA, ROMUEL SEROTE', 'gender': 'Male', 'acc': '6020-2026-0002', 'lrn': 'M2ES-G6I-0002'}, {'name': 'CABISO, MARVIN JR. PREPOSE', 'gender': 'Male', 'acc': '6020-2026-0003', 'lrn': 'M2ES-G6I-0003'}, {'name': 'DORINGO, RAIZEN PARTIDO', 'gender': 'Male', 'acc': '6020-2026-0004', 'lrn': 'M2ES-G6I-0004'}, {'name': 'ERCILLA, ZACHARY MARTIN', 'gender': 'Male', 'acc': '6020-2026-0005', 'lrn': 'M2ES-G6I-0005'}, {'name': 'PALLORINA, RAFAEL PALISOC', 'gender': 'Male', 'acc': '6020-2026-0006', 'lrn': 'M2ES-G6I-0006'}, {'name': 'VALERO, KENJIE PASCUA', 'gender': 'Male', 'acc': '6020-2026-0007', 'lrn': 'M2ES-G6I-0007'}, {'name': 'ALONZO, KRICHELLE GABRIELLA TAQUIQUI', 'gender': 'Female', 'acc': '6020-2026-0008', 'lrn': 'M2ES-G6I-0008'}, {'name': 'BELONIO, JOANNA BUDUAN', 'gender': 'Female', 'acc': '6020-2026-0009', 'lrn': 'M2ES-G6I-0009'}, {'name': 'CATUBAY, JENNY ROSE SAPIGAO', 'gender': 'Female', 'acc': '6020-2026-0010', 'lrn': 'M2ES-G6I-0010'}, {'name': 'FERNANDEZ, YHANA TACAC', 'gender': 'Female', 'acc': '6020-2026-0011', 'lrn': 'M2ES-G6I-0011'}, {'name': 'GABONI, KATHLIAN FELIPE', 'gender': 'Female', 'acc': '6020-2026-0012', 'lrn': 'M2ES-G6I-0012'}, {'name': 'LANGUIDO, MARIA ELENA MARIANO', 'gender': 'Female', 'acc': '6020-2026-0013', 'lrn': 'M2ES-G6I-0013'}, {'name': 'MIER, PAULYN GRACE BUDUAN', 'gender': 'Female', 'acc': '6020-2026-0014', 'lrn': 'M2ES-G6I-0014'}, {'name': 'QUINTERO, JHAMIRA AGCAOILI', 'gender': 'Female', 'acc': '6020-2026-0015', 'lrn': 'M2ES-G6I-0015'}, {'name': 'SAPIGAO, ANGEL BUHANGIN', 'gender': 'Female', 'acc': '6020-2026-0016', 'lrn': 'M2ES-G6I-0016'}, {'name': 'VELASCO, JANELLA FEY', 'gender': 'Female', 'acc': '6020-2026-0017', 'lrn': 'M2ES-G6I-0017'}, {'name': 'VIERNES, TWILA MAE BUDUAN', 'gender': 'Female', 'acc': '6020-2026-0018', 'lrn': 'M2ES-G6I-0018'}]

if "balances_df" not in st.session_state:
    try:
        df_b = pd.read_csv(BALANCES_CSV_URL)
        if "Account" in df_b.columns and not df_b.empty:
            st.session_state["balances_df"] = df_b
        else:
            raise ValueError("Sheet empty")
    except Exception:
        st.session_state["balances_df"] = pd.DataFrame([{
            "Account": s['acc'],
            "Name": s['name'],
            "Gender": s['gender'],
            "Balance": 50
        } for s in STUDENTS])

if "tx_df" not in st.session_state:
    try:
        df_t = pd.read_csv(TRANSACTIONS_CSV_URL)
        if "Account" in df_t.columns and not df_t.empty:
            st.session_state["tx_df"] = df_t
        else:
            raise ValueError("Sheet empty")
    except Exception:
        st.session_state["tx_df"] = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Account": s['acc'],
            "Name": s['name'],
            "Particulars": "Initial Account Opening Bonus",
            "Earned": 50,
            "Spent": 0,
            "Balance": 50
        } for s in STUDENTS])

st.sidebar.title("ATM Navigation")
st.sidebar.info("💳 Project ATM Portal Active | Marabulig 2 ES - Grade 6 Iris")
menu = st.sidebar.radio("Select Portal:", ["🔍 Student Balance Lookup", "🏆 Top Savers Leaderboard", "👩‍🏫 Teacher Admin Panel"])

df_bal = st.session_state["balances_df"]
df_tx = st.session_state["tx_df"]

if menu == "🔍 Student Balance Lookup":
    st.header("🔍 Check Account Balance")
    student_names = [f"{s['name']} ({s['acc']})" for s in STUDENTS]
    selected_student_str = st.selectbox("Select or Search Student Name / Account Number:", student_names)
    
    acc_no = selected_student_str.split("(")[1].replace(")", "").strip()
    student_info = next(s for s in STUDENTS if s['acc'] == acc_no)
    
    bal_match = df_bal[df_bal['Account'] == acc_no]
    curr_balance = int(bal_match['Balance'].values[0]) if not bal_match.empty else 50
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("💳 **ATM CARD DETAILS**")
        st.markdown(f"**Cardholder:** {student_info['name']}")
        st.markdown(f"**Account No:** `{student_info['acc']}`")
        st.markdown(f"**Student ID:** `{student_info['lrn']}`")
        st.markdown(f"**Class:** Grade 6 - Iris (Marabulig 2 ES)")
        st.markdown(f"**Gender:** {student_info['gender']}")
        
    with col2:
        st.metric(label="CURRENT MERIT BALANCE", value=f"{curr_balance} Merits")
        
    st.subheader("📖 Passbook Transaction History")
    student_tx = df_tx[df_tx['Account'] == acc_no]
    st.dataframe(student_tx[['Date', 'Particulars', 'Earned', 'Spent', 'Balance']], use_container_width=True)

elif menu == "🏆 Top Savers Leaderboard":
    st.header("🏆 Top Savers Leaderboard - Grade 6 Iris")
    df_lb = df_bal.sort_values(by="Balance", ascending=False).reset_index(drop=True)
    df_lb.index += 1
    st.dataframe(df_lb[['Name', 'Gender', 'Account', 'Balance']], use_container_width=True)

elif menu == "👩‍🏫 Teacher Admin Panel":
    st.header("👩‍🏫 Teacher Admin Panel - Grade 6 Iris")
    pin = st.text_input("Enter Teacher Admin PIN:", type="password")
    
    if pin == "1234":
        st.success("Admin Authenticated! Welcome Teacher Sheila Micah T. Yao")
        student_names = [f"{s['name']} ({s['acc']})" for s in STUDENTS]
        selected_student_str = st.selectbox("Select Student:", student_names)
        acc_no = selected_student_str.split("(")[1].replace(")", "").strip()
        student_info = next(s for s in STUDENTS if s['acc'] == acc_no)
        
        bal_match = df_bal[df_bal['Account'] == acc_no]
        curr_balance = int(bal_match['Balance'].values[0]) if not bal_match.empty else 50
        
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
        
        if st.button("Submit Transaction"):
            if "Deposit" in action_type:
                new_bal = curr_balance + amount
                earned, spent = amount, 0
            else:
                new_bal = curr_balance - amount
                earned, spent = 0, amount
                
            st.session_state["balances_df"].loc[st.session_state["balances_df"]['Account'] == acc_no, 'Balance'] = new_bal
            
            new_tx = pd.DataFrame([{
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Account": acc_no,
                "Name": student_info['name'],
                "Particulars": reason,
                "Earned": earned,
                "Spent": spent,
                "Balance": new_bal
            }])
            
            st.session_state["tx_df"] = pd.concat([st.session_state["tx_df"], new_tx], ignore_index=True)
            
            try:
                from streamlit_gsheets import GSheetsConnection
                conn = st.connection("gsheets", type=GSheetsConnection)
                SPREADSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
                conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Balances", data=st.session_state["balances_df"])
                conn.update(spreadsheet=SPREADSHEET_URL, worksheet="Transactions", data=st.session_state["tx_df"])
                st.success(f"🎉 Recorded & Synced to Google Sheets! New Balance for {student_info['name']}: {new_bal} Merits.")
            except Exception:
                st.success(f"🎉 Recorded! New Balance for {student_info['name']}: {new_bal} Merits.")
                
            st.rerun()
            
    elif pin != "":
        st.error("Incorrect PIN Code.")
