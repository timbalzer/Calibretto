/*******************************
Calibretto Database Setup
Use each section to set up the
tables needed to run Calibretto
*******************************/


/*******************************
Table: tweets
*******************************/

-- DROP TABLE tweets;

CREATE TABLE tweets
(
  tweet_id bigint NOT NULL,
  tweet_datetime timestamp without time zone,
  tweet_keyword character varying(50),
  tweet character varying(200),
  tweeter character varying(50),
  lang character varying(50),
  latitude double precision,
  longitude double precision,
  CONSTRAINT pk_tweets PRIMARY KEY (tweet_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tweets
--  OWNER TO {your username};




/*******************************
Table: temptweets
*******************************/

-- DROP TABLE temptweets;

CREATE TABLE temptweets
(
  tweet_id bigint NOT NULL,
  tweet_datetime timestamp without time zone,
  tweet_keyword character varying(50),
  tweet character varying(200),
  tweeter character varying(50),
  lang character varying(50),
  latitude double precision,
  longitude double precision
)
WITH (
  OIDS=FALSE
);
ALTER TABLE temptweets
--  OWNER TO {your username};






/*******************************
Table: tweetlog
*******************************/

-- DROP TABLE tweetlog;

CREATE TABLE tweetlog
(
  runid serial NOT NULL,
  batchid integer,
  rundate timestamp without time zone,
  keyword character varying(50),
  harvestedthisrun integer,
  totalharvested integer,
  CONSTRAINT pk_tweetlog PRIMARY KEY (runid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tweetlog
--  OWNER TO {your username};

