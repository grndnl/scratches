# Scratches


Conda not found ubuntu wsl: 
``` bash
source ~/anaconda3/etc/profile.d/conda.sh
```
---
 saving list of strings with newline character to csv. Here is a simple solution: Replace all \n with \\n before saving to CSV. This will preserve the newline characters.
```
df.loc[:, "Column_Name"] = df["Column_Name"].apply(lambda x: x.replace('\n', '\\n'))
df.to_csv("df.csv", index=False)
```
