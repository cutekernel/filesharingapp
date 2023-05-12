create database filesharingdb;
use filesharingdb;


-- Drop tables if they exist
DROP TABLE IF EXISTS AccessControlRule;
DROP TABLE IF EXISTS FileFormat;
DROP TABLE IF EXISTS FileVersion;
DROP TABLE IF EXISTS File;
DROP TABLE IF EXISTS FileCategory;
DROP TABLE IF EXISTS Notification;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS UserGroup;
DROP TABLE IF EXISTS UserActivity;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS user_receives_notification;
DROP TABLE IF EXISTS user_belongs_userGroup;
DROP TABLE IF EXISTS file_has_ac_rule;
DROP TABLE IF EXISTS file_has_tag;
DROP TABLE IF EXISTS file_has_filecategory;


-- Create User table
CREATE TABLE User (
UserID INT NOT NULL AUTO_INCREMENT, -- unique identifier for each user
Username VARCHAR(50) UNIQUE NOT NULL, -- username should be unique and not null
Email VARCHAR(255) UNIQUE NOT NULL, -- email should be unique and not null
Password VARCHAR(255) NOT NULL, -- password should not be null
RegistrationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- registration date is set to current timestamp by default
LastLoginDate DATETIME, -- last login date may be null if user has not logged in yet
UserProfile TEXT, -- user profile is a text field that may contain large amounts of data
PRIMARY KEY (UserID) -- set UserID as primary key
);

-- Create FileCategory table
CREATE TABLE FileCategory (
CategoryID INT NOT NULL AUTO_INCREMENT,
CategoryName VARCHAR(50) UNIQUE NOT NULL,
CategoryDescription TEXT,
PRIMARY KEY (CategoryID)
-- The CategoryID attribute is the primary key of the table
-- The CategoryName attribute is unique to ensure there are no duplicate categories
);


-- Create AccessControlRule table with RuleID as the primary key, which is an auto-incrementing integer to ensure uniqueness
CREATE TABLE AccessControlRule (
RuleID INT NOT NULL AUTO_INCREMENT,
RuleName VARCHAR(50) UNIQUE NOT NULL, -- RuleName should be unique to ensure each rule has a distinct name
RuleDescription TEXT,
AccessLevel VARCHAR(20) NOT NULL,
UserID INT NOT NULL,
FOREIGN KEY (UserID) REFERENCES User (UserID) ON DELETE CASCADE,
PRIMARY KEY (RuleID)
);


-- Create UserActivity table with ActivityID as the primary key, which is an auto-incrementing integer to ensure uniqueness
CREATE TABLE UserActivity (
ActivityID INT NOT NULL AUTO_INCREMENT,
FileID INT NOT NULL, -- FileID is a foreign key referencing the File table to ensure data consistency
ActivityType VARCHAR(50) NOT NULL,
ActivityDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- ActivityDate defaults to the current timestamp to ensure accurate recording of activity
UserID INT NOT NULL,
PRIMARY KEY (ActivityID),
FOREIGN KEY (UserID) REFERENCES User (UserID) ON DELETE CASCADE -- FileID references the File table and cascade deletion is used to maintain referential integrity
);


-- Create FileVersion table with columns for tracking file versions and related file ID.
CREATE TABLE FileVersion (
VersionID INT NOT NULL AUTO_INCREMENT, -- Unique version ID
VersionNumber INT NOT NULL, -- Version number for tracking purposes
VersionDescription TEXT, -- Description of changes made in the version
VersionSize INT NOT NULL, -- Size of the version in bytes
VersionUploadDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the version was uploaded
PRIMARY KEY (VersionID)
);


-- Create FileFormat table to store the available formats for files.
CREATE TABLE FileFormat (
FormatID INT NOT NULL AUTO_INCREMENT, -- Unique format ID
FormatName VARCHAR(50) UNIQUE NOT NULL, -- Name of the file format
FormatDescription TEXT, -- Description of the file format
PRIMARY KEY (FormatID)
);

-- Create File table
CREATE TABLE File (
FileID INT NOT NULL AUTO_INCREMENT,
FileName VARCHAR(255) NOT NULL,
FileSize INT NOT NULL,
UploadDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
LatestVersionID INT,
OwnerID INT,
UserID INT NOT NULL,
FormatID INT,
PRIMARY KEY (FileID),
FOREIGN KEY (FormatID) REFERENCES FileFormat (FormatID) ON DELETE CASCADE,
FOREIGN KEY (UserID) REFERENCES User (UserID) ON DELETE CASCADE,
FOREIGN KEY (LatestVersionID) REFERENCES FileVersion (VersionID) ON DELETE SET NULL
);



