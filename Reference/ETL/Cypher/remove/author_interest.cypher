USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/author_interest.csv' as line
FIELDTERMINATOR ';'
WITH line

MERGE ( author:Author {name: line.author} )
MERGE ( interest:Interest {name: line.interest} )

create (author)-[:Interest_In]->(interest)
create (interest)-[:I_HAVE]->(author)
;