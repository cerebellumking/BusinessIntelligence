USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/author_affiliation.csv' as line
FIELDTERMINATOR ';'
WITH line

MERGE ( author:Author {name: line.author} )
MERGE ( affiliation:Affiliation {name: line.affiliation} )

create (author)-[:AFFILIATED_WITH]->(affiliation)
create (affiliation)-[:HAVE]->(author)
;