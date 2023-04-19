CREATE CONSTRAINT ON (v:Venue) ASSERT v.name IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/paper_publication.csv' as line
FIELDTERMINATOR ';'
WITH line

MERGE ( p:Paper {index: toInteger(line.paper)} )
MERGE ( v:Venue {name: line.venue} )

CREATE ( v ) - [:PUBLICATION] -> ( p )
;