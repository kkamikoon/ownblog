INSERT INTO blog.categories(name, hidden) VALUES("TEST1", false); -- idx : 1 
INSERT INTO blog.categories(name, hidden) VALUES("TEST2", false); -- idx : 2

-- TEST 1 Category posts
INSERT INTO blog.posts(category_idx, title, abstract, filename, hidden) VALUES(1, "test1 - title1", "abstract", "test1_title1", false);
INSERT INTO blog.posts(category_idx, title, abstract, filename, hidden) VALUES(1, "test1 - title2", "abstract", "test1_title2", false);
INSERT INTO blog.posts(category_idx, title, abstract, filename, hidden) VALUES(1, "test1 - title3", "abstract", "test1_title3", false);

-- TEST 2 Category posts
INSERT INTO blog.posts(category_idx, title, abstract, filename, hidden) VALUES(2, "test2 - title1", "abstract", "test2_title1", false);
INSERT INTO blog.posts(category_idx, title, abstract, filename, hidden) VALUES(2, "test2 - title2", "abstract", "test2_title2", false);
INSERT INTO blog.posts(category_idx, title, abstract, filename, hidden) VALUES(2, "test2 - title3", "abstract", "test2_title3", false);