import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df1 = pd.read_csv("zomato.csv")
df1.drop(columns=['url', 'address', 'phone', 'reviews_list'], inplace=True, errors='ignore')

df1['rate'] = df1['rate'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)

df1['approx_cost(for two people)'] = df1['approx_cost(for two people)'].astype(str).str.replace(',', '', regex=False)
df1['approx_cost(for two people)'] = pd.to_numeric(df1['approx_cost(for two people)'], errors='coerce')

df1.dropna(how='any', subset=['location', 'cuisines', 'approx_cost(for two people)', 'rate'], inplace=True)

print(df1.shape)

sns.set_palette('pastel')
sns.set_style('white')

plt.figure(figsize=(12, 5))
sns.countplot(data=df1, x='location', order=df1['location'].value_counts().iloc[:10].index)
plt.xticks(rotation=45)
plt.title('Restaurant Count per Location')
plt.show()

df1['rate_category'] = pd.cut(df1['rate'], bins=[0, 3.5, 4.2, 5], labels=['Low', 'Medium', 'High'])
plt.figure(figsize=(8, 5))
sns.boxplot(x='rate_category', y='approx_cost(for two people)', data=df1)
plt.ylim(0, 3000)
plt.title('Cost Distribution across Rating Categories')
plt.show()

text_d = " ".join(str(x) for x in df1['rest_type'].dropna())
wc_d = WordCloud(width=600, height=300, background_color='lightgrey', colormap='Set2').generate(text_d)
plt.figure(figsize=(10, 5))
plt.imshow(wc_d, interpolation='bilinear')
plt.axis("off")
plt.title('Popular Restaurant Types')
plt.show()