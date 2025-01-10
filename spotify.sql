create database spotify_db;
use spotify_db;
CREATE TABLE IF NOT EXISTS spotify_tracks (
	id INT auto_increment primary key,
    track_name VARCHAR(255),
	artist VARCHAR(255),
    album VARCHAR(255),
    popularity INT,
    Duration_mins FLOAT);
    
 SELECT * FROM track_details  
 
 RENAME TABLE trackdata TO track_details;
delete from track_details where id =3;

ALTER TABLE track_details ADD UNIQUE (track_name, artist);

select avg(popularity) from track_details;


SELECT 
	CASE 
		WHEN popularity>=80 THEN 'very popular'
        WHEN popularity>=50 THEN 'popular'
		ELSE 'less popular'
        END AS popularity_range,
        count(*) as track_count
from track_details     
group by popularity_range;
having popularity >60;


