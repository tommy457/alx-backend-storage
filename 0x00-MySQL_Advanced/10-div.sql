-- script that creates a function SafeDiv.
DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    IF b != 0 THEN
        RETURN A / B;
    END IF;
    RETURN 0;
END$$
DELIMITER ;
