from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


class PopularityRecommender:
    '''Recommend the most popular products items regardless of user purchase history.'''
    
    def __init__(self):
        self.MODEL_NAME = 'Popularity'
        
    def fit(self, train_interactions):
        self.pop = pd.DataFrame(train_interactions.groupby('itemid').strength.sum()).sort_values('strength', ascending=False).reset_index()
        self.user_interactions = train_interactions.groupby('userid').itemid.agg(set)

    def get_model_name(self):
        return self.MODEL_NAME
    
    def recommend_items(self, userid):
        userid = str(userid)
        return self.pop['itemid'].tolist()
    
    def _get_interacted_items(self, userid):
        userid = str(userid)
        return self.user_interactions.get(userid, {})


class CFRecommenderKNN:
    '''Item-item nearest neighbors collaborative filtering.'''
    
    def __init__(self, k_neighbors=5):
        self.MODEL_NAME = 'KNN collaborative filtering'
        self.k = k_neighbors
        self.pop_model = PopularityRecommender()
        
    def fit(self, train_interactions):
        self.pop_model.fit(train_interactions)
        self.user_interactions = train_interactions.groupby('userid').itemid.agg(set)
        self.utility_matrix = train_interactions.groupby(['userid','itemid']).strength.sum().reset_index()\
                                                .pivot(index='itemid', columns='userid', values='strength').fillna(0)

        # take similarity of itemids, since rows=itemids
        self.similarity_matrix = pd.DataFrame(cosine_similarity(self.utility_matrix.values), 
                                                index=self.utility_matrix.index, 
                                                columns=self.utility_matrix.index,)
        
    def recommend_items(self, userid):
        userid = str(userid)
        if userid not in self.utility_matrix.columns:
            return self.pop_model.recommend_items(userid)
                
        ranking = self.utility_matrix[userid]
        for product in ranking.index:
            sim = self.similarity_matrix[product].iloc[np.argpartition(-self.similarity_matrix[product].values, self.k)[:self.k]]
            if sum(sim.values) == 0:
                ranking.loc[product] = 0
            else:
                ranking.loc[product] = np.dot(0.01 + self.utility_matrix[userid].loc[list(sim.index)].values, sim.values) / sum(sim.values)
        
        return ranking.sort_values(ascending=False).index.tolist()
        

    def _get_interacted_items(self, userid):
        userid = str(userid)
        return self.user_interactions.get(userid, {})
    
    def get_model_name(self):
        return self.MODEL_NAME