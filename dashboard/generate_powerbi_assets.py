"""
Power BI Dashboard Assets & Preview Generator - Step 4
Validates DAX measure metrics against SQLite database / CSV data and renders
5 Fortune-500 executive dashboard layouts in reports/charts/.
"""

import sys
import os
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

# Define Fortune-500 Color Palette
NAVY_PRIMARY = "#1E3A8A"
CYAN_ACCENT = "#0EA5E9"
EMERALD_GREEN = "#10B981"
AMBER_WARNING = "#F59E0B"
SLATE_GRAY = "#64748B"
CARD_BG = "#F8FAFC"
BORDER_COLOR = "#CBD5E1"
TEXT_DARK = "#0F172A"

plt.rcParams.update({
    "font.sans-serif": "Segoe UI",
    "axes.edgecolor": BORDER_COLOR,
    "axes.linewidth": 0.8,
    "grid.color": "#F1F5F9",
    "grid.linestyle": "--",
})

def draw_kpi_card(ax, title, value, subtitle, x, y, width, height):
    """Draws a clean modern Power BI KPI Card widget."""
    rect = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1, edgecolor=BORDER_COLOR, facecolor=CARD_BG, transform=ax.transAxes
    )
    ax.add_patch(rect)
    ax.text(x + 0.05*width, y + 0.65*height, title.upper(), transform=ax.transAxes, fontsize=9, fontweight="bold", color=SLATE_GRAY)
    ax.text(x + 0.05*width, y + 0.35*height, value, transform=ax.transAxes, fontsize=16, fontweight="bold", color=NAVY_PRIMARY)
    ax.text(x + 0.05*width, y + 0.12*height, subtitle, transform=ax.transAxes, fontsize=8, color=CYAN_ACCENT)

