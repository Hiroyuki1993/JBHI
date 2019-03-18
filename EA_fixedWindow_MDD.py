import pandas as pd
from datetime import datetime
import re, os, glob

def calc_awake_period(EMA_records):
    data = EMA_records[(EMA_records.schedule == 2) | (EMA_records.schedule == 1)]
    awake_time = []
    sleep_time = []
    state = 0
    for key, row in data.iterrows():
        if ((state == 0) and (row.schedule == 2)):
            awake_time.append(row.time)
            state = 1
        if ((state == 1) and (row.schedule == 1)):
            sleep_time.append(row.time)
            state = 0
        if ((state == 1) and (row.schedule == 2)):
            awake_time.pop()
            awake_time.append(row.time)
    if (len(awake_time) > len(sleep_time)):
        awake_time.pop()
    period_awake = pd.DataFrame({"awake": pd.to_datetime(awake_time), "sleep": pd.to_datetime(sleep_time)})
    return period_awake

def extractActivities(activity, period_awake, ID, window_min):
    act_list = []
    for key, row in period_awake.iterrows():
        start_time = row.awake
        while start_time < (row.sleep - pd.Timedelta(minutes = window_min)):
            end_time = start_time + pd.Timedelta(minutes = window_min -1) 
            act_extracted = activity[start_time:end_time].Activity
            act_extracted = act_extracted[act_extracted.notnull()].astype(int).astype(str)
            start_time = end_time
            if (len(act_extracted) < window_min):
                # print("length is not enough")
                continue
            act_string = " ".join(act_extracted)
            if(re.search(" 0 0 0 0 0", act_string)):
                # print("too many zero sequences")
                continue
            act_list.append(act_string)
    return pd.DataFrame({"ID": ID, "activities": act_list})

def main():
    window_min = 60

    participants = pd.read_csv('./MDD_data/EMA_data_all participants.csv')
    df_list = []

    activity_files = glob.glob("./MDD_data/Activity_Data/*.csv")
    for fname in activity_files:
        print(fname)
        ID = int(re.sub(r'\D', '', fname))
        participant = participants[participants.ID == ID].copy()
        activity = pd.read_csv(fname, index_col=0, parse_dates=True).sort_index()
        period_awake = calc_awake_period(participant)
        extracted_activities = extractActivities(activity, period_awake, ID, window_min)
        df_list.append(extracted_activities)
    result_df = pd.concat(df_list)
    result_df.to_csv("results/March 2019/MDD_{}min.csv".format(window_min), index=False)

if __name__ == "__main__":
    main()