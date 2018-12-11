import pandas as pd
import xlrd, os, glob

def main():
    excel_files = glob.glob("./MDD_data/Activity_Data/*.xls")
    for fname in excel_files:
        print(fname[:-4])
        data = pd.read_excel(fname)
        data.to_csv(fname[:-3]+"csv", index=False)

if __name__ == "__main__":
    main()