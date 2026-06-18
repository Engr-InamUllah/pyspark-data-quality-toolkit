from pyspark.sql import DataFrame, functions as F
class QualityError(Exception):pass

def profile(df:DataFrame)->dict:
 count=df.count()
 return {"rows":count,"columns":len(df.columns),"nulls":{c:df.filter(F.col(c).isNull()).count() for c in df.columns}}
def assert_unique(df:DataFrame,column:str)->DataFrame:
 duplicates=df.groupBy(column).count().filter("count > 1")
 if duplicates.limit(1).count():raise QualityError(f"duplicate {column}")
 return df
def assert_range(df:DataFrame,column:str,minimum:float,maximum:float)->DataFrame:
 if df.filter(~F.col(column).between(minimum,maximum)).limit(1).count():raise QualityError(f"{column} outside range")
 return df