import streamlit as st
import pandas as pd

def export_csv(df, filename, label="📥 Télécharger CSV"):
    """Exporte un DataFrame en CSV et propose le téléchargement"""
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label=label, data=csv, file_name=filename, mime='text/csv')

def kpi_card(label, value, icon="📊", color="#2563EB", bg="#EFF6FF"):
    """Retourne une carte HTML pour les KPIs"""
    return f"""
    <div style="background:{bg};border:1px solid {color}22;border-radius:12px;
                padding:16px 18px;text-align:center;">
      <div style="font-size:1.4rem;margin-bottom:4px;">{icon}</div>
      <div style="font-size:1.5rem;font-weight:700;color:{color};line-height:1.1;">{value}</div>
      <div style="font-size:0.72rem;font-weight:600;color:#64748B;text-transform:uppercase;
                  letter-spacing:0.05em;margin-top:4px;">{label}</div>
    </div>
    """

def status_banner(label, detail, color):
    """Affiche une bannière de statut colorée"""
    st.markdown(
        f'<div style="background:{color}12;border-left:4px solid {color};'
        f'border-radius:8px;padding:12px 16px;margin:8px 0;">'
        f'<b style="color:{color};">{label}</b>'
        f'<span style="color:#475569;margin-left:10px;font-size:0.875rem;">{detail}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )

def section_header(title, icon=""):
    """Affiche un en-tête de section stylisé"""
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;margin:24px 0 10px 0;">'
        f'<span style="font-size:1.1rem;">{icon}</span>'
        f'<span style="font-size:1rem;font-weight:700;color:#0F172A;">{title}</span>'
        f"</div>",
        unsafe_allow_html=True,
    )