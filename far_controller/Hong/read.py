import pickle
with open('./tmp/macro.pkl','rb')as f:
    data = pickle.load(f)

print(data)