-- Create Notification table
-- Notification table: NotificationID is the primary key to uniquely identify each notification. NotificationType and NotificationMessage are required columns to describe the type and message of the notification. NotificationDate is the timestamp for when the notification was created.
CREATE TABLE Notification (
  NotificationID INT NOT NULL AUTO_INCREMENT,
  NotificationType VARCHAR(50) NOT NULL,
  NotificationMessage TEXT NOT NULL,
  NotificationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (NotificationID)
);


-- Create UserGroup table
-- UserGroup table: GroupID is the primary key to uniquely identify each user group. GroupName is a required column to give a name to the group that is unique. GroupDescription is an optional field to provide a description of the user group.
CREATE TABLE UserGroup (
  GroupID INT NOT NULL AUTO_INCREMENT,
  GroupName VARCHAR(50) UNIQUE NOT NULL,
  GroupDescription TEXT,
  PRIMARY KEY (GroupID)
);


-- Create Tag table
-- Tag table: TagID is the primary key to uniquely identify each tag. TagName is a required column to give a name to the tag that is unique. TagDescription is an optional field to provide a description of the tag.
CREATE TABLE Tag (
  TagID INT NOT NULL AUTO_INCREMENT,
  TagName VARCHAR(50) UNIQUE NOT NULL,
  TagDescription TEXT,
  PRIMARY KEY (TagID)
);



-- Missing Tables
CREATE TABLE user_receives_notification (
  UserID INT NOT NULL,
  notificationID INT NOT NULL,
  PRIMARY KEY (UserID, notificationID),
  FOREIGN KEY (UserID) REFERENCES User (UserID) ON DELETE CASCADE,
  FOREIGN KEY (notificationID) REFERENCES Notification (notificationID) ON DELETE CASCADE
);


CREATE TABLE user_belongs_userGroup (
  UserID INT NOT NULL,
  groupID INT NOT NULL,
  PRIMARY KEY (UserID, groupID),
  FOREIGN KEY (UserID) REFERENCES User (UserID) ON DELETE CASCADE,
  FOREIGN KEY (groupID) REFERENCES UserGroup (groupID) ON DELETE CASCADE
);


CREATE TABLE file_has_ac_rule (
  fileID INT NOT NULL,
  ruleID INT NOT NULL,
  PRIMARY KEY (fileID, ruleID),
  FOREIGN KEY (fileID) REFERENCES File (fileID) ON DELETE CASCADE,
  FOREIGN KEY (ruleID) REFERENCES AccessControlRule (ruleID) ON DELETE CASCADE
);


CREATE TABLE file_has_tag (
  fileID INT NOT NULL,
  tagID INT NOT NULL,
  PRIMARY KEY (fileID, tagID),
  FOREIGN KEY (fileID) REFERENCES File (fileID) ON DELETE CASCADE,
  FOREIGN KEY (tagID) REFERENCES Tag (tagID) ON DELETE CASCADE
);


CREATE TABLE file_has_filecategory (
  fileID INT NOT NULL,
  categoryID INT NOT NULL,
  PRIMARY KEY (fileID, categoryID),
  FOREIGN KEY (fileID) REFERENCES File (fileID) ON DELETE CASCADE,
  FOREIGN KEY (categoryID) REFERENCES FileCategory (categoryID) ON DELETE CASCADE
);




INSERT INTO User (Username, Email, Password, RegistrationDate, LastLoginDate, UserProfile)
VALUES
    ('johndoe', 'johndoe@example.com', 'P@ssw0rd1', NOW(), NOW(), 'John Doe is a software engineer who enjoys hiking and playing guitar in his free time.'),
    ('janedoe', 'janedoe@example.com', 'P@ssw0rd2', NOW(), NOW(), 'Jane Doe is a graphic designer who loves to travel and try new foods.'),
    ('bobsmith', 'bobsmith@example.com', 'P@ssw0rd3', NOW(), NOW(), 'Bob Smith is a marketing specialist who enjoys playing basketball and watching movies.'),
    ('sarajohnson', 'sarajohnson@example.com', 'P@ssw0rd4', NOW(), NOW(), 'Sara Johnson is a teacher who enjoys reading and practicing yoga.'),
    ('mikejones', 'mikejones@example.com', 'P@ssw0rd5', NOW(), NOW(), 'Mike Jones is a software developer who loves to play video games and go hiking.'),
    ('jennylee', 'jennylee@example.com', 'P@ssw0rd6', NOW(), NOW(), 'Jenny Lee is a musician who enjoys playing the guitar and singing in her free time.'),
    ('tomhanks', 'tomhanks@example.com', 'P@ssw0rd7', NOW(), NOW(), 'Tom Hanks is an actor who loves to play golf and travel around the world.'),
    ('jenniferlopez', 'jenniferlopez@example.com', 'P@ssw0rd8', NOW(), NOW(), 'Jennifer Lopez is a singer who enjoys dancing and spending time with her family.'),
    ('willsmith', 'willsmith@example.com', 'P@ssw0rd9', NOW(), NOW(), 'Will Smith is an actor who loves to play basketball and read motivational books.'),
    ('angelinajolie', 'angelinajolie@example.com', 'P@ssw0rd10', NOW(), NOW(), 'Angelina Jolie is an actress who enjoys humanitarian work and spending time with her children.');


