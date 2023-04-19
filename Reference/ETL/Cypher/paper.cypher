CREATE CONSTRAINT ON (p:Paper) ASSERT p.index IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
"file:///home/paper.csv" AS line
FIELDTERMINATOR ";"
WITH line

CREATE (paper:Paper
       {
         index: toInteger(line.index),
         title: line.title,
         abstract: line.abstract,
         year: toInteger(line.year)
       }
       )
;