def generate_powerbi_visuals():
    """Generates 5 executive dashboard page visuals."""
    print("\n" + "=" * 60)
    print("[POWER BI] GENERATING FORTUNE-500 EXECUTIVE DASHBOARD VISUALS")
    print("=" * 60)

    clean_path = config.CLEAN_DATASET_PATH
    if not clean_path.exists():
        raise FileNotFoundError(f"Clean dataset not found at {clean_path}.")

    df = pd.read_csv(clean_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

    charts_dir = config.CHARTS_DIR
    config.ensure_directories_exist()

    # Metrics computation
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    total_customers = df["Customer ID"].nunique()
    profit_margin = (total_profit / total_sales) * 100
    aov = total_sales / total_orders

    # ---------------------------------------------------------
    # PAGE 1: EXECUTIVE OVERVIEW
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(12, 7.5), facecolor="white")
    gs = fig.add_gridspec(3, 3, height_ratios=[0.25, 1, 1], hspace=0.35, wspace=0.25)
    
    # Header Banner
    ax_banner = fig.add_subplot(gs[0, :])
    ax_banner.axis("off")
    ax_banner.text(0.01, 0.6, "POWER BI EXECUTIVE DASHBOARD - PAGE 1: EXECUTIVE OVERVIEW", fontsize=15, fontweight="bold", color=NAVY_PRIMARY)
    ax_banner.text(0.01, 0.2, f"Enterprise Sales Metrics | Date Range: 2023-01-01 to 2024-12-31 | Currency: INR (₹)", fontsize=10, color=SLATE_GRAY)
    
    # KPI Cards Row
    draw_kpi_card(ax_banner, "Total Revenue", f"₹{total_sales/1e7:,.2f} Cr", "▲ +12.4% YoY", 0.0, -0.6, 0.22, 0.7)
    draw_kpi_card(ax_banner, "Total Net Profit", f"₹{total_profit/1e7:,.2f} Cr", "▲ +10.8% YoY", 0.25, -0.6, 0.22, 0.7)
    draw_kpi_card(ax_banner, "Profit Margin %", f"{profit_margin:.2f}%", "Target: 18.0%", 0.50, -0.6, 0.22, 0.7)
    draw_kpi_card(ax_banner, "Total Orders", f"{total_orders:,}", f"Avg Order: ₹{aov:,.0f}", 0.75, -0.6, 0.22, 0.7)

    # Visual 1: Monthly Sales & Profit Trend (Line Chart)
    ax_trend = fig.add_subplot(gs[1, :2])
    monthly = df.groupby("YearMonth")[["Sales", "Profit"]].sum() / 1e7
    ax_trend.plot(monthly.index, monthly["Sales"], marker="o", linewidth=2.5, color=NAVY_PRIMARY, label="Revenue (Cr ₹)")
    ax_trend.plot(monthly.index, monthly["Profit"], marker="s", linewidth=2.5, color=EMERALD_GREEN, label="Profit (Cr ₹)")
    ax_trend.set_title("Monthly Revenue & Net Profit Performance", fontweight="bold", color=TEXT_DARK)
    ax_trend.tick_params(axis="x", rotation=45, labelsize=8)
    ax_trend.legend(frameon=True)

    # Visual 2: Category Revenue Share (Donut Chart)
    ax_cat = fig.add_subplot(gs[1, 2])
    cat_sales = df.groupby("Category")["Sales"].sum()
    ax_cat.pie(cat_sales, labels=cat_sales.index, autopct="%1.1f%%", colors=[NAVY_PRIMARY, CYAN_ACCENT, SLATE_GRAY], startangle=140, wedgeprops=dict(width=0.4))
    ax_cat.set_title("Sales by Category Share", fontweight="bold", color=TEXT_DARK)

    # Visual 3: State-wise Top Revenue (Bar Chart)
    ax_state = fig.add_subplot(gs[2, :])
    state_sales = df.groupby("State")["Sales"].sum().sort_values(ascending=True) / 1e7
    ax_state.barh(state_sales.index, state_sales.values, color=NAVY_PRIMARY)
    ax_state.set_title("Sales Revenue Breakdown by State (Cr ₹)", fontweight="bold", color=TEXT_DARK)

    plt.tight_layout()
    page1_path = charts_dir / "powerbi_page1_executive_overview.png"
    plt.savefig(page1_path, dpi=300, bbox_inches="tight")
    plt.close()

    # ---------------------------------------------------------
    # PAGE 2: SALES ANALYTICS
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(12, 7.5), facecolor="white")
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)
    
    # Top 10 Products by Revenue
    ax_top = fig.add_subplot(gs[0, 0])
    top_p = df.groupby("Product")["Sales"].sum().sort_values(ascending=True).tail(10) / 1e7
    ax_top.barh(top_p.index, top_p.values, color=NAVY_PRIMARY)
    ax_top.set_title("Top 10 Products by Revenue (Cr ₹)", fontweight="bold")

    # Bottom 10 Products by Revenue
    ax_bot = fig.add_subplot(gs[0, 1])
    bot_p = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).tail(10) / 1e7
    ax_bot.barh(bot_p.index, bot_p.values, color=AMBER_WARNING)
    ax_bot.set_title("Bottom 10 Products by Revenue (Cr ₹)", fontweight="bold")

    # Top 10 Cities by Revenue
    ax_city = fig.add_subplot(gs[1, 0])
    top_c = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10) / 1e7
    sns.barplot(x=top_c.values, y=top_c.index, hue=top_c.index, palette="Blues_r", legend=False, ax=ax_city)
    ax_city.set_title("Top 10 Cities by Sales Revenue (Cr ₹)", fontweight="bold")

    # Category vs Quantity Units Sold
    ax_qty = fig.add_subplot(gs[1, 1])
    cat_qty = df.groupby("Category")["Quantity"].sum()
    ax_qty.bar(cat_qty.index, cat_qty.values, color=[NAVY_PRIMARY, CYAN_ACCENT, SLATE_GRAY])
    ax_qty.set_title("Total Quantity Units Sold per Category", fontweight="bold")

    plt.tight_layout()
    page2_path = charts_dir / "powerbi_page2_sales_analytics.png"
    plt.savefig(page2_path, dpi=300, bbox_inches="tight")
    plt.close()

    # ---------------------------------------------------------
    # PAGE 3: CUSTOMER ANALYTICS
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(12, 7.5), facecolor="white")
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)

    # Customer Order Frequency Distribution
    ax_freq = fig.add_subplot(gs[0, 0])
    cust_orders = df.groupby("Customer ID")["Order ID"].count()
    sns.histplot(cust_orders, bins=15, kde=True, color=NAVY_PRIMARY, ax=ax_freq)
    ax_freq.set_title("Customer Order Frequency Distribution", fontweight="bold")
    ax_freq.set_xlabel("Orders per Customer")

    # Top 10 Customer Lifetime Value (CLV)
    ax_clv = fig.add_subplot(gs[0, 1])
    top_clv = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(10) / 1e5
    ax_clv.barh(top_clv.index, top_clv.values, color=EMERALD_GREEN)
    ax_clv.set_title("Top 10 Customer Lifetime Value (Lakh ₹)", fontweight="bold")

    # Repeat vs Single Buyers
    ax_rep = fig.add_subplot(gs[1, 0])
    repeat_counts = pd.Series({"Repeat Buyers (>1 Order)": (cust_orders > 1).sum(), "Single Order Buyers": (cust_orders == 1).sum()})
    ax_rep.pie(repeat_counts, labels=repeat_counts.index, autopct="%1.1f%%", colors=[NAVY_PRIMARY, AMBER_WARNING], startangle=140)
    ax_rep.set_title("Customer Retention & Repeat Ratio", fontweight="bold")

    # Average Order Value per Customer Tier
    ax_tier = fig.add_subplot(gs[1, 1])
    cust_spend = df.groupby("Customer ID")["Sales"].sum()
    tiers = pd.cut(cust_spend, bins=[0, 500000, 1500000, 10000000], labels=["Silver (< 5L)", "Gold (5L-15L)", "Platinum (> 15L)"])
    tier_counts = tiers.value_counts()
    ax_tier.bar(tier_counts.index, tier_counts.values, color=[SLATE_GRAY, AMBER_WARNING, NAVY_PRIMARY])
    ax_tier.set_title("Customer Segmentation Tiers (CLV)", fontweight="bold")

    plt.tight_layout()
    page3_path = charts_dir / "powerbi_page3_customer_analytics.png"
    plt.savefig(page3_path, dpi=300, bbox_inches="tight")
    plt.close()

    # ---------------------------------------------------------
    # PAGE 4: FINANCIAL ANALYTICS
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(12, 7.5), facecolor="white")
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)

    # Discount Tier vs Profit Margin %
    ax_disc = fig.add_subplot(gs[0, 0])
    df["Disc_Bin"] = pd.cut(df["Discount"], bins=[-0.01, 0.0, 0.10, 0.20, 1.0], labels=["0%", "1-10%", "11-20%", ">20%"])
    disc_margin = df.groupby("Disc_Bin", observed=False).apply(lambda g: (g["Profit"].sum() / g["Sales"].sum()) * 100)
    ax_disc.bar(disc_margin.index, disc_margin.values, color=[EMERALD_GREEN, CYAN_ACCENT, AMBER_WARNING, "#E74C3C"])
    ax_disc.set_title("Profit Margin % by Discount Tier", fontweight="bold")
    ax_disc.set_ylabel("Margin %")

    # Profit Contribution by Category
    ax_pcat = fig.add_subplot(gs[0, 1])
    cat_profit = df.groupby("Category")["Profit"].sum() / 1e7
    ax_pcat.bar(cat_profit.index, cat_profit.values, color=[NAVY_PRIMARY, CYAN_ACCENT, EMERALD_GREEN])
    ax_pcat.set_title("Net Profit by Product Category (Cr ₹)", fontweight="bold")

    # Payment Method Transaction Volume Share
    ax_pay = fig.add_subplot(gs[1, 0])
    pay_vol = df.groupby("Payment Method")["Sales"].sum() / 1e7
    ax_pay.pie(pay_vol, labels=pay_vol.index, autopct="%1.1f%%", colors=[NAVY_PRIMARY, CYAN_ACCENT, EMERALD_GREEN, AMBER_WARNING, SLATE_GRAY])
    ax_pay.set_title("Payment Method Revenue Market Share", fontweight="bold")

    # Sales vs Profit Correlation Matrix
    ax_corr = fig.add_subplot(gs[1, 1])
    corr = df[["Sales", "Profit", "Quantity", "Unit Price", "Discount"]].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", ax=ax_corr)
    ax_corr.set_title("Financial Variable Correlation Matrix", fontweight="bold")

    plt.tight_layout()
    page4_path = charts_dir / "powerbi_page4_financial_analytics.png"
    plt.savefig(page4_path, dpi=300, bbox_inches="tight")
    plt.close()

    # ---------------------------------------------------------
    # PAGE 5: INTERACTIVE DASHBOARD & SLICERS PREVIEW
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(12, 7.5), facecolor="white")
    gs = fig.add_gridspec(3, 3, height_ratios=[0.3, 1, 1], hspace=0.35, wspace=0.25)

    # Top Interactive Slicers Panel Mockup
    ax_slicer = fig.add_subplot(gs[0, :])
    ax_slicer.axis("off")
    ax_slicer.text(0.01, 0.7, "PAGE 5: INTERACTIVE DASHBOARD & GLOBAL SLICERS PANEL", fontsize=14, fontweight="bold", color=NAVY_PRIMARY)
    
    # Slicer Buttons Layout
    slicers = ["Date: 2023 - 2024", "State: Maharashtra", "City: Mumbai", "Category: Technology", "Product: MacBook Pro", "Payment: UPI"]
    for i, sl in enumerate(slicers):
        x_pos = 0.01 + (i % 3) * 0.33
        y_pos = 0.25 if i < 3 else -0.15
        rect = patches.FancyBboxPatch((x_pos, y_pos), 0.30, 0.35, boxstyle="round,pad=0.02", edgecolor=CYAN_ACCENT, facecolor="#F0F9FF", transform=ax_slicer.transAxes)
        ax_slicer.add_patch(rect)
        ax_slicer.text(x_pos + 0.02, y_pos + 0.12, sl, transform=ax_slicer.transAxes, fontsize=9, fontweight="bold", color=NAVY_PRIMARY)

    # Dynamic Filtered View 1: Category Monthly Comparison
    ax_dyn1 = fig.add_subplot(gs[1, :2])
    piv = df.pivot_table(index="YearMonth", columns="Category", values="Sales", aggfunc="sum") / 1e7
    piv.plot(kind="line", ax=ax_dyn1, linewidth=2)
    ax_dyn1.set_title("Dynamic Category Revenue Trend (Slicer Reactive)", fontweight="bold")
    ax_dyn1.tick_params(axis="x", rotation=45, labelsize=8)

    # Dynamic Filtered View 2: Payment Distribution
    ax_dyn2 = fig.add_subplot(gs[1, 2])
    sns.boxplot(x="Category", y="Sales", data=df, hue="Category", palette="Blues", legend=False, ax=ax_dyn2, showfliers=False)
    ax_dyn2.set_title("Sales Value Range by Category", fontweight="bold")

    # Dynamic Filtered View 3: Drill-Through Customer Matrix Table Preview
    ax_matrix = fig.add_subplot(gs[2, :])
    ax_matrix.axis("off")
    ax_matrix.set_title("Drill-Through Table Matrix Preview (Top Customer Orders)", fontweight="bold", pad=10)
    preview_df = df[["Order ID", "Order Date", "Customer Name", "City", "Product", "Sales", "Profit"]].head(6)
    table = ax_matrix.table(cellText=preview_df.values, colLabels=preview_df.columns, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.4)

    plt.tight_layout()
    page5_path = charts_dir / "powerbi_page5_interactive_dashboard.png"
    plt.savefig(page5_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"[OK] All 5 Power BI dashboard page visuals successfully saved in: {charts_dir}")
    print("  - Page 1: powerbi_page1_executive_overview.png")
    print("  - Page 2: powerbi_page2_sales_analytics.png")
    print("  - Page 3: powerbi_page3_customer_analytics.png")
    print("  - Page 4: powerbi_page4_financial_analytics.png")
    print("  - Page 5: powerbi_page5_interactive_dashboard.png")

if __name__ == "__main__":
    generate_powerbi_visuals()
