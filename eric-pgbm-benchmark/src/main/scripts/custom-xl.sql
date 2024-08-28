\set aid random(1, 100000 * :scale)
\set bid random(1, 1 * :scale)
\set tid random(1, 10 * :scale)
\set delta random(-15000, 15000)
\set y (6000)
\set z (100000 * :bid)
\set w (1)
\set v (2)
\set u (3)

SELECT * FROM pgbench_tellers WHERE  tbalance >= :w ORDER BY bid ;
select * from pgbench_tellers WHERE tbalance >= :w ORDER BY tbalance;
INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);

select * from pgbench_history where bid = :bid order by delta ;

UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE  tid = :tid and MOD(:aid, :u) = :w ;

select * from pgbench_accounts WHERE bid = :bid  and aid < :z and aid > :z - :y  ORDER BY abalance ;

SELECT tbalance FROM pgbench_tellers where tid = :tid ORDER BY tbalance ;

select delta from pgbench_history where tid = :tid order by delta;

DELETE FROM pgbench_accounts WHERE aid = :aid + :w and MOD(:aid, :v) = :w;

BEGIN;
select * from pgbench_tellers where bid >= :bid and tbalance >= :w order by tbalance ;
DELETE FROM pgbench_accounts WHERE aid = :aid;
DELETE FROM pgbench_history WHERE tid = :tid;
END;