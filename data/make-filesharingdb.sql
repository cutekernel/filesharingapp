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
  FOREIGN KEY (fileID) REFERENCES File (FileID) ON DELETE CASCADE,
  FOREIGN KEY (ruleID) REFERENCES AccessControlRule (RuleID) ON DELETE CASCADE
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


