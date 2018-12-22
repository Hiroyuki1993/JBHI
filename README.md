# environments
Python 3.6.4
```
$ls
MDD_data   Todai_office_workers_data  preprocessing.ipynb
README.md  extractActivity.py         xls2csv.py
```

# preprocessing
## cut the activity data
```
$python xls2csv.py
$python extractActivity.py
```
warning: you should correct the typo of year in patient no.1 and no.3 before execute xls2csv.py

## results
extractActivity.py cut activity data into many segments.

```
.../MDD_data/Activity_Data/patient1$ ls
activity_12_0.csv   activity_27_1.csv  activity_42_0.csv  activity_63_1.csv
activity_12_1.csv   activity_28_1.csv  activity_42_1.csv  activity_65_1.csv ...
```

file name description: activity_{row number}_{cut_number}
For example, activity_12_2.csv corresponds to 2nd segment of 12nd row in EMA_data_all.csv for patient no.1 .
extractActivity cut the segments if 0 continues more than 5 times.