import streamlit as st
from openai import OpenAI
import pandas as pd

st.set_page_config(
    page_title="Problem Analysis Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Problem Analysis Assistant")

# Sidebar
st.sidebar.header("Configuration")

api_key = st.sidebar.text_input(
    "Enter OpenAI API Key",
    type="password"
)

# Session state
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Problem Statement",
        "Insights",
        "Variables",
        "Supporting Documents"
    ]
)

# -------------------------
# TAB 1: Problem Statement
# -------------------------
with tab1:

    st.header("Problem Definition")

    problem_statement = st.text_area(
        "Enter Problem Statement",
        height=200,
        placeholder="""
Example:
PS lead generations are not happening in selected villages despite repeated rounds of community meetings by Goat Mobilisers and Field Executives.
"""
    )

    analyze_btn = st.button("Analyze Problem")

    if analyze_btn:

        if not api_key:
            st.error("Please enter your OpenAI API key.")
        elif not problem_statement:
            st.error("Please enter a problem statement.")
        else:

            try:

                client = OpenAI(api_key=api_key)

                prompt = f"""
You are an expert program designer and researcher.

Analyze the following problem statement.

Problem Statement:
{problem_statement}

Provide output in the following format:

## Major Insights
- Insight 1
- Insight 2
- Insight 3
- Insight 4
- Insight 5

## Dependent Variables
- Variable
- Variable

## Independent Variables
- Variable
- Variable

## Possible Hypotheses
- Hypothesis 1
- Hypothesis 2
- Hypothesis 3
"""

                response = client.responses.create(
                    model="gpt-5",
                    input=prompt
                )

                result = response.output_text

                st.session_state.analysis = result

                st.success("Analysis completed.")

            except Exception as e:
                st.error(f"Error: {e}")

# -------------------------
# TAB 2: Insights
# -------------------------
with tab2:

    st.header("Major Insights")

    if st.session_state.analysis:
        st.markdown(st.session_state.analysis)
    else:
        st.info("Run analysis from the Problem Statement tab.")

# -------------------------
# TAB 3: Variables
# -------------------------
with tab3:

    st.header("Dependent & Independent Variables")

    if st.session_state.analysis:
        st.markdown(st.session_state.analysis)
    else:
        st.info("Run analysis first.")

# -------------------------
# TAB 4: Supporting Docs
# -------------------------
with tab4:

    st.header("Upload Supporting Documents")

    uploaded_files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=[
            "pdf",
            "docx",
            "txt",
            "csv",
            "xlsx"
        ]
    )

    if uploaded_files:

        file_data = []

        for file in uploaded_files:

            file_data.append({
                "File Name": file.name,
                "Size (KB)": round(file.size / 1024, 2),
                "Type": file.type
            })

        df = pd.DataFrame(file_data)

        st.success(
            f"{len(uploaded_files)} file(s) uploaded."
        )

        st.dataframe(
            df,
            use_container_width=True
        )