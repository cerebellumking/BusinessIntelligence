USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/paper_participate.csv' AS line
FIELDTERMINATOR ';'
WITH line

MERGE (author:Author {name: line.author})
MERGE (p:Paper {index: toInteger(line.paper)})

CREATE (author)-[:PARTICIPATE_IN]->(p)
;