INSERT INTO FileFormat (FormatName, FormatDescription)
VALUES
    ('PDF', 'Portable Document Format'),
    ('DOCX', 'Microsoft Word Document'),
    ('XLSX', 'Microsoft Excel Spreadsheet'),
    ('PPTX', 'Microsoft PowerPoint Presentation'),
    ('JPG', 'Joint Photographic Experts Group Image'),
    ('PNG', 'Portable Network Graphics Image'),
    ('MP3', 'MPEG Audio Layer III File'),
    ('TXT', 'Plain Text File'),
    ('PSD', 'Adobe Photoshop Document'),
    ('PY', 'Python Script File');

INSERT INTO FileVersion (VersionNumber, VersionDescription, VersionSize, VersionUploadDate)
VALUES
  (1, 'Initial version', 1048576, '2022-01-01 12:00:00'),
  (2, 'Added new feature', 2097152, '2022-01-02 13:30:00'),
  (3, 'Bug fixes', 1572864, '2022-01-04 09:45:00'),
  (4, 'Performance improvements', 3145728, '2022-01-06 16:20:00'),
  (5, 'Refactored code', 2621440, '2022-01-08 10:10:00'),
  (6, 'New UI design', 4194304, '2022-01-10 14:15:00'),
  (7, 'Improved user experience', 3670016, '2022-01-12 11:30:00'),
  (8, 'Added support for new file formats', 5242880, '2022-01-14 15:40:00'),
  (9, 'Bug fixes and minor improvements', 4718592, '2022-01-16 09:20:00'),
  (10, 'Security enhancements', 5767168, '2022-01-18 12:50:00');



INSERT INTO File (FileName, FileSize, UploadDate, LatestVersionID, OwnerID, UserID, FormatID)
VALUES
('file1.txt', 1024, '2023-05-09 12:00:00', 1, 1, 2, 1),
('file2.docx', 2048, '2023-05-08 14:30:00', 2, 1, 3, 2),
('file3.jpg', 5120, '2023-05-07 16:45:00', 3, 2, 4, 3),
('file4.pdf', 4096, '2023-05-06 10:15:00', 4, 2, 5, 1),
('file5.mp3', 1048576, '2023-05-05 09:00:00', 5, 3, 6, 4),
('file6.pptx', 3072, '2023-05-04 11:30:00', 6, 3, 7, 2),
('file7.png', 2048, '2023-05-03 14:20:00', 7, 4, 8, 3),
('file8.xlsx', 6144, '2023-05-02 16:00:00', 8, 4, 9, 2),
('file9.txt', 256, '2023-05-01 10:10:00', 9, 5, 10, 1),
('file10.doc', 10240, '2023-04-30 09:30:00', 10, 5, 1, 2);





INSERT INTO FileCategory (CategoryName, CategoryDescription)
VALUES
    ('Documents', 'Files related to textual documents such as .docx, .pdf, .txt, etc.'),
    ('Images', 'Files related to digital images such as .jpg, .png, .bmp, etc.'),
    ('Music', 'Files related to audio content such as .mp3, .wav, .aac, etc.'),
    ('Videos', 'Files related to video content such as .mp4, .avi, .mov, etc.'),
    ('Spreadsheets', 'Files related to tabular data such as .xlsx, .csv, .tsv, etc.'),
    ('Presentations', 'Files related to slide-based presentations such as .pptx, .key, .odp, etc.'),
    ('Text', 'Files related to plain text content such as .txt, .md, .html, etc.'),
    ('PDF', 'Files related to the portable document format (.pdf)'),
    ('Code', 'Files related to programming code such as .py, .cpp, .java, etc.'),
    ('Design', 'Files related to digital design content such as .psd, .ai, .svg, etc.');


