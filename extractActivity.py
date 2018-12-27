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
        patient['start_time'] = patient.shift().time
        patient['prevous_schedule'] = patient.shift().schedule
        activity = pd.read_csv(fname, index_col=0, parse_dates=True).sort_index()
        folder = "./MDD_data/Activity_Data/patient{}".format(ID)
        os.makedirs(folder, exist_ok=True)
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
            if len(activities_cut) == 0 or row.prevous_schedule == 1 or total_dep != total_dep:
                continue
            else:
                # cut in zero sequence
                is_active = activities_cut.apply(lambda x: 0 if x==0 else 1)
                sequence = is_active.astype(str).str.cat()
                # thorethold: zero more than 5 times -> device off
                matches = re.finditer('0{6,}', sequence)
                start = 0
                num_off = 0
                for num_off, match in enumerate(matches):
                    end = match.start()
                    # if data lentgh is too short, we don't generate row.
                    if abs(end - start) < 10:
                        start = match.end()
                        continue
                    act_str = " ".join(activities_cut[start:end].astype(str))
                    rows.append([ID, act_str, total_dep, fatigue, unconcentration, forgetful, headache, sleepiness, total_anxiety, positive_mood, negative_mood])
                    start = match.end()
                if(len(activities_cut[start:]) > 10):
                    num_off += 1
                    act_str = " ".join(activities_cut[start:].astype(str))
                    rows.append([ID, act_str, total_dep, fatigue, unconcentration, forgetful, headache, sleepiness, total_anxiety, positive_mood, negative_mood])
                # rows.append([ID, act_str, total_dep])
    result = pd.DataFrame(rows, columns=['patient_id', 'activities', 'total_dep', 'fatigue', 'unconcentration', 'forgetful', 'headache', 'sleepiness', 'total_anxiety', 'positive_mood', 'negative_mood'])
    # result = pd.DataFrame(rows, columns=['patient_id', 'activities', 'total_dep'])
    result.to_csv('result.csv', index=False)

if __name__ == "__main__":
    main()