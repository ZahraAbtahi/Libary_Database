--1-a) 
SELECT * FROM MainLibrary
--1-b)
SELECT s.sectorname, b.bookid, b.title, b.publicationname, b.publicationdate
FROM Sector s
LEFT JOIN Book b ON s.sectorname = b.sectorname
ORDER BY s.sectorname, b.title;
--1-c)
SELECT b.bookid, b.title, b.publicationname, b.publicationdate
FROM Book b
JOIN Author a ON b.bookid = a.bookid
WHERE b.title LIKE '%[book_name]%' OR a.name LIKE '%[author_name]%'
ORDER BY b.title;
--2-a)
SELECT distinct ml.name AS LibraryName, ml.address AS LibraryAddress, ml.phone AS LibraryPhone, ml.totalmember AS TotalMembers
FROM MainLibrary ml
JOIN Member m ON m.password = [password]
WHERE m.memberid = [memberid];
--2-b) all books
SELECT s.sectorname, b.bookid, b.title, b.publicationname, b.publicationdate
FROM Sector s
JOIN Book b ON s.sectorname = b.sectorname
ORDER BY s.sectorname, b.title;
--2-b) just available books
SELECT s.sectorname, b.bookid, b.title, b.publicationname, b.publicationdate
FROM Sector s
JOIN Book b ON s.sectorname = b.sectorname
WHERE b.IsAvailable = 1
ORDER BY s.sectorname, b.title;
--2-c)
SELECT b.bookid, b.title, b.publicationname, b.publicationdate, b.IsReserved, b.IsAvailable, a.name AS author_name, a.family AS author_family, t.name AS translator_name, t.family AS translator_family, s.sectorname
FROM Book b
LEFT JOIN Author a ON b.bookid = a.bookid
LEFT JOIN Translator t ON b.bookid = t.bookid
JOIN Sector s ON b.sectorname = s.sectorname
WHERE b.title LIKE '%[book_name]%'
ORDER BY b.title;
--2-d)
SELECT m.memberid, m.name, m.family, m.phone, m.address, m.registerydate, m.photolink, b.bookid, b.title, b.publicationname, b.publicationdate, br.barrowdate, br.deliverydate, br.penalty
FROM Member m
LEFT JOIN Borrow br ON m.memberid = br.memberid
LEFT JOIN Book b ON br.bookid = b.bookid
WHERE m.password = [password];
--2-e)
SELECT m.memberid, m.name, m.family, COUNT(borrow.bookid) AS num_borrowed_books
FROM Member m
LEFT JOIN Borrow ON m.memberid = Borrow.memberid
GROUP BY m.memberid, m.name, m.family
HAVING COUNT(borrow.bookid) <=5;
--2-f)
INSERT INTO Reservation (bookid, memberid, resDate)
SELECT br.bookid, [memberid], CONVERT(DATE, GETDATE())
FROM Borrow br
WHERE br.memberid <> [memberid] AND br.bookid NOT IN (SELECT bookid FROM Reservation WHERE memberid = [memberid]);
--2-g)
SELECT b.memberid, m.name, m.family, b.bookid, b.borrowdate, b.deliverydate,
       CASE
           WHEN DATEDIFF(day, b.borrowdate, b.deliverydate) > 3 THEN 5000 * (DATEDIFF(day, b.borrowdate, b.deliverydate) - 3)
           ELSE 0
       END AS penalty
FROM Borrow b
INNER JOIN Member m ON b.memberid = m.memberid
WHERE b.IsDelivered = 1
      AND DATEDIFF(day, b.borrowdate, b.deliverydate) > 3;
-------------------
DECLARE @sector INT;
DECLARE @modid INT;

SET @sector = ( select sectorname
				from moderator
				where moderatorid = @modid);
-------------------
--3-a)
select [name],family,phone,sectorname,isboss
from moderator as m
where moderatorid = m.moderatorid
--3-b)
select *
from member;
select *
from book
where sectorname = @sector;
--3-c)
insert into member (name,family,phone,address,registerydate,photolink,barrowedBookNumber) values(name.get(),familt.get(),….);
delete from member 
where memberid = 12345;
CREATE PROC addbook
@modid int,@isdelete bit,@bookid int,@title varchar(20),
@publicationname varchar(50),@publicationdate char(10),
@sectorname nvarchar (6)
as
declare @tmp nvarchar(6);
set @tmp = (select sectorname
		from moderator
		where moderatorid = @modid);
if @tmp = @sectorname
begin
	if @isdelete = 1
	begin
		delete from book 
		where bookid = @bookid;
	end
	ELSE
	begin
		insert into book (bookid,title,publicationname,publicationdate,sectorname)
		values (@bookid,@title,@publicationname,@publicationdate,@sectorname);
	end
	print 'done'
end
else 
begin
	print 'action is not valid'
end
--3-d)
CREATE PROC approvaling
@modid int,
@barid int,
@act bit
as
declare @tmp nvarchar(6);
set @tmp = (select moderatorid
			from borrow
			where borrowid = @barid);
if @tmp = @modid
begin
	UPDATE borrow
	SET approval = @act
	WHERE borrowid = @barid;
	print 'done'
end
else 
begin
	print 'action is not valid'
end
--3-e)
delete from book
where year(CAST( GETDATE() AS Date ))- year(publicationdate)  >= 10 
	and bookid in (select bookid
			from borrow 
			where year(CAST( GETDATE() AS Date ))-1 = year(borrowdate)
			group by bookid
			having count(borrowid) < 5)
--4-a)
UPDATE moderator
SET isboss = 0;

with mod_bar_co as 
(select moderatorid as id,count(borrowid) as c
from borrow
where year(CAST( GETDATE() AS Date ))-1 = year(borrowdate)
group by moderatorid)

UPDATE moderator
SET isboss = 1
WHERE moderatorid = 
	(SELECT TOP 1 id
	from mod_bar_co
	where c = (	select max(c)
			from mod_bar_co));
--4-b
-- date is first day of year we will apply the query in each first day of year
-- xxxx/01/01
--4-c)
SELECT *
from moderator
--4-d)
select *
from book
select *
from member
--4-e)
select sectorname, count(borrowid) as count_borrow
from borrow,book
where IsDelivered = 1 and borrow.bookid = book.bookid
group by sectorname
order by count_borrow desc
--4-f)
select m.memberid, count(b.borrowid) as borrows
from member as m inner join borrow as b
on b.memberid = m.memberid
where IsDelivered = 1
group by m.memberid
order by borrows desc