INSERT INTO AccessControlRule (RuleName, RuleDescription, AccessLevel, UserID)
VALUES
    ('Admin Access', 'Full access for system administrators', 'admin', 1),
    ('Manager Access', 'Access for department managers', 'manager', 2),
    ('Supervisor Access', 'Access for team supervisors', 'supervisor', 3),
    ('Employee Access', 'Access for regular employees', 'employee', 4),
    ('ReadOnly Access', 'Read-only access for stakeholders', 'readonly', 5),
    ('Sales Access', 'Access for sales team', 'sales', 6),
    ('Marketing Access', 'Access for marketing team', 'marketing', 7),
    ('Engineering Access', 'Access for engineering team', 'engineering', 8),
    ('Finance Access', 'Access for finance team', 'finance', 9),
    ('IT Access', 'Access for IT team', 'it', 10);


INSERT INTO UserActivity (FileID, ActivityType, UserID) VALUES
(1, 'Downloaded', 1),
(2, 'Uploaded', 2),
(3, 'Viewed', 3),
(4, 'Downloaded', 4),
(5, 'Uploaded', 5),
(6, 'Viewed', 1),
(7, 'Downloaded', 2),
(8, 'Uploaded', 3),
(9, 'Viewed', 4),
(10, 'Downloaded', 5);





INSERT INTO Notification (NotificationType, NotificationMessage)
VALUES 
  ('New file upload', 'A new file has been uploaded.'),
  ('File deleted', 'A file has been deleted.'),
  ('Version uploaded', 'A new version of a file has been uploaded.'),
  ('User added', 'A new user has been added.'),
  ('User deleted', 'A user has been deleted.'),
  ('Access control rule added', 'A new access control rule has been added.'),
  ('Access control rule deleted', 'An access control rule has been deleted.'),
  ('User activity recorded', 'A user activity has been recorded.'),
  ('File format added', 'A new file format has been added.'),
  ('File format deleted', 'A file format has been deleted.');

INSERT INTO UserGroup (GroupName, GroupDescription)
VALUES
  ('Marketing Team', 'Group responsible for promoting and advertising the company\'s products and services'),
  ('Sales Team', 'Group responsible for selling the company\'s products and services'),
  ('Product Development Team', 'Group responsible for developing and improving the company\'s products and services'),
  ('Human Resources Team', 'Group responsible for managing the company\'s personnel'),
  ('Finance Team', 'Group responsible for managing the company\'s financial resources'),
  ('Customer Support Team', 'Group responsible for assisting customers with their inquiries and concerns'),
  ('IT Team', 'Group responsible for managing the company\'s information technology infrastructure'),
  ('Legal Team', 'Group responsible for ensuring the company\'s compliance with legal and regulatory requirements'),
  ('Research and Development Team', 'Group responsible for conducting research and development to improve the company\'s products and services'),
  ('Operations Team', 'Group responsible for managing the company\'s day-to-day operations');

INSERT INTO Tag (TagName, TagDescription)
VALUES 
    ('Technology', 'Files related to technology'),
    ('Sports', 'Files related to sports and fitness'),
    ('Food', 'Files related to cooking and food'),
    ('Travel', 'Files related to travel and exploration'),
    ('Art', 'Files related to art and creativity'),
    ('Music', 'Files related to music and entertainment'),
    ('Fashion', 'Files related to fashion and style'),
    ('Education', 'Files related to education and learning'),
    ('Business', 'Files related to business and finance'),
    ('Health', 'Files related to health and wellness');


INSERT INTO user_receives_notification (userID, notificationID) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7),
(4, 8),
(5, 9),
(5, 10);


INSERT INTO user_belongs_userGroup (userID, groupID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10);

INSERT INTO file_has_ac_rule (fileID, ruleID) VALUES
  (1, 4),
  (1, 7),
  (2, 3),
  (2, 6),
  (3, 1),
  (3, 9),
  (4, 2),
  (4, 5),
  (5, 8),
  (5, 10);

INSERT INTO file_has_tag (fileID, tagID)
VALUES
  (1, 4),
  (1, 7),
  (2, 3),
  (2, 6),
  (3, 1),
  (3, 9),
  (4, 2),
  (4, 5),
  (5, 8),
  (5, 10);

INSERT INTO file_has_filecategory (fileID, categoryID)
VALUES 
  (1, 1),
  (1, 3),
  (2, 2),
  (3, 1),
  (3, 2),
  (4, 3),
  (5, 1),
  (6, 2),
  (7, 3),
  (8, 1);

