import streamlit as st

DARK_NAVY_CSS = """
<style>
    /* Dark Navy Intelligence Theme */
    .stApp {
        background-color: #0b0f19;
        color: #cbd5e1;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    
    p, span, div, label {
        color: #cbd5e1;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #070a12;
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] * {
        color: #94a3b8;
    }

    .sidebar-brand {
        font-size: 1.3rem;
        font-weight: 800;
        color: #38bdf8 !important;
        letter-spacing: 0.08em;
        margin-bottom: 2px;
    }

    .sidebar-subbrand {
        font-size: 0.75rem;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 1.2rem;
        line-height: 1.3;
    }
    
    .sidebar-meta-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b !important;
        margin-top: 0.8rem;
    }

    .sidebar-meta-value {
        font-size: 0.85rem;
        font-weight: 600;
        color: #e2e8f0 !important;
        font-family: monospace;
    }
    
    /* Custom Card Styling */
    .helios-card {
        background-color: #131c2e;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    .helios-metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 0.3rem;
    }
    
    .helios-metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #f8fafc;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }

    .helios-metric-subtext {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }
    
    /* Status Badges */
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: inline-block;
    }

    .badge-high {
        background-color: rgba(245, 158, 11, 0.15);
        color: #fbbf24 !important;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: inline-block;
    }
    
    .badge-ready {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399 !important;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: inline-block;
    }

    .badge-info {
        background-color: rgba(56, 189, 248, 0.15);
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Structured Evidence Table Card */
    .evidence-card {
        background-color: #0f172a;
        border-left: 3px solid #38bdf8;
        border-top: 1px solid #1e293b;
        border-right: 1px solid #1e293b;
        border-bottom: 1px solid #1e293b;
        border-radius: 4px;
        padding: 0.9rem;
        margin-bottom: 0.75rem;
    }

    .evidence-feature {
        font-weight: 700;
        color: #38bdf8;
        font-size: 0.95rem;
    }

    .evidence-observed {
        font-family: monospace;
        font-weight: 600;
        color: #f8fafc;
    }

    /* Override dataframe table header/row styling */
    [data-testid="stDataFrame"] {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 6px;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }

    hr {
        border-color: #1e293b !important;
    }
</style>
"""

def apply_theme():
    st.markdown(DARK_NAVY_CSS, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">TxAnomaly</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-subbrand">SIH26146<br>Investigation Intelligence Platform</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown('<div class="sidebar-meta-label">Environment</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top: 4px;"><span class="badge-high">CONTROLLED VALIDATION</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-meta-label">Pipeline</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top: 4px;"><span class="badge-ready">READY</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-meta-label">Dataset</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-meta-value">3393 records</div>', unsafe_allow_html=True)
        st.markdown("---")
