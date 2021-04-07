import json, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
import modules.pandas as pd
import modules.requests as requests

def reader(url):
    #DIRECTLY PULL DATA FROM GITHUB WITH REQUESTS    
    resp = requests.get(url).text
    
    #WRITE TO CSV FILE   
    with open("github.csv", "w") as f: f.write(resp)

    #READ DATA DIRECTLY INTO DATAFRAME
    df = pd.read_csv("github.csv")
    print(f"\nThe length of the dataframe is {len(df)} rows")
    return df

def cleaner(df):
    #CLEAN OUT NON-NUMERIC DATA   
    df = df[pd.to_numeric(df['Profit (in millions)'], errors='coerce').notnull()]
    print(f"\nThere are {len(df)} rows left after cleaning")

    #SORT CLEAN LIST IN DESCENDING ORDER
    top_profit = df.sort_values(by="Profit (in millions)", ascending=False)

    #PRINT TOP 20 PROFIT VALUES FROM SORTED LIST
    print("\n\nThe Top Profits are: \n"); print(top_profit[:20])
    return df

def convert_json(df):
    #CONVERT TO JSON    
    json_df = json.loads(df.to_json(orient="table"))

    #OUTPUT JSON FILE   
    with open("data2.json", "w") as fp: json.dump(json_df, fp=fp, indent=3)

    #FILE LOCATION    
    flocation = os.getcwd()+'\\data2.json'
    print("\n\nCompleted!\n"); print(f"Output is in file ==> 'data2.json'\nCheck this location:\n{flocation}")

def handler(git_url):
    df = reader(git_url)
    df = cleaner(df)
    convert_json(df)

if __name__ == "__main__":
    print("\n\n\n--------------------")
    print("START CODE")
    print("--------------------\n")

    try: url = sys.argv[1]
    except: print("You need to pass the URL of the csv file!")
    handler(url)
    print("\n\n\n--------------------")
    print("END")
    print("--------------------\n\n\n")
