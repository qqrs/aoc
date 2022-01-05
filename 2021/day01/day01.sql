CREATE TABLE pings (
   depth INTEGER
);

-- .import example.txt pings
.import input.txt pings

SELECT sum(x) FROM (SELECT depth > lag(depth, 1) OVER () AS x FROM pings) ;
SELECT sum(x) FROM (SELECT depth > lag(depth, 3) OVER () AS x FROM pings) ;


WITH zzz AS (
    SELECT row_number() OVER () as n,
        sum(depth) OVER lagwin < sum(depth) OVER curwin as x
    FROM pings
    WINDOW lagwin AS (ROWS 3 PRECEDING EXCLUDE CURRENT ROW),
        curwin AS (ROWS 2 PRECEDING)
) select sum(n > 3 and x) from zzz ;

