import vk
import pandas as pd
import time
import numpy as np

data = pd.read_csv('data/user_data.csv', dtype=({'Name': 'str', 'id': 'int'}))
user_names, user_ids = data.Name.values, data.id.values

with open('token.txt', 'r') as f:
    access_token = f.readline().strip()

session = vk.AuthSession(access_token=access_token)
vk_api = vk.API(session, v='5.87')
adj_matrix = np.zeros(shape=(len(user_names), len(user_names)))
all_friends_id = []
for i, row in data.iterrows():
    friend_list = vk_api.friends.get(user_id=row[1])['items']
    all_friends_id.append(friend_list)
    time.sleep(0.3)
all_friends_id = [item for sublist in all_friends_id for item in sublist]
unique_ids = np.unique(np.array(all_friends_id))

row_col_ids = np.arange(unique_ids.shape[0])
id_to_idx = dict(zip(unique_ids, row_col_ids))

matrix = np.zeros((unique_ids.shape[0], unique_ids.shape[0]))
names = []
for user_id, user_ix in id_to_idx.items():
    name = vk_api.users.get(user_id=user_id, fields = 'name')[0]
    name = name['first_name'] + " " + name['last_name']
    names.append(name)
    try:
        friends_of_user = vk_api.friends.get(user_id=user_id)['items']
        user_friends_id = (np.intersect1d(unique_ids, friends_of_user))
        for friend_id in user_friends_id:
            friend_idx = id_to_idx[friend_id]
            matrix[friend_idx][user_ix] = 1
            matrix[user_ix][friend_idx] = 1
    time.sleep(0.5)

pd.DataFrame(matrix, columns=names, index=names).to_csv('data/matrix.csv', index_label='Name')