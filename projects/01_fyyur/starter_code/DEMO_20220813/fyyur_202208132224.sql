--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    phone character varying(120),
    genres character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    website character varying(120),
    seeking_venue boolean,
    seeking_description character varying(120)
);


ALTER TABLE public.artist OWNER TO postgres;

--
-- Name: artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artist_id_seq OWNER TO postgres;

--
-- Name: artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artist_id_seq OWNED BY public.artist.id;


--
-- Name: show; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.show (
    id integer NOT NULL,
    venue_id integer NOT NULL,
    artist_id integer NOT NULL,
    start_time timestamp without time zone
);


ALTER TABLE public.show OWNER TO postgres;

--
-- Name: show_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.show_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.show_id_seq OWNER TO postgres;

--
-- Name: show_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.show_id_seq OWNED BY public.show.id;


--
-- Name: venue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.venue (
    id integer NOT NULL,
    name character varying,
    city character varying(120),
    state character varying(120),
    address character varying(120),
    phone character varying(120),
    image_link character varying(500),
    facebook_link character varying(120),
    website character varying(120),
    seeking_talent boolean,
    seeking_description character varying(120),
    genres character varying[]
);


ALTER TABLE public.venue OWNER TO postgres;

--
-- Name: venue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venue_id_seq OWNER TO postgres;

--
-- Name: venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.venue_id_seq OWNED BY public.venue.id;


--
-- Name: artist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist ALTER COLUMN id SET DEFAULT nextval('public.artist_id_seq'::regclass);


--
-- Name: show id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show ALTER COLUMN id SET DEFAULT nextval('public.show_id_seq'::regclass);


--
-- Name: venue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venue ALTER COLUMN id SET DEFAULT nextval('public.venue_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
a8ff295911e6
\.


--
-- Data for Name: artist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) FROM stdin;
1	Yvan TCHOUDIE DJOMESSI	Douala	CA	677550471	{}	https://www.petitionpublicservice.eu/wp-content/uploads/2013/04/public-services.jpg	https://www.facebook.com	\N	t	Yvan TCHOUDIE is the first Artist in this project
2	Mister LEO	Bamenda	CA	35214515145112	{}	https://z-p3-scontent.fdla2-1.fna.fbcdn.net/v/t39.30808-6/274502709_490938372388541_8471053129604412073_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeGqRX4Ol5T4sKc1gKkRoQRSHFrGwjXmd28cWsbCNeZ3b12rMMlXdMHimOSW6kamyXVZnIqOHbX-7pFTRZIgTSkE&_nc_ohc=xg4DXgHA_FYAX_RdAAG&_nc_zt=23&_nc_ht=z-p3-scontent.fdla2-1.fna&oh=00_AT9Ys1idh984qCxjT1lkNa_TJOsc1Mwa2G-jtRpo6d-pLA&oe=62FDE6DD	https://web.facebook.com/leo4live?_rdc=1&_rdr	\N	t	Mr LEO is an impressive Cameroonian Musician
3	Charlotte Dipanda	Douala	CA	677550471	{Blues,Classical}	https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/CharlotteDipanda.jpg/400px-CharlotteDipanda.jpg	https://web.facebook.com/charlottedipandaofficiel?_rdc=1&_rdr	\N	t	Charlotte Dipanda is a very exceptional Artist
\.


--
-- Data for Name: show; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.show (id, venue_id, artist_id, start_time) FROM stdin;
1	1	1	2022-08-12 21:04:13
2	1	1	2022-08-16 21:04:13
3	1	2	2022-06-13 21:04:13
4	1	2	2021-08-13 21:04:13
5	1	2	2022-10-13 21:04:13
7	2	2	2020-08-13 21:40:25
8	2	1	2020-05-13 11:40:25
9	1	3	2020-08-13 21:40:25
10	3	3	2022-08-13 22:03:27
\.


--
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.venue (id, name, city, state, address, phone, image_link, facebook_link, website, seeking_talent, seeking_description, genres) FROM stdin;
1	Avenue De Gaulle	Douala	Country	Bonanjo - Douala	677550471	https://www.petitionpublicservice.eu/wp-content/uploads/2013/04/public-services.jpg	https://www.facebook.com	\N	t	L avenue de Gaulle est situee a Douala, precisement a Bonanjo	{Alternative,Blues,Classical}
2	Krystal Palace	Douala	Classical	AKWA, Boulevard de la liberte	52144114135	https://z-p3-scontent.fdla2-1.fna.fbcdn.net/v/t39.30808-6/281877478_1870756583116349_6111031574872413819_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeGVoDvCWxOL4EBNt1cqZ_9VvNAEAAWz6VG80AQABbPpUUw0c0_4Sa1yWp5oKlrqxzTILlTwl7lujzF8bxgC7M8L&_nc_ohc=GICA_gd-AasAX_yN8d8&tn=eC0SItKtKzzDgp4u&_nc_zt=23&_nc_ht=z-p3-scontent.fdla2-1.fna&oh=00_AT-ZDXXxjgsiKhBSSRh5C6JpQoMml4iLwNzsmaKsdQRjww&oe=62FC5805	https://web.facebook.com/krystalpalacedouala/?_rdc=1&_rdr	\N	t	Krystal Palace est un super interessant et VIP pour les artistes	{Blues,Classical,Country,Electronic,Folk,Funk,HipHop,HeavyMetal,Instrumental,Jazz,MusicalTheatre}
3	Oympia	Yaounde	Classical	Biyem assi montee Jouvence	319814654687	https://z-p3-scontent.fdla2-1.fna.fbcdn.net/v/t1.6435-9/59794092_2184812608272576_2711172786767790080_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeFdITZxRFsMFwIq0BfLLJBfmbZ01Sm1FEiZtnTVKbUUSAU3fXFczzNl14MAvEeqf4wRSPQuf2d10itViUq2by4X&_nc_ohc=3lcQUvk-0s8AX8UG_24&_nc_ht=z-p3-scontent.fdla2-1.fna&oh=00_AT-N9rJUcHinvhs25Wn4DT36AqCNDZukSvU2PWxTtcSYIw&oe=631C797A	https://web.facebook.com/Olympia-Lounge-SNACK-BAR-423009881119533/	\N	t	Olympia is a Lounge great for artist and for Shows	{Alternative,Blues,Classical,Country,Electronic}
\.


--
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.artist_id_seq', 3, true);


--
-- Name: show_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.show_id_seq', 10, true);


--
-- Name: venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venue_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: show show_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_pkey PRIMARY KEY (id);


--
-- Name: venue venue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id);


--
-- Name: show show_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: show show_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.show
    ADD CONSTRAINT show_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venue(id);


--
-- PostgreSQL database dump complete
--

