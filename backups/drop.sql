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