PK     ê³ZE«]Kº  º     streamlit_app.pyimport streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="DCF Calculator", layout="wide")
st.title("ð Discounted Cash Flow (DCF) Calculator with Forecasting")

# Sidebar
with st.sidebar:
    st.header("ð§ Settings")
    discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, max_value=100.0, value=8.0)
    enable_forecast = st.checkbox("Enable Forecasting", value=False)

    if enable_forecast:
        forecast_years = st.slider("Forecast Years", 1, 10, 5)
        growth_rate = st.number_input("Annual Growth Rate (%)", value=5.0)

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    required_columns = {"Date", "Cash Flow"}
    if not required_columns.issubset(df.columns):
        st.error(f"File must contain columns: {required_columns}")
    else:
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        start_date = df["Date"].iloc[0]
        df["Years"] = (df["Date"] - start_date).dt.days / 365.25

        if enable_forecast:
            last_row = df.iloc[-1]
            current_date = last_row["Date"]
            current_cash_flow = last_row["Cash Flow"]
            forecast_rows = []
            for year in range(1, forecast_years + 1):
                future_date = current_date + pd.DateOffset(years=year)
                future_cf = current_cash_flow * ((1 + growth_rate / 100) ** year)
                forecast_rows.append({"Date": future_date, "Cash Flow": future_cf})
            df_forecast = pd.DataFrame(forecast_rows)
            df = pd.concat([df, df_forecast], ignore_index=True)
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")
            df["Years"] = (df["Date"] - start_date).dt.days / 365.25

        r = discount_rate / 100
        df["Present Value"] = df["Cash Flow"] / ((1 + r) ** df["Years"])
        npv = df["Present Value"].sum()

        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("ð Discounted Cash Flows Table")
            st.dataframe(df[["Date", "Cash Flow", "Years", "Present Value"]].round(2), use_container_width=True)
        with col2:
            st.metric("ð Net Present Value (NPV)", f"${npv:,.2f}")

        st.markdown("---")
        st.subheader("ð Cash Flow vs Present Value Over Time")
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Cash Flow"], label="Cash Flow", marker="o")
        ax.plot(df["Date"], df["Present Value"], label="Present Value", marker="o")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Cash Flow Projection")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        def create_pdf_with_chart(df, npv, discount_rate, chart_fig):
            chart_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            chart_fig.savefig(chart_file.name, dpi=300, bbox_inches='tight')
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Discounted Cash Flow (DCF) Report", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Discount Rate: {discount_rate:.2f}%", ln=True)
            pdf.cell(200, 10, txt=f"Net Present Value (NPV): ${npv:,.2f}", ln=True)
            pdf.ln(10)
            pdf.image(chart_file.name, x=10, w=pdf.w - 20)
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(50, 10, "Date", border=1)
            pdf.cell(40, 10, "Cash Flow", border=1)
            pdf.cell(30, 10, "Years", border=1)
            pdf.cell(50, 10, "Present Value", border=1)
            pdf.ln()
            pdf.set_font("Arial", '', 10)
            for _, row in df.iterrows():
                pdf.cell(50, 10, row['Date'].strftime('%Y-%m-%d'), border=1)
                pdf.cell(40, 10, f"${row['Cash Flow']:,.2f}", border=1)
                pdf.cell(30, 10, f"{row['Years']:.2f}", border=1)
                pdf.cell(50, 10, f"${row['Present Value']:,.2f}", border=1)
                pdf.ln()
            pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(pdf_file.name)
            os.remove(chart_file.name)
            return pdf_file.name

        pdf_file = create_pdf_with_chart(df, npv, discount_rate, fig)
        with open(pdf_file, "rb") as file:
            st.download_button(
                label="ð Download Full DCF Report (PDF with Chart)",
                data=file,
                file_name="DCF_Report_With_Chart.pdf",
                mime="application/pdf"
            )
        os.remove(pdf_file)
PK     ê³Zñpã*   *      requirements.txtstreamlit
pandas
matplotlib
fpdf
openpyxl
PK     ê³Zóè    	   README.md# ð¸ Discounted Cash Flow (DCF) Streamlit App

Upload your cash flow spreadsheet, choose your discount rate, and get the Net Present Value (NPV) instantly â with optional forecasting and a downloadable PDF report.

### ð¦ Features:
- Upload Excel or CSV file
- Forecast future cash flows with growth rate
- Visualize data (chart + table)
- Export results to PDF

Built with Streamlit, Matplotlib, and FPDF.
PK     ê³ZE«]Kº  º             ¤    streamlit_app.pyPK     ê³Zñpã*   *              ¤è  requirements.txtPK     ê³Zóè    	           ¤@  README.mdPK      ³       