import os
import sys

# Ensure project root is importable when Streamlit runs this script directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from graph.workflow import graph

st.set_page_config(
    page_title="Eugene AgentCore POC",
    page_icon="🧠",
    layout="wide"
)

st.title(
    "🧠 Eugene AgentCore + LangGraph POC"
)

st.markdown(
    """
This POC demonstrates:

- Supervisor Agent
- LangGraph Workflow
- Foundation Agent
- Graph Agent
- Publication Agent
- MCP Gateway
- Research Report Generation
"""
)

# query = st.text_area(
#     "Enter Research Question",
#     height=120,
#     value="Find emerging KRAS inhibitors and supporting evidence"
# )

query = st.text_input("Enter Research Query")

if st.button("Run Research"):

    state = {

        "query": query,
       "intent": "",
        "selected_agents": [],
        "foundation_result": {},
        "graph_result": {},
        "publication_result": {},
        "final_report": ""
    }

    with st.spinner(
        "Supervisor analyzing request..."
    ):

        result = graph.invoke(state)

    st.success(
        "Research Completed"
    )

    st.subheader(
        "Supervisor Decision"
    )

    st.json(
        result["selected_agents"]
    )
    st.subheader(
        "Long-Term Memory"
        )
    
    st.json(
        result.get("long_term_memory",{})
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.subheader(
            "Foundation Agent"
        )

        st.json(
            result["foundation_result"]
        )

    with col2:

        st.subheader(
            "Graph Agent"
        )

        st.json(
            result["graph_result"]
        )

    with col3:

        st.subheader(
            "Publication Agent"
        )

        st.json(
            result["publication_result"]
        )

    with col4:
    
            st.subheader(
                "Graph Analytics"
                )
                
            st.json(
                result.get(
                "graph_analytics",{})
                )

    st.subheader(
        "Final Research Report"
    )

    st.markdown(
        result["final_report"]
    )