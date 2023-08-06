from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


class PopularityRecommender:
    '''Recommend the most popular products items regardless of user purchase history.'''
    
    def __init__(self):
        self.MODEL_NAME = 'Popularity'
        
    def fit(self, train_interactions):
        self.pop = pd.DataFrame(train_interactions.groupby('productid').qty.sum()).sort_values('qty', ascending=False).reset_index()
        self.user_interactions = train_interactions.groupby('loyalty').productid.agg(set)

    def get_model_name(self):
        return self.MODEL_NAME
    
    def recommend_items(self, loyalty):
        loyalty = str(loyalty)
        return self.pop['productid'].tolist()
    
    def _get_interacted_items(self, loyalty):
        loyalty = str(loyalty)
        return self.user_interactions.get(loyalty, {})


class CFRecommenderKNN:
    '''Item-item nearest neighbors collaborative filtering.'''
    
    def __init__(self, k_neighbors=5):
        self.MODEL_NAME = 'KNN collaborative filtering'
        self.k = k_neighbors
        self.pop_model = PopularityRecommender()
        
    def fit(self, train_interactions):
        self.pop_model.fit(train_interactions)
        train_interactions.qty = np.log2(1 + train_interactions.qty)
        self.user_interactions = train_interactions.groupby('loyalty').productid.agg(set)
        self.utility_matrix = train_interactions.groupby(['loyalty','productid']).qty.sum().reset_index()\
                                                .pivot(index='productid', columns='loyalty', values='qty').fillna(0)

        # take similarity of productids, since rows=productids
        self.similarity_matrix = pd.DataFrame(cosine_similarity(self.utility_matrix.values), 
                                                index=self.utility_matrix.index, 
                                                columns=self.utility_matrix.index,)
        
    def recommend_items(self, loyalty):
        loyalty = str(loyalty)
        if loyalty not in self.utility_matrix.columns:
            return self.pop_model.recommend_items(loyalty)
                
        ranking = self.utility_matrix[loyalty]
        for product in ranking.index:
            sim = self.similarity_matrix[product].iloc[np.argpartition(-self.similarity_matrix[product].values, self.k)[:self.k]]
            if sum(sim.values) == 0:
                ranking.loc[product] = 0
            else:
                ranking.loc[product] = np.dot(0.01 + self.utility_matrix[loyalty].loc[list(sim.index)].values, sim.values) / sum(sim.values)
        
        return ranking.sort_values(ascending=False).index.tolist()
        

    def _get_interacted_items(self, loyalty):
        loyalty = str(loyalty)
        return self.user_interactions.get(loyalty, {})
    
    def get_model_name(self):
        return self.MODEL_NAME
