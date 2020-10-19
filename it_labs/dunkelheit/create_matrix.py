import vk
import pandas as pd
import time
import numpy as np
from vk.exceptions import VkAPIError
import tqdm


TOKEN_PATH = "token.txt"
DATA_PATH = "user_data.csv"
MATRIX_NAME = "matrix.csv"

data = pd.read_csv('data/'+DATA_PATH, dtype=({'Name': 'str', 'id': 'int'}))
user_names, user_ids = data.Name.values, data.id.values

with open(TOKEN_PATH, 'r') as f:
    access_token = f.readline().strip()

session = vk.AuthSession(access_token=access_token)
vk_api = vk.API(session, v='5.87')

all_friends_id = []
for i, row in data.iterrows():
    try:
        friend_list = vk_api.friends.get(user_id=row[1])['items']
        all_friends_id.append(friend_list)
        time.sleep(0.5)
    except VkAPIError:
        continue
        
all_friends_id = [item for sublist in all_friends_id for item in sublist]
unique_ids = np.unique(np.array(all_friends_id))

row_col_ids = np.arange(unique_ids.shape[0])
id_to_idx = dict(zip(unique_ids, row_col_ids))
matrix = np.zeros((unique_ids.shape[0], unique_ids.shape[0]))
names = []

for user_id, user_ix in tqdm.tqdm(id_to_idx.items()):
    try:
        name = vk_api.users.get(user_id=user_id, fields = 'name')[0]
        name = name['first_name'] + " " + name['last_name']
        time.sleep(0.51)
        friends_of_user = vk_api.friends.get(user_id=user_id)['items']
        user_friends_id = (np.intersect1d(unique_ids, friends_of_user))
        names.append(name)
        for friend_id in user_friends_id:
            friend_idx = id_to_idx[friend_id]
            matrix[friend_idx][user_ix] = 1
            matrix[user_ix][friend_idx] = 1
    except VkAPIError:
        names.append(user_id)
        continue

pd.DataFrame(matrix, columns=names, index=names).to_csv('data/'+MATRIX_NAME, index_label='Name')
