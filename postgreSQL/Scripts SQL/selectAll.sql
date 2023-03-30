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
WHERE t.title='Set Acidcore / Tekno / Mentalcore 2023'
GROUP BY t.tracks_id, a.artist_name, tag.tag_name;
