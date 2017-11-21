
# coding: utf-8

# In[1]:


import pandas as pd


# In[12]:


data = pd.read_csv("jfkrelease-2017-dce65d0ec70a54d5744de17d280f3ad2.csv", sep=';')


# In[13]:


data.head()


# In[15]:


meanPages = data['Num Pages'].mean()
meanPages


# In[16]:


maxPages = data['Num Pages'].max()
maxPages


# In[17]:


minPages = data['Num Pages'].min()


# In[18]:


minPages


# In[24]:


missingPages = data['Num Pages'].isnull().sum()
missingPages


# In[28]:


nbTypes = data['Doc Type'].nunique()
nbTypes


# In[29]:


nbDocTypes = data['Doc Type'].value_counts()
nbDocTypes


# In[30]:


nbAgencies = data['Agency'].nunique()
nbAgencies


# In[31]:


nbDocAgencies = data['Agency'].value_counts()
nbDocAgencies


# In[57]:


import seaborn as sns
get_ipython().magic('matplotlib inline')


# In[58]:


ax = sns.countplot(x="Doc Type", data=data)
ax


# In[59]:


ax = sns.countplot(x="Agency", data=data)
ax

