

----------Tables----------

--CentralLibary
create table CentralLibary
	(id int,
	name varchar (30),
	address varchar (200),
	phone int,
	totalmember int,
	primary key (id) 
	);
--Sector
create table Sector
	(sectorname nvarchar (6) check(sectorname in (N'ورزش',N'پزشکی',N'مهندسی',N'هنر',N'ادبیات')),
	libaryid int,
	primary key (sectorname),
	foreign key (libaryid) references CentralLibary (id) 
	);
--moderator
create table moderator
	(moderatorid int,
	name varchar(15),
	family varchar(15),
	phone int,
	sectorname nvarchar (6),
	IsBoss Bit,
	primary key (moderatorid),
	foreign key (sectorname) references Sector (sectorname)
	);
--Member
create table Member 
	(memberid int,
	name varchar(15),
	family varchar(15),
	phone int,
	address varchar (200),
	registerydate char(10),
	photolink varchar(100),
	barrowedBookNumber int CHECK(barrowedBookNumber < 6),
	primary key (memberid)
	);
--Book
create table Book 
	(bookid int,
	title varchar(20),
	publicationname varchar(50),
	publicationdate char(10),
	IsReserved Bit,
	IsAvailable Bit,
	sectorname nvarchar (6),
	primary key (bookid),
	foreign key (sectorname) references Sector (sectorname) 
	);
--Author
create table Author 
	(Aid int,
	name varchar(15),
	family varchar(15),
	bookid int,
	primary key (Aid),
	foreign key (bookid) references Book (bookid) 
	);
--Translator
create table Translator 
	(tid int not null,
	name varchar(15),
	family varchar(15),
	bookid int,
	primary key (tid),
	foreign key (bookid) references Book (bookid) 
	);
--Borrow
create table Borrow 
	(barrowid int,
	bookid int,
	memberid int,
	barrowdate char(10),
	deliverydate char(10),
	penalty int,
	moderatorid int,
	IsDelivered bit,
	primary key (barrowid),
	foreign key (bookid) references Book (bookid),
	foreign key (memberid) references Member (memberid),
	foreign key (moderatorid) references moderator (moderatorid)
	);
--Reservation
create table Reservation
	(bookid int unique,
	memberid int,
	resDate char(10),
	primary key (bookid, memberid),
	foreign key (bookid) references Book (bookid),
	foreign key (memberid) references Member (memberid)
	);

