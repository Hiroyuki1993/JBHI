import pandas as pd
from datetime import datetime
import re

def calc_awake_period(EMA_records):
    data = EMA_records[(EMA_records.type_of_record == "awake") | (EMA_records.type_of_record == "sleep")]
    awake_time = []
    sleep_time = []
    state = 0
    for key, row in data.iterrows():
        if ((state == 0) and (row.type_of_record == "awake")):
            awake_time.append(row.time)
            state = 1
        if ((state == 1) and (row.type_of_record == "sleep")):
            sleep_time.append(row.time)
            state = 0
        if ((state == 1) and (row.type_of_record == "awake")):
            awake_time.pop()
            awake_time.append(row.time)
    if (len(awake_time) > len(sleep_time)):
        awake_time.pop()
    period_awake = pd.DataFrame({"awake":pd.to_datetime(awake_time), "sleep": pd.to_datetime(sleep_time)})
    return period_awake

def extractActivities(activity, period_awake, ID, window_min):
    act_list = []
    for key, row in period_awake.iterrows():
        start_time = row.awake
        while start_time < (row.sleep - pd.Timedelta(minutes = window_min)):
            end_time = start_time + pd.Timedelta(minutes = window_min)
            act_extracted = activity[start_time:end_time].activity
            act_extracted = act_extracted[act_extracted.notnull()].astype(int).astype(str)
            start_time = end_time
            if (len(act_extracted) < window_min):
                print("length is not enough")
                continue
            act_string = " ".join(act_extracted)
            if(re.search(" 0 0 0 0 0", act_string)):
                print("too many zero sequences")
                continue
            act_list.append(act_string)
    return pd.DataFrame({"ID": ID, "activities": act_list})

def main():
    window_min = 180

    participants = pd.read_csv('./Todai_office_workers_data/Todai_EMA_2011-2012.csv')
    df_list = []
    for year in [2011, 2012]:
        participants_year = participants[participants.year == year]
        if year == 2011:
            activities = pd.read_csv("./Todai_office_workers_data/Activity_data/todai_activity_2011.csv", names=["ID", "datetime", "activity"], skiprows=1)
            exclude_id = [11,15, 22, 25, 30, 31]
        else:
            activities = pd.read_csv("./Todai_office_workers_data/Activity_data/todai_activity_2012.csv", names=["ID", "datetime", "activity"], skiprows=1)
            exclude_id = [10,14,17,29,26,35,38,49,52,32]
        activities['datetime'] = pd.to_datetime(activities.datetime, format="%d%b%y:%H:%M")
        activities.set_index("datetime", inplace=True)
        activities = activities.sort_index()
        
        N = max(participants_year.ID)
        for ID in range(1, N+1):
            if ID in exclude_id:
                continue
            print(year, ID)
            ID_new = str(year) + str(ID)
            participant = participants_year[participants_year.ID == ID]
            activity = activities[activities.ID == ID]
            period_awake = calc_awake_period(participant)
            extracted_activities = extractActivities(activity, period_awake, ID_new, window_min)
            df_list.append(extracted_activities)
    result_df = pd.concat(df_list)
    result_df.to_csv("results/March 2019/healthy_{}min.csv".format(window_min), index=False)

if __name__ == "__main__":
    main()