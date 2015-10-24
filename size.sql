SELECT CONCAT(table_schema, '.', table_name),
       CONCAT(ROUND(table_rows, 2), 'rs') rows,
       CONCAT(ROUND(data_length / (1024), 2), 'KB') data,
       CONCAT(ROUND(index_length / (1024), 2), 'KB') idx,
       CONCAT(ROUND(( data_length + index_length ) / (1024), 2), 'KB') total_size,
       ROUND(index_length / data_length, 2) idxfrac
FROM   information_schema.TABLES
ORDER  BY data_length + index_length DESC
LIMIT  15;