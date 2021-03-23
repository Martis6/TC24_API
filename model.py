from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle

butai = pd.read_csv("butai_vilnius.csv")
districts = dict(butai.neighborhood.value_counts() > 20)
districts = list(districts.keys())[:sum(list(districts.values()))]
df = butai[~(butai.duplicated(subset = None, keep = 'first'))]
df.loc[~df["neighborhood"].isin(districts), "neighborhood"] = "Other"

df = df.dropna(subset = ["build_material", "heating_type", "condition"])
df["neighborhood"] = df["neighborhood"].astype("category")
df["build_material"] = df["build_material"].astype("category")
df["heating_type"] = df["heating_type"].astype("category")
df["condition"] = df["condition"].astype("category")

cat_columns = df.select_dtypes(['category']).columns
df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

target = df.price
data = df.drop(["price", "price_per_m2"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(data, target)

lreg = LinearRegression()
lreg.fit(X_train, y_train)
predicted = lreg.predict(X_test)
# expected = y_test
# from sklearn.metrics import mean_squared_error, r2_score
# print(f"Mean Squared Error: {mean_squared_error(expected, predicted)}")
# print(f"R2 Score: {r2_score(expected, predicted)}")

with open("lregression.pkl", "wb") as l:
    pickle.dump(lreg, l)
