import pandas as pd

def extractActivities(activity, row):
    if pd.isnull(row.startTime):
        activities = activity[:row.endTime].activity
    else:
        activities = activity[row.startTime:row.endTime].activity
    return activities

def main():
    rows = []
    participants = pd.read_csv('./Todai_office_workers_data/Todai_EMA_2011-2012.csv')
    participants = participants[["ID", "year", "time", "type_of_record"]]
    participants['endTime'] = pd.to_datetime(participants.time)
    participants['startTime'] = participants.endTime - pd.Timedelta(minutes=30)

    for year in [2011, 2012]:
        participants_year = participants[participants.year == year]
        if year == 2011:
            activities = pd.read_csv("./Todai_office_workers_data/Activity_data/todai_activity_2011.csv", names=["ID", "datetime", "activity"], skiprows=1)
        else:
            activities = pd.read_csv("./Todai_office_workers_data/Activity_data/todai_activity_2012.csv", names=["ID", "datetime", "activity"], skiprows=1)
        activities['datetime'] = pd.to_datetime(activities.datetime, format="%d%b%y:%H:%M")
        activities.set_index("datetime", inplace=True)
        activities = activities.sort_index()

        N = max(participants_year.ID)
        for ID in range(1, N+1):
            print(year, ID)
            subject = participants_year[participants_year.ID == ID]
            activity = activities[activities.ID == ID]
            for rownum, (key, row) in enumerate(subject.iterrows(), 1):
                if row.type_of_record in [" ptonn", " awake"]:
                    continue
                activities_cut = extractActivities(activity, row)
                if len(activities_cut) < 25:
                    continue
                act_str = " ".join(activities_cut.astype(str))
                rows.append([ID, row.startTime, row.endTime, act_str])
    result = pd.DataFrame(rows, columns=['patient_id', 'startTime', 'endTime', 'activities'])
    result.to_csv('HealthyWorkers.csv', index=False)

if __name__ == "__main__":
    main()