USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/paper_cite.csv' as line
FIELDTERMINATOR ';'
WITH line

MERGE (p:Paper {index: toInteger(line.paper)})
MERGE (c:Paper {index: toInteger(line.cite)})

create (p)-[:CITE]->(c)
;