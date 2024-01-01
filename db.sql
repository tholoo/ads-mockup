CREATE TABLE IF NOT EXISTS advertiser (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    clicks INT DEFAULT 0 CHECK (clicks >= 0),
    views INT DEFAULT 0 CHECK (views >= 0)
);

CREATE TABLE IF NOT EXISTS ad (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    clicks INT DEFAULT 0 CHECK (clicks >= 0),
    views INT DEFAULT 0 CHECK (views >= 0),
    img_url TEXT,
    link TEXT,
    advertiser_id INT,
    FOREIGN KEY (advertiser_id) REFERENCES advertiser(id)
);

