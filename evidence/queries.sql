-- Read-only metadata queries used 2026-10-12.
-- Run individually with the clickhouse-client skill from the project root.
-- Defaults: 30 seconds, 100 result rows; pass --setting max_rows_to_read=1000000.
SELECT database, sum(bytes_on_disk) AS bytes, sum(rows) AS rows, count() AS active_parts
FROM system.parts WHERE active GROUP BY database ORDER BY bytes DESC LIMIT 100;
SELECT name,total_space,free_space,unreserved_space FROM system.disks LIMIT 100;
SELECT name,sorting_key,partition_key,
 extract(create_table_query,'TTL (.*?)(?: SETTINGS|$)') AS ttl
FROM system.tables WHERE database='solana'
 AND (name IN ('transaction_token_balance','trades','pool_transactions_cache') OR startsWith(name,'meteora_'))
ORDER BY name LIMIT 100;
SELECT multiIf(positionCaseInsensitive(create_table_query,'toIntervalMonth(1)')>0,'1 month',
 positionCaseInsensitive(create_table_query,'toIntervalYear(1)')>0,'1 year',
 position(create_table_query,'TTL ')>0,'other TTL','no TTL') AS retention,
 count() AS tables,sum(total_bytes) AS bytes
FROM system.tables WHERE database='solana' AND engine LIKE '%MergeTree%'
GROUP BY retention ORDER BY bytes DESC LIMIT 100;
SELECT table,sum(rows) AS rows,sum(bytes_on_disk) AS bytes
FROM system.parts WHERE active AND database='solana'
 AND (startsWith(table,'meteora_') OR table IN ('transaction_token_balance','trades','pool_transactions_cache'))
GROUP BY table ORDER BY bytes DESC LIMIT 100;
SELECT now() AS measured_at,
 sumIf(bytes_on_disk,startsWith(table,'meteora_') AND NOT startsWith(table,'meteora_damm')) AS dlmm_bytes,
 sumIf(bytes_on_disk,table='transaction_token_balance') AS balance_bytes
FROM system.parts WHERE active AND database='solana' LIMIT 100;
