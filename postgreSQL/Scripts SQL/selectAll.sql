SELECT 
    t.tracks_id, 
    t.title, 
    a.artist_name, 
    t.datep, 
    t.num_likes, 
    t.num_comments, 
    t.num_streams, 
    tag.tag_name AS main_tag, 
    array_agg(DISTINCT tag2.tag_name) AS tag_list
FROM tracks t
JOIN artists a ON t.artists_id = a.artists_id
JOIN tags tag ON t.maintag = tag.tags_id
LEFT JOIN tracks_tags tt ON t.tracks_id = tt.tracks_id
LEFT JOIN tags tag2 ON tt.tags_id = tag2.tags_id

GROUP BY t.datep, t.num_streams, tag.tag_name, a.artist_name, t.tracks_id;



INSERT INTO public.tracks
(
	title,
	artists_id,
	datep,
	num_likes,
	num_comments,
	num_streams,
	maintag,
	taglist
) 
VALUES 
(
	'techhhhh111',
	(SELECT artists_id FROM public.artists WHERE artist_name = 'jakubae1738'),
	'2023-03-16 23:43:06',
	'14',
	'0',
	'186',
	(SELECT tags_id FROM public.tags WHERE tag_name = 'techno'),
	ARRAY(SELECT tags_id FROM public.tags WHERE tag_name = 'tekno')
) 
ON CONFLICT (title)
DO UPDATE SET num_likes = '14',
num_comments = '0', num_streams = '186',
taglist = array_append(tracks.taglist, (SELECT tags.tags_id FROM public.tags WHERE tag_name = 'tekno'))
WHERE tracks.title = 'techhhhh111';

SELECT array_append(ARRAY[2,9], 6);

SELECT  
    tag.tag_name AS main_tag,
	SUM(t.num_streams) as num_streams_by_tag
FROM tracks t
JOIN tags tag ON t.maintag = tag.tags_id
LEFT JOIN tracks_tags tt ON t.tracks_id = tt.tracks_id
LEFT JOIN tags tag2 ON tt.tags_id = tag2.tags_id
GROUP BY main_tag
ORDER BY num_streams_by_tag DESC;

SELECT
	COUNT(tags_id)
FROM tags;

GROUP BY t.datep, t.num_streams, tag.tag_name, a.artist_name, t.tracks_id;