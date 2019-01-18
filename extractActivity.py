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
    rows = []
    participants = pd.read_csv('./MDD_data/EMA_data_all participants.csv')
    participants['time'] = pd.to_datetime(participants.time)

    activity_files = glob.glob("./MDD_data/Activity_Data/*.csv")
    for fname in activity_files:
        print(fname)
        ID = int(re.sub(r'\D', '', fname))
        patient = participants[participants.ID == ID].copy()
        patient['start_time'] = patient.time - pd.Timedelta(minutes = 30)
        patient['prevous_schedule'] = patient.shift().schedule
        activity = pd.read_csv(fname, index_col=0, parse_dates=True).sort_index()
        for rownum, (key, row) in enumerate(patient.iterrows(), 1):
            total_dep = row.total_dep
            fatigue = row.fatigue
            unconcentration = row.not_concentrating
            forgetful = row.forgetful
            headache = row.headache
            sleepiness = row.sleepiness
            total_anxiety = row.total_anxiety
            positive_mood = row.positive_mood
            negative_mood = row.negative_mood
            activities_cut = extractActivities(activity, row)
            # skip sleep or no-depression period
            if len(activities_cut) != 30 or row.prevous_schedule == 1 or total_dep != total_dep:
                continue
            else:
                act_str = " ".join(activities_cut.astype(str))
                rows.append([ID, act_str, total_dep, fatigue, unconcentration, forgetful, headache, sleepiness, total_anxiety, positive_mood, negative_mood])
    result = pd.DataFrame(rows, columns=['patient_id', 'activities', 'total_dep', 'fatigue', 'unconcentration', 'forgetful', 'headache', 'sleepiness', 'total_anxiety', 'positive_mood', 'negative_mood'])
    result.to_csv('result.csv', index=False)

if __name__ == "__main__":
    main()