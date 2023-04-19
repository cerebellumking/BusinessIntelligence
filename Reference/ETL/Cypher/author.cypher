CREATE CONSTRAINT ON (a:Author) ASSERT a.name IS UNIQUE;
CREATE CONSTRAINT ON (a:Author) ASSERT a.index IS UNIQUE;
CREATE CONSTRAINT ON (af:Affiliation)  ASSERT af.name IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM
'file:///home/author.csv' as line
FIELDTERMINATOR ';'
WITH line

CREATE (author:Author
       {
         name: line.name,
         index: toInteger(line.index),
         hi: toInteger(line.hi),
         pc: toInteger(line.pc),
         pi: toFloat(line.pi),
         cn:toInteger(line.cn),
         upi:toFloat(line.upi),
         interest: line.interest
       })
;
