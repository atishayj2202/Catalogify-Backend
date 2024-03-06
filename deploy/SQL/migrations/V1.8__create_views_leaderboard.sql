CREATE VIEW post_likes AS
SELECT p.id                                          AS id,
       p.created_at                                  AS created_at,
       p.last_modified_at                            AS last_modified_at,
       p.category                                    AS post_category,
       COUNT(r.id) FILTER (WHERE r.reaction = TRUE)  AS positive_reactions
FROM posts p
         LEFT JOIN
     reactions r ON p.id = r.post_id
GROUP BY p.id;

CREATE VIEW post_assessments AS
SELECT p.id               AS id,
       p.created_at       AS created_at,
       p.last_modified_at AS last_modified_at,
       p.category         AS post_category,
       r.total            AS post_score
FROM posts p,
     assessments r
WHERE p.id = r.post_id;