import pickle
with open('./macro.pkl','rb')as f:
    data = pickle.load(f)

print(data)