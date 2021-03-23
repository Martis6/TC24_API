import pandas as pd
import json


def preprocess(request_data: json) -> pd.DataFrame:
  """Function to preprocess input for prediction."""

  butai = pd.read_csv("butai_vilnius.csv")
  # aggregating uncommon districts
  districts = dict(butai.neighborhood.value_counts() > 20)
  districts = list(districts.keys())[:sum(list(districts.values()))]
  df = butai[~(butai.duplicated(subset = None, keep = 'first'))]
  df.loc[~df["neighborhood"].isin(districts), "neighborhood"] = "Other"
  # preparation for categorical variable recoding
  df["neighborhood"] = df["neighborhood"].astype("category")
  df["build_material"] = df["build_material"].astype("category")
  df["heating_type"] = df["heating_type"].astype("category")
  df["condition"] = df["condition"].astype("category")

  cat_columns = df.select_dtypes(['category']).columns
  df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
  # dictonaries for the recoding
  neighborhood = pd.concat([df.neighborhood, df.neighborhood.cat.codes], axis=1).drop_duplicates()
  neighborhood = neighborhood.set_index("neighborhood")[0].to_dict()
  build_material = pd.concat([df.build_material, df.build_material.cat.codes], axis=1).drop_duplicates()
  build_material = build_material.set_index("build_material")[0].to_dict()
  heating_type = pd.concat([df.heating_type, df.heating_type.cat.codes], axis=1).drop_duplicates()
  heating_type = heating_type.set_index("heating_type")[0].to_dict()
  condition = pd.concat([df.condition, df.condition.cat.codes], axis=1).drop_duplicates()
  condition = condition.set_index("condition")[0].to_dict()
  # preprocessing the input
  res = pd.DataFrame(json.loads(request_data)["input"])
  res.loc[~res["neighborhood"].isin(neighborhood), "neighborhood"] = "Other"
  res["neighborhood"].replace(neighborhood, inplace=True)
  res["build_material"].replace(build_material, inplace=True)
  res["heating_type"].replace(heating_type, inplace=True)
  res["condition"].replace(condition, inplace=True)
  return res