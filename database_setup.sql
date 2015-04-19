/*******************************
Calibretto Database Setup
Use each section to set up the
tables needed to run Calibretto
*******************************/


/*******************************
Table: tweets
*******************************/
CREATE TABLE tweets
(
  tweet_id bigint NOT NULL PRIMARY KEY,
  tweet_datetime timestamp without time zone,
  tweet_keyword character varying(50),
  tweet character varying(200),
  tweeter character varying(50),
  lang character varying(50),
  latitude double precision,
  longitude double precision
)



/*******************************
Table: temptweets
*******************************/
CREATE TABLE temptweets
(
  tweet_id bigint NOT NULL PRIMARY KEY,
  tweet_datetime timestamp without time zone,
  tweet_keyword character varying(50),
  tweet character varying(200),
  tweeter character varying(50),
  lang character varying(50),
  latitude double precision,
  longitude double precision
)
