USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/coauthor.csv' as line
FIELDTERMINATOR ';'
WITH line

MERGE (a1:Author {index: toInteger(line.name1)})
MERGE (a2:Author {index: toInteger(line.name2)})

create (a1)-[r1:COOPERATION]->(a2)
create (a2)-[r2:COOPERATION]->(a1)

SET r1.count = toInteger(line.count)
SET r2.count = toInteger(line.count)
;