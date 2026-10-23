import pandas as pd
df= pd.DataFrame({
    "Teachers_name":["Sonu","Mita","Tina","Sharu"],
    "Dept":["IT","CS","Chem","Mech"],
    "Salary":[80000,70000,90000,400000]
})
print(" Original Data \n",df)
print("\n Subset(Salary>8000):\n",df[df["Salary"]>8000])
print("\n Sorted by Salary(Ascending):\n",df.sort_values("Salary"))
print("\n Sorted by Salary (Descending):\n",df.sort_values("Salary",ascending=False))
print("\n Grouped(Average Salary by Departemnt):\n",df.groupby("Dept")["Salary"].mean())
print("\n Mean=",df["Salary"].mean())
print("\n Median =",df["Salary"].median())
print("Mode=")
print(df["Salary"].mode())