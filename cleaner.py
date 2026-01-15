import csv
import numpy as np

class EmployeeDataCleaner:
    def __init__(self):
        self.csv_file = "messy_data.csv"
        self.id = []
        self.names = []
        self.header = []

        self.data = []

    def distributor(self):
        header = np.genfromtxt(self.csv_file, delimiter=',', dtype=str)
        self.header = header[0]

        id =  np.genfromtxt(self.csv_file, delimiter=',', dtype=str, skip_header=True, usecols=[0])
        self.id = id

        names = np.genfromtxt(self.csv_file, delimiter=',', dtype=str, skip_header=True, usecols=[1])
        self.names = names

        data = np.genfromtxt(self.csv_file, delimiter=',', skip_header=1, dtype=float, usecols=range(2,len(self.header)))
        self.data = data


    def fill_missing(self):
        mean = np.round(np.nanmean(self.data, axis=0), 2)
        data = np.where(np.isnan(self.data), mean, self.data)
        self.data = data


    def handle_outlier(self):
        experience_year = np.clip(self.data[:,1], 0,100)
        self.data[:,1] = experience_year

        monthly_hour = np.clip(self.data[:,2], 0, 300)
        self.data[:,2] = monthly_hour

        salary = np.clip(self.data[:,3], 1,None)
        self.data[:,3] = salary


    def generate_csv(self):
        output_file = "cleaned_data.csv"
        with open(output_file, 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(self.header)

            for id, names, vals in zip(self.id, self.names, self.data):
                write.writerow([id,names]+ vals.tolist())

        print('='*20, f"Saved file as {output_file}", '=' *20)


def main():
    c = EmployeeDataCleaner()
    c.distributor()
    c.fill_missing()
    c.handle_outlier()
    c.generate_csv()

if __name__ == '__main__':
    main()