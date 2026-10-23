import pandas as pd 
df= pd.DataFrame({
    "Teachers_Name":["Amol","Geeta","Swara","Sonam"],
    "Dept":["CS","IT","Mech","Civil"],
    "Salary":[15000,60000,80000,30000]
})

print("Original Data :\n",df)

print("\n Subset(Salary>80000):\n",df[df["Salary"] > 8000])

print("\nSorted by Salary(Ascending):\n",df.sort_values("Salary"))

print("\nSorted by Salary(Descending):\n",df.sort_values("Salary",ascending=False))

print("\n Grouped(Average Salary by Department):\n",df.groupby("Dept")["Salary"].mean())
print("Median =",df["Salary"].median())
print("Mode= \n")
print(df["Salary"].mode())