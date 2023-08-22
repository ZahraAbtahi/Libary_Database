--MainLibrary
INSERT INTO MainLibrary (name, address, phone, totalmember)
VALUES ('Main Library', '123 Library Street', 1234567890, 500);
--Sector
INSERT INTO Sector (sectorname)
VALUES (N'ورزش'), (N'پزشکی'), (N'مهندسی'), (N'هنر'), (N'ادبیات');
--moderator
INSERT INTO Moderator (moderatorid, name, family, phone, sectorname, IsBoss, password)
VALUES (1, 'John', 'Smith', 98765432, N'ورزش', 1, 123),
       (2, 'Emily', 'Johnson', 98765432, N'پزشکی', 0, 234),
       (3, 'David', 'Brown', 98765432, N'مهندسی', 0, 345),
       (4, 'Sophia', 'Lee', 98765432, N'هنر', 0, 456),
       (5, 'James', 'Wilson', 98765432, N'ادبیات', 0, 567);
--Member
INSERT INTO Member (memberid, name, family, phone, address, registerydate, photolink, password, barrowedBookNumber)
VALUES (1, 'Sarah', 'Davis', 98765432, '456 Member Street', '2023-01-01', 'link1.jpg',34, 3),
       (2, 'Michael', 'Anderson', 98765432, '789 Member Avenue', '2023-02-15', 'link2.jpg',45, 1),
       (3, 'Emma', 'Martinez', 98765432, '321 Member Road', '2023-03-10', 'link3.jpg',56, 4),
       (4, 'Ethan', 'Thomas', 98765432, '654 Member Lane', '2023-04-20', 'link4.jpg',67, 0),
       (5, 'Olivia', 'Garcia', 98765432, '987 Member Boulevard', '2023-05-05', 'link5.jpg',78, 2);
--Book
INSERT INTO Book (bookid, title, publicationname, publicationdate, IsReserved, IsAvailable, sectorname)
VALUES (1, 'Book1', 'Publisher1', '2023-01-01', 0, 1, N'ورزش'),
       (2, 'Book2', 'Publisher2', '2023-02-15', 1, 0, N'پزشکی'),
       (3, 'Book3', 'Publisher3', '2023-03-10', 0, 1, N'مهندسی'),
       (4, 'Book4', 'Publisher4', '2023-04-20', 1, 0, N'هنر'),
       (5, 'Book5', 'Publisher5', '2023-05-05', 0, 1, N'ادبیات');
--Author
INSERT INTO Author (Aid, name, family, bookid)
VALUES (1, 'Author1', 'Lastname1', 1),
       (2, 'Author2', 'Lastname2', 2),
       (3, 'Author3', 'Lastname3', 3),
       (4, 'Author4', 'Lastname4', 4),
       (5, 'Author5', 'Lastname5', 5);
--Translator
INSERT INTO Translator (tid, name, family, bookid)
VALUES (1, 'Translator1', 'Lastname1', 1),
       (2, 'Translator2', 'Lastname2', 2),
       (3, 'Translator3', 'Lastname3', 3),
       (4, 'Translator4', 'Lastname4', 4),
       (5, 'Translator5', 'Lastname5', 5);
--Borrow
INSERT INTO Borrow (barrowid, bookid, memberid, barrowdate, deliverydate, penalty, moderatorid, IsDelivered, approval) 
VALUES (10, 1, 1, '2023-01-02', '2023-01-05', 1, 5, 1, 1),
       (20, 2, 2, '2023-02-16', '2023-02-19', 1, 4, 1, 1),
       (30, 3, 3, '', '', 0, 3, 0, 1),
       (40, 4, 4, '', '', 0, 2, 0, 0),
       (50, 5, 5, '', '', 0, 1, 0, 1);
--Reservation
INSERT INTO Reservation (bookid, memberid, resDate)
VALUES (2, 1, '2023-12-03'),
       (3, 2, '2023-10-17'),
       (4, 3, '2023-08-12'),
       (5, 4, '2023-06-22'),
       (1, 5, '2023-05-06');



