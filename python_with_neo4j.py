#!/usr/bin/env python
# coding: utf-8

# In[21]:


## Packages


# In[22]:


import pandas as pd
import numpy as np
from py2neo import Graph, Node, Relationship


# In[23]:


## Initial Graph


# In[24]:


graph = Graph(uri='bolt://localhost:7687',user='neo4j', password='Data')
tx = graph.begin()


# In[25]:


# graph.delete_all()


# In[26]:


node1 = Node("Node_type_1", name="Node 1", attr2="value_attr2")
node2 = Node("Node_type_1", name="Node 2")
node3 = Node("Node_type_1", name="Node 3", attr4="value_attr4")
node4 = Node("Node_type_1", name="Node 4", attr4=44)

edgeA = Relationship(node1,"Edge_A",node2)
edgeB = Relationship(node1,"Edge_B",node3)
edgeC = Relationship(node2,"Edge_C",node1)
edgeD = Relationship(node2,"Edge_D",node3)
edgeE = Relationship(node3,"Edge_E",node1)
edgeF = Relationship(node3,"Edge_F",node2)

graph.create(node1 | node2 | node3 | edgeA | edgeB | edgeC | edgeD | edgeD | edgeE |  edgeF)    


# In[27]:


# Matching results: 


# In[28]:


# Get a py2neo table


# In[29]:


tx.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2 ').to_table()


# In[30]:


type(tx.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2 ').to_table())


# In[31]:


# return py2neo node


# In[32]:


tx.evaluate('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2')


# In[33]:


type(tx.evaluate('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2'))


# In[34]:


# return info like list


# In[35]:


tx.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2').data()


# In[36]:


type(tx.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2').data())


# In[37]:


pd.DataFrame(graph.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1.name, n1.attr2,n2.name').data())


# In[38]:


# Keys in a py2neo table


# In[39]:


graph.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2').to_table().keys()


# In[40]:


type(graph.run('MATCH (n1)-[r:Edge_A]->(n2) RETURN n1,n2').to_table().keys())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




