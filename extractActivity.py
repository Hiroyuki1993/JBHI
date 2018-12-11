import re, os, glob
import pandas as pd

def extractActivities(activity, row):
    startTime = row.start_time
    endTime = row.time
    if pd.isnull(startTime):
        activities = activity[:endTime].Activity
    else:
        activities = activity[startTime:endTime].Activity
    return activities

def main():
    participants = pd.read_csv('./MDD_data/EMA_data_all participants.csv')
    participants['time'] = pd.to_datetime(participants.time)

    activity_files = glob.glob("./MDD_data/Activity_Data/*.csv")
    for fname in activity_files:
        print(fname)
        ID = int(re.sub(r'\D', '', fname))
        patient = participants[participants.ID == ID].copy()
        patient['start_time'] = patient.shift().time
        activity = pd.read_csv(fname, index_col=0, parse_dates=True).sort_index()
        folder = "./MDD_data/Activity_Data/patient{}".format(ID)
        os.makedirs(folder, exist_ok=True)
        for rownum, (key, row) in enumerate(patient.iterrows(), 1):
            activities_cut = extractActivities(activity, row)
            if len(activities_cut) == 0:
                continue
            else:
                activities_cut.to_csv(folder + "/activity_{}.csv".format(rownum))

if __name__ == "__main__":
    main()