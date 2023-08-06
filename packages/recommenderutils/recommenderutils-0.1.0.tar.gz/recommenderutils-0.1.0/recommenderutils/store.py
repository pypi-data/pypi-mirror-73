import numpy as np
import pandas as pd
from .models import CFRecommenderKNN, PopularityRecommender


class DashboardRecommender:
    def __init__(self, storemaps):
        self.MODEL_NAME = 'Dashboard Recommender'
        self.storemaps = storemaps
        self.model = CFRecommenderKNN()

    def fit(self, train_interactions):
        self.model.fit(train_interactions)
    
    def recommend_items(self, loyalty, waiterproid):
        recommendations  = self.model.recommend_items(loyalty)
        return [item for item in recommendations if item in self.storemaps[waiterproid]]


class ProductRecommender:
    def __init__(self, franchiseinv, storeinvs):
        self.MODEL_NAME = 'Product Recommender'