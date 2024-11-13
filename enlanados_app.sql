BEGIN;

-- Create tables

CREATE TABLE IF NOT EXISTS public.product
(
    id SERIAL,
    name character varying,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.product_type
(
    id SERIAL,
    name character varying,
    product_id integer,
    price real NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.city
(
    id SERIAL,
    name character varying,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.payment_method
(
    id SERIAL,
    name character varying,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.status
(
    id SERIAL,
    name character varying,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS public.whool_stock
(
    id SERIAL,
    color character varying NOT NULL,
    quantity integer NOT NULL,
    last_update date NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (color)
);

CREATE TABLE IF NOT EXISTS public."order"
(
    id SERIAL,
    client character varying NOT NULL,
    city_id integer NOT NULL,
    product_type_id integer NOT NULL,
    description text NOT NULL,
    added_price real DEFAULT 0.0,
    credit real DEFAULT 0.0,
    payment_method_id integer NOT NULL,
    estimated_date date NOT NULL,
    status_id integer NOT NULL DEFAULT 1,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id)
);

CREATE TABLE IF NOT EXISTS public.order_whool
(
    id SERIAL,
    order_id integer NOT NULL,
    whool_stock_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (id)
);


-- Add foreign key constraints

ALTER TABLE IF EXISTS public.product_type
    ADD FOREIGN KEY (product_id)
    REFERENCES public.product (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;
    

ALTER TABLE IF EXISTS public."order"
    ADD CONSTRAINT city_fk FOREIGN KEY (city_id)
    REFERENCES public.city (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."order"
    ADD CONSTRAINT product_type_fk FOREIGN KEY (product_type_id)
    REFERENCES public.product_type (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."order"
    ADD CONSTRAINT payment_method_fk FOREIGN KEY (payment_method_id)
    REFERENCES public.payment_method (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public."order"
    ADD CONSTRAINT status_fk FOREIGN KEY (status_id)
    REFERENCES public.status (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.order_whool
    ADD CONSTRAINT order_fk FOREIGN KEY (order_id)
    REFERENCES public."order" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.order_whool
    ADD CONSTRAINT whool_stock_fk FOREIGN KEY (whool_stock_id)
    REFERENCES public.whool_stock (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


-- Add check constraints

ALTER TABLE IF EXISTS public.product_type
    ADD CHECK (price>0.0);

ALTER TABLE IF EXISTS public."order"
    ADD CHECK (added_price>=0.0);

ALTER TABLE IF EXISTS public."order"
    ADD CHECK (credit>=0.0);

ALTER TABLE IF EXISTS public.whool_stock
    ADD CHECK (quantity>=0);


--
-- Data for Name: city; Type: TABLE DATA; Schema: public;
--

COPY public.city (id, name, created_at) FROM stdin;
1	Mérida	2024-10-18 22:12:25.032809
2	Caracas	2024-10-18 22:12:32.004716
3	Aragua	2024-10-18 22:12:39.087281
4	Trujillo	2024-10-18 22:12:46.658481
5	Zulia	2024-10-18 22:12:54.599651
6	Táchira	2024-10-18 22:13:00.133375
7	Falcón	2024-10-18 22:13:12.236486
8	Lara	2024-10-18 22:13:19.602549
9	Portuguesa	2024-10-18 22:13:28.722043
10	Barinas	2024-10-18 22:13:44.653823
11	Apure	2024-10-18 22:13:54.132789
12	Vargas	2024-10-18 22:14:00.957993
13	Cojedes	2024-10-18 22:14:07.0839
14	Sucre	2024-10-18 22:14:13.688207
15	Nueva Esparta	2024-10-18 22:14:23.133902
16	Anzoátegui	2024-10-18 22:14:43.729271
17	Monagas	2024-10-18 22:14:55.540461
18	Bolívar	2024-10-18 22:15:04.731634
19	Amazonas	2024-10-18 22:15:19.346217
20	Delta Amacuro	2024-10-18 22:15:31.792061
21	Carabobo	2024-10-18 22:15:41.276262
22	Guárico	2024-10-18 22:15:48.018878
23	Miranda	2024-10-18 22:15:53.275544
24	Yaracuy	2024-10-18 22:16:01.205574
\.

--
-- Data for Name: payment_method; Type: TABLE DATA; Schema: public;
--

COPY public.payment_method (id, name, created_at) FROM stdin;
1	Pago Móvil Bs	2024-10-18 22:17:25.173372
2	Efectivo $	2024-10-18 22:17:43.533078
\.

--
-- Data for Name: status; Type: TABLE DATA; Schema: public;
--

COPY public.status (id, name, created_at) FROM stdin;
1	Pendiente	2024-10-18 22:11:36.574146
2	Entregado	2024-10-18 22:11:49.143601
3	Cancelado	2024-10-18 22:11:57.712391
\.
    
END;