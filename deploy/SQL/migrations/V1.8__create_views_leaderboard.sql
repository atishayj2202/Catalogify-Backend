CREATE VIEW post_likes AS
SELECT p.id                                          AS id,
       p.created_at                                  AS created_at,
       p.last_modified_at                            AS last_modified_at,
       p.user_id                                     AS post_user_id,
       p.title                                       AS post_title,
       p.category                                    AS post_category,
       p.images                                      AS post_images,
       p.description                                 AS post_description,
       p.cost                                        AS post_cost,
       p.brand                                       AS post_brand,
       p.warranty_yrs                                AS post_warranty_years,
       p.warranty_months                             AS post_warranty_months,
       p.return_days                                 AS post_return_days,
       p.seller_location                             AS post_seller_location,
       p.in_box                                      AS post_in_box,
       COUNT(r.id) FILTER (WHERE r.reaction = TRUE)  AS positive_reactions,
       COUNT(r.id) FILTER (WHERE r.reaction = FALSE) AS negative_reactions,
       COUNT(r.id)                                   AS total_reactions
FROM posts p
         LEFT JOIN
     reactions r ON p.id = r.post_id
GROUP BY p.id;

CREATE VIEW post_assessments AS
SELECT p.id               AS id,
       p.created_at       AS created_at,
       p.last_modified_at AS last_modified_at,
       p.user_id          AS post_user_id,
       p.title            AS post_title,
       p.category         AS post_category,
       p.images           AS post_images,
       p.description      AS post_description,
       p.cost             AS post_cost,
       p.brand            AS post_brand,
       p.warranty_yrs     AS post_warranty_years,
       p.warranty_months  AS post_warranty_months,
       p.return_days      AS post_return_days,
       p.seller_location  AS post_seller_location,
       p.in_box           AS post_in_box,
       r.total            AS post_score
FROM posts p,
     assessments r
WHERE p.id = r.post_id;