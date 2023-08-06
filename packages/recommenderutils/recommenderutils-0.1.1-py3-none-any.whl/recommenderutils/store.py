import numpy as np
import pandas as pd
from .models import CFRecommenderKNN, PopularityRecommender


class DashboardRecommender:
    '''Recommender using dashboardid as item IDs.
        
    storemaps : dict
        waiterproid (str) -> {set of dashboardid (int)}
    '''
    def __init__(self, storemap):
        self.MODEL_NAME = 'Dashboard Recommender'
        self.storemap = storemap
        self.model = CFRecommenderKNN()

    def fit(self, train_interactions):
        self.model.fit(train_interactions)
    
    def recommend_items(self, loyalty, waiterproid):
        waiterproid = str(waiterproid)
        loyalty = str(loyalty)
        userid = loyalty + waiterproid
        recommendations  = self.model.recommend_items(userid)
        return [item for item in recommendations if item in self.storemap.get(waiterproid, {})]

    def _get_interacted_items(self, loyalty, waiterproid):
        userid = str(loyalty) + str(waiterproid)
        return self.model.user_interactions.get(userid, {})


class ProductRecommender:
    '''Recommender using productid as item IDs.
        
    storeinvs : dict
        waiterproid (str) -> ( name (str) -> productid (int) )
        
    franchiseinv: dict
        fid (int) -> name (str)
    '''
    def __init__(self, franchiseinv, storeinvs):
        self.MODEL_NAME = 'Product Recommender'
        self.franchiseinv = franchiseinv
        self.storeinvs = storeinvs
        self.model = CFRecommenderKNN()

    def fit(self, train_interactions):
        self.model.fit(train_interactions)

    def recommend_items(self, loyalty, waiterproid):
        waiterproid = str(waiterproid)
        loyalty = str(loyalty)
        userid = loyalty + waiterproid
        storeinv = self.storeinvs.get(waiterproid, {})
        recommendations = []
        for franchiseid in self.model.recommend_items(userid):
            name = self.franchiseinv[franchiseid]
            if name in storeinv.keys():
                recommendations.append(storeinv[name])
        return recommendations
    
    def _get_interacted_items(self, loyalty, waiterproid):
        waiterproid = str(waiterproid)
        loyalty = str(loyalty)
        userid = loyalty + waiterproid
        storeinv = self.storeinvs.get(waiterproid, {})
        interactions = []
        for franchiseid in self.model.user_interactions.get(userid, {}):
            name = self.franchiseinv[franchiseid]
            if name in storeinv.keys():
                interactions.append(storeinv[name])
        return set(interactions)