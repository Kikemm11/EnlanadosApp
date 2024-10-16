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
    product_id integer NOT NULL,
    product_type_id integer NOT NULL,
    description text NOT NULL,
    price real,
    added_price real DEFAULT 0.0,
    credit real DEFAULT 0.0,
    payment_method_id integer NOT NULL,
    estimated_date date NOT NULL,
    status_id integer NOT NULL,
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
    ADD CONSTRAINT product_fk FOREIGN KEY (product_id)
    REFERENCES public.product (id) MATCH SIMPLE
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


-- Add check constraints

ALTER TABLE IF EXISTS public.product_type
    ADD CHECK (price>0.0);

ALTER TABLE IF EXISTS public."order"
    ADD CHECK (added_price>=0.0);

ALTER TABLE IF EXISTS public."order"
    ADD CHECK (credit>=0.0);

ALTER TABLE IF EXISTS public.whool_stock
    ADD CHECK (quantity>=0);
    
END;