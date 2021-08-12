import streamlit as st
import pandas as pd
import base64

st.title("Features Extraction Interface")
st.write("Fill the differents items then click on generate")

user_id = st.text_input("User ID")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

BHK_score = st.text_input("BHK Score")

handed = st.selectbox(
'Left handed or Right handed',
('Left Handed', 'Right Handed'))

constraint = st.selectbox("level of constraint",('1','2','3','4','5','6','7','8','9','10'))

finger = st.checkbox("finger")
wrist = st.checkbox("wrist")
elbow = st.checkbox("elbow")
shoulder = st.checkbox("shoulder")

int_val = st.number_input('Frame Resolution', min_value=1, max_value=10, value=5, step=1)


df_BHK = pd.DataFrame()
df_Global = pd.DataFrame()
df_Frames = pd.DataFrame()


df_final = pd.concat([df_BHK, df_Global, df_Frames], axis=0)


csv = df_final.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown('### **⬇️ Download output CSV File **')
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ".csv")'
st.markdown(href, unsafe_allow_html=True)
