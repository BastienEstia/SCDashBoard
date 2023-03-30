-- SCHEMA: public

-- DROP SCHEMA IF EXISTS public ;

CREATE SCHEMA IF NOT EXISTS public
    AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT USAGE ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO pg_database_owner;

	DROP TABLE tracks_artists;
	DROP TABLE tracks_tags;
	DROP TABLE tracks;
	DROP TABLE tags;
	DROP TABLE artists;
	
	-- Création de la table artists
	
	CREATE TABLE artists (
		artists_id SERIAL PRIMARY KEY,
		artist_name VARCHAR(60) UNIQUE,
		num_sub INT
	);
	
	-- Création de la table tags
	
	CREATE TABLE tags (
		tags_id SERIAL PRIMARY KEY,
		tag_name VARCHAR(60) UNIQUE
	);
	
	--Création de la table tracks
	
	CREATE TABLE tracks (
		tracks_id SERIAL PRIMARY KEY,
		title VARCHAR(100) UNIQUE NOT NULL,
		artists_id INT REFERENCES artists (artists_id),
		dateP DATE NOT NULL,
		num_likes INT,
		num_comments INT,
		num_streams INT,
		maintag INT REFERENCES tags (tags_id),
		taglist INT[]
	);

	-- Ajout de la colonne artists_id fk pour la table artists
	--ALTER TABLE tracks
	--ADD COLUMN artists_id INT REFERENCES artists (artists_id);
	
	-- Création de la table d'association tracks_artists
	
	CREATE TABLE tracks_artists (
		tracks_id INT REFERENCES tracks (tracks_id),
		artists_id INT REFERENCES artists (artists_id),
		PRIMARY KEY (tracks_id, artists_id)
	);
	
	-- Création de la table d'association tracks_tags
	
	CREATE TABLE tracks_tags (
		tracks_id INT REFERENCES tracks(tracks_id),
		tags_id INT REFERENCES tags(tags_id),
		PRIMARY KEY (tracks_id, tags_id)
	);
	
	
	SELECT * FROM tracks;
	
	WITH artist_data AS (SELECT artists_id FROM artists WHERE artist_name = 'Dave Vincent');