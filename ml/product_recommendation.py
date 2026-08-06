"""
Product Recommendation Engine - Step 5
Builds a product co-occurrence & item similarity recommendation engine
to suggest cross-sell products based on customer purchase history.
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def build_product_recommendation_engine(clean_data_path=config.CLEAN_DATASET_PATH):
    """
    Builds a customer-product matrix, computes item-item cosine similarity,
    and returns top-N recommended products for any given product or customer profile.
    """
    print("\n" + "=" * 60)
    print("[ML] MODULE D: PRODUCT RECOMMENDATION ENGINE")
    print("=" * 60)

    # 1. Load Clean Dataset
    df = pd.read_csv(clean_data_path)

    # 2. Build Customer-Product Binary Matrix (1 if purchased, 0 otherwise)
    basket_matrix = df.groupby(["Customer ID", "Product"])["Quantity"].sum().unstack().fillna(0)
    basket_binary = (basket_matrix > 0).astype(int)

    # 3. Compute Item-Item Cosine Similarity Matrix
    item_similarity = cosine_similarity(basket_binary.T)
    similarity_df = pd.DataFrame(item_similarity, index=basket_binary.columns, columns=basket_binary.columns)

    print(f"[INFO] Constructed Item Similarity Matrix ({similarity_df.shape[0]} Products x {similarity_df.shape[1]} Products)")

    # 4. Recommendation Lookup Function
    def get_top_recommendations(product_name, top_n=3):
        if product_name not in similarity_df.index:
            return []
        scores = similarity_df[product_name].sort_values(ascending=False)
        # Exclude self-similarity
        recommendations = scores.iloc[1:top_n+1].index.tolist()
        return recommendations

    # Example Demonstrations
    sample_products = ["MacBook Pro 16-inch", "Ergonomic Mesh Office Chair", "Thermal Label Printer"]
    print("\n[RECOMMENDATION SAMPLE DEMOS]")
    recommendation_results = {}
    for p_sample in sample_products:
        recs = get_top_recommendations(p_sample, top_n=3)
        recommendation_results[p_sample] = recs
        print(f"  • If customer bought '{p_sample}':")
        for rank, rec_prod in enumerate(recs, 1):
            print(f"      -> Recommended #{rank}: {rec_prod}")

    # 5. Save Model Artifact
    config.ensure_directories_exist()
    model_path = config.ML_MODELS_DIR / "recommender.joblib"
    joblib.dump({
        "similarity_matrix": similarity_df,
        "sample_recommendations": recommendation_results
    }, model_path)
    print(f"\n[OK] Saved recommendation engine artifact to: {model_path}")

    return {
        "similarity_df": similarity_df,
        "sample_recommendations": recommendation_results
    }

if __name__ == "__main__":
    build_product_recommendation_engine()
