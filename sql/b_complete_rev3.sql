/*
Author: Sebastian Alvarez
Script date: January 17, 2023
Description: This query returns all the info regarding a B device: id, name, PLC, comment and status (used/not used)
*/

DROP TABLE IF EXISTS B_complete_3;
CREATE TABLE B_complete_3 AS(
	SELECT
		t3.id,
		t3.device_name,
		t3.plc,
		t4.comment,
		CASE
			WHEN t4.device_name IS NULL THEN 'Not used'
			ELSE 'Used'
		END AS device_status
	FROM B_range_plc_class t3
	LEFT JOIN (
		SELECT
			t1.device_name,
			t1.comment,
			CASE
				WHEN t2.device_name IS NULL THEN 'Not used'
				ELSE 'Used'
			END AS device_status
		FROM ge6_cc_ac1_comments t1
		LEFT JOIN (
			-- these selection returns only B devices from the used devices table
			SELECT 
				DISTINCT(device_name)
			FROM ge6_cc_ac1_used_devices
			WHERE device_name LIKE('B%')
			) t2
			ON t1.device_name = t2.device_name
		WHERE t1.device_name LIKE('B%') 
	) t4
	ON t3.device_name = t4.device_name
);


