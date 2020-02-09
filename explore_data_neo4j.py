#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from py2neo import Graph, Node, Relationship


# In[2]:


graph = Graph(uri='bolt://localhost:7687',user='neo4j', password='Data')
tx = graph.begin()


# In[3]:


graph.delete_all()


# In[4]:


df_temp = pd.read_csv('neo4j-community-4.0.0/import/university.csv', delimiter=';')
print(df_temp.columns)
df_temp.head()


# In[5]:


load_csv = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM 'file:///grupos_colciencias.csv' AS row
    CREATE (c:Grupo_colciencias {
        COD_GRUPO_GR:row.COD_GRUPO_GR
        , NME_GRUPO_GR:row.NME_GRUPO_GRNME_MUNICIPIO_GR
        , NME_DEPARTAMENTO_GR : row.NME_DEPARTAMENTO_GR
        , ID_AREA_CON_GR : row.ID_AREA_CON_GR
        , NME_AREA_GR : row.NME_AREA_GR
        , NME_GRAN_AREA_GR : row.NME_GRAN_AREA_GR
        , NME_CLASIFICACION_GR : row.NME_CLASIFICACION_GR
        , INST_AVAL : row.INST_AVAL
    })
"""
graph.run(load_csv)


# In[6]:


load_csv = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM 'file:///proyectos_colciencias.csv' AS row
    CREATE (c:Proyecto_colciencias {
        CODIGO_PROYECTO : row.CODIGO_PROYECTO
        ,TITULO_PROYECTO : row.TITULO_PROYECTO
        ,ENTIDAD : row.ENTIDAD
        ,AREA_TEMATICA : row.AREA_TEMATICA
        ,DEPARTAMENTO_ENTIDAD : row.DEPARTAMENTO_ENTIDAD
        ,CIUDAD_ENTIDAD : row.CIUDAD_ENTIDAD
    })
"""
graph.run(load_csv)


# In[7]:


load_csv = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM 'file:///revistas_indexadas.csv' AS row
    CREATE (c:Revistas_indexadas {
        NRO_ISSN : row.NRO_ISSN
        ,TITULO : row.TITULO
        ,INST_EDITORA : row.INST_EDITORA
        ,TXT_CLASIFICACION : row.TXT_CLASIFICACION
        ,MUNICIPIO : row.MUNICIPIO
        ,DEPARTAMENTO : row.DEPARTAMENTO
    })
"""
graph.run(load_csv)


# In[8]:


load_csv = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM 'file:///university.csv' AS row
    CREATE (c:University {
        Name : row.Name
    })
"""
graph.run(load_csv)    


# In[9]:


load_csv = """
    USING PERIODIC COMMIT 500
    LOAD CSV WITH HEADERS FROM 'file:///municipios.csv' AS row
    CREATE (c:Municipios {
        nombre : row.nombre
        ,pais : row.pais
    })
"""
graph.run(load_csv)  


# In[10]:


create_relationships = """
    MATCH(gc:Grupo_colciencias),(m:Municipios)
    WHERE gc.NME_DEPARTAMENTO_GR = m.nombre
    CREATE (gc)-[r:FROM]->(m)
    RETURN r
"""
graph.run(create_relationships)    


# In[11]:


create_relationships = """
    MATCH(pc:Proyecto_colciencias),(m:Municipios)
    WHERE pc.CIUDAD_ENTIDAD = m.nombre
    CREATE (pc)-[r:FROM]->(m)
    RETURN r
"""
graph.run(create_relationships)    


# In[12]:


create_relationships = """
   MATCH(ri:Revistas_indexadas),(m:Municipios)
    WHERE ri.MUNICIPIO = m.nombre
    CREATE (ri)-[r:FROM]->(m)
    RETURN r
"""
graph.run(create_relationships)    


# In[13]:


# Group data


# In[14]:


group_query = """
    MATCH (m:Municipios)<-[:FROM]-(gc:Grupo_colciencias)
    WITH m.nombre as name, count(gc) AS groups_by_city
    WHERE groups_by_city > 100
    RETURN *
    ORDER BY groups_by_city desc
"""
graph.run(group_query)    


# In[15]:


university_relationship = """
    MATCH(ri:Revistas_indexadas),(u:University)
    WHERE ri.INST_EDITORA = u.Name
    CREATE (ri)-[r:BELONG_TO]->(u)
    RETURN type(r)
"""
graph.run(university_relationship)


# In[16]:


university_relationship = """
    MATCH(gc:Grupo_colciencias),(u:University)
    WHERE gc.INST_AVAL = u.Name
    CREATE (gc)-[r:BELONG_TO]->(u)
    RETURN type(r)
"""
graph.run(university_relationship)


# In[17]:


university_relationship = """
    MATCH(pc:Proyecto_colciencias),(u:University)
    WHERE pc.ENTIDAD = u.Name
    CREATE (pc)-[r:BELONG_TO]->(u)
    RETURN type(r)
"""
graph.run(university_relationship)


# In[ ]:





# In[ ]:





# In[ ]:




