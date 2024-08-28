\set aid random(1, 100000 * :scale)
\set bid random(1, 1 * :scale)
\set tid random(1, 10 * :scale)
\set delta random(-5000, 5000)

select bid from pgbench_accounts limit 600;
UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid and bid = :bid;
select tid from pgbench_tellers WHERE tid = :tid;

SELECT tbalance FROM pgbench_tellers WHERE tid >= :tid limit 600;
select tid from pgbench_tellers limit 600;
INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);

SELECT tbalance FROM pgbench_tellers WHERE tid >= :tid limit 600;
select count(*) from pgbench_tellers ;

select bid from pgbench_tellers WHERE tid = :tid;

SELECT aid, abalance FROM pgbench_accounts WHERE aid >= :aid limit 600;
select tid, tbalance from pgbench_tellers limit 600;

BEGIN;
select mtime from pgbench_history where tid = :tid ;
select * from pgbench_tellers limit 600;
SELECT tbalance FROM pgbench_tellers WHERE tid < :tid limit 600;
DELETE FROM pgbench_accounts WHERE aid = :aid;
DELETE FROM pgbench_history WHERE aid = :aid;
END;