-- phpMyAdmin SQL Dump
-- version 2.8.1-Debian-1~dapper1
-- http://www.phpmyadmin.net
-- 
-- Host: localhost
-- Generato il: 14 Dic, 2007 at 12:51 AM
-- Versione MySQL: 5.0.22
-- Versione PHP: 4.4.2-1build1
-- 
-- Database: `openpursuit`
-- 

-- --------------------------------------------------------

-- 
-- Struttura della tabella `op_answers`
-- 

CREATE TABLE `op_answers` (
  `ID_ANSWER` int(10) NOT NULL auto_increment,
  `ID_QUESTION` int(10) unsigned NOT NULL,
  `right1` tinytext NOT NULL,
  `wrong1` tinytext character set utf8 NOT NULL,
  `wrong2` tinytext character set utf8 NOT NULL,
  `wrong3` tinytext character set utf8 NOT NULL,
  PRIMARY KEY  (`ID_ANSWER`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=36 ;

-- 
-- Dump dei dati per la tabella `op_answers`
-- 

INSERT INTO `op_answers` (`ID_ANSWER`, `ID_QUESTION`, `right1`, `wrong1`, `wrong2`, `wrong3`) VALUES (2, 444, '', 'w1', 'w2', 'w3'),
(3, 21, '', 'w1', 'w2', 'w3'),
(4, 22, '', 'w1', 'w2', 'w3'),
(5, 23, '', 'w1', 'w2', 'w3'),
(6, 24, 'r1w1', 'w1', 'w2', 'w3'),
(7, 25, 'r1w1', 'w1', 'w2', 'w3'),
(8, 26, 'r1w1', 'w1', 'w2', 'w3'),
(9, 27, 'r1w1', 'w1', 'w2', 'w3'),
(10, 28, 'r1w1', 'w1', 'w2', 'w3'),
(11, 29, 'r1w1', 'w1', 'w2', 'w3'),
(12, 30, 'r1w1', 'w1', 'w2', 'w3'),
(13, 31, 'r1w1', 'w1', 'w2', 'w3'),
(14, 32, 'r1w1', 'w1', 'w2', 'w3'),
(15, 33, 'r1w1', 'w1', 'w2', 'w3'),
(16, 34, 'r1w1', 'w1', 'w2', 'w3'),
(17, 35, 'r1w1', 'w1', 'w2', 'w3'),
(18, 36, 'r1w1', 'w1', 'w2', 'w3'),
(19, 37, 'r1w1', 'w1', 'w2', 'w3'),
(20, 38, 'r1w1', 'w1', 'w2', 'w3'),
(21, 39, 'r1w1', 'w1', 'w2', 'w3'),
(22, 40, 'r1', 'w1', 'w2', 'w3'),
(23, 41, 'r1', 'w1', 'w2', 'w3'),
(24, 42, 'r1', 'w1', 'w2', 'w3'),
(25, 43, 'r1', 'w1', 'w2', 'w3'),
(26, 44, 'r1', 'w1', 'w2', 'w3'),
(27, 45, 'r1', 'w1', 'w2', 'w3'),
(28, 46, 'r1', 'w1', 'w2', 'w3'),
(29, 47, 'r1', 'w1', 'w2', 'w3'),
(30, 48, 'r1', 'w1', 'w2', 'w3'),
(31, 49, 'r1', 'w1', 'w2', 'w3'),
(32, 50, 'r1', 'w1', 'w2', 'w3'),
(33, 51, 'r1', 'w1', 'w2', 'w3'),
(34, 52, '160', '256', '512', '16'),
(35, 53, 'r1', 'w1', 'w2', 'w3');

-- --------------------------------------------------------

-- 
-- Struttura della tabella `op_members`
-- 

CREATE TABLE `op_members` (
  `ID_MEMBER` mediumint(8) NOT NULL auto_increment,
  `memberName` varchar(80) character set utf8 NOT NULL,
  `dateRegistered` date NOT NULL,
  `password` varchar(64) character set utf8 NOT NULL,
  `posts` mediumint(8) unsigned NOT NULL,
  `quality` tinyint(4) unsigned NOT NULL,
  `emailAddress` tinytext character set utf8 NOT NULL,
  `realName` tinytext character set utf8 NOT NULL,
  `location` tinytext character set utf8 NOT NULL,
  `gender` tinyint(4) unsigned NOT NULL,
  `birthdate` date NOT NULL,
  `websiteUrl` tinytext character set utf8 NOT NULL,
  `personalText` mediumtext character set utf8 NOT NULL,
  `passwordSalt` varchar(5) character set utf8 NOT NULL,
  `personalIcon` tinytext character set utf8 NOT NULL,
  `score` int(10) NOT NULL,
  `active` set('0','1') NOT NULL,
  PRIMARY KEY  (`ID_MEMBER`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

-- 
-- Dump dei dati per la tabella `op_members`
-- 

INSERT INTO `op_members` (`ID_MEMBER`, `memberName`, `dateRegistered`, `password`, `posts`, `quality`, `emailAddress`, `realName`, `location`, `gender`, `birthdate`, `websiteUrl`, `personalText`, `passwordSalt`, `personalIcon`, `score`, `active`) VALUES (1, 'prova', '2007-12-11', 'prova', 0, 0, '', 'prova', '', 0, '0000-00-00', '', '', '', '', 0, ''),
(2, 'prova2', '2007-12-11', '280093f2cfe260a00ee1bb06f96584de', 0, 0, '', '', '', 0, '0000-00-00', '', '', '', '', 0, ''),
(3, 'prova3', '0000-00-00', 'd6f21258c28da5af4831d73e47aecc1e', 0, 0, 'webmaster@frascati1.org', 'Lorenzo', 'grotta', 0, '0000-00-00', 'wurl', 'ptext', '', 'picon', 0, '1'),
(4, 'prova4', '0000-00-00', '1775223eeeb515c77a7f201db191af09', 0, 0, 'email', 'realname', 'loca', 0, '0000-00-00', 'web', 'perstest', '', 'picon', 0, '1'),
(6, '', '0000-00-00', 'd41d8cd98f00b204e9800998ecf8427e', 0, 0, '', '', '', 0, '0000-00-00', '', '', '', '', 0, '1'),
(7, '', '0000-00-00', 'd41d8cd98f00b204e9800998ecf8427e', 0, 0, '', '', '', 0, '0000-00-00', '', '', '', '', 0, '1'),
(8, 'Loose Dog', '2007-12-12', '0ceb5024f1811a21f506ff58fb7b3df1', 0, 0, 'bzzauz@gmail.com', 'Fabio', 'Monte Merda', 0, '0000-00-00', 'bzzauz.com', '', '', '', 0, '1'),
(9, 'prova10', '2007-12-12', 'e6455e15f34299bed16f4f5ab1c2e093', 0, 0, 'hhhh', 'GGG', 'grotta', 0, '0000-00-00', '', '', '', '', 0, '1');

-- --------------------------------------------------------

-- 
-- Struttura della tabella `op_questions`
-- 

CREATE TABLE `op_questions` (
  `ID_QUESTION` int(10) NOT NULL auto_increment,
  `ID_MEMBER` mediumint(8) unsigned NOT NULL,
  `question` tinytext character set utf8 NOT NULL,
  `creationDate` date NOT NULL,
  `difficulty` tinytext NOT NULL,
  `score` tinytext NOT NULL,
  PRIMARY KEY  (`ID_QUESTION`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=54 ;

-- 
-- Dump dei dati per la tabella `op_questions`
-- 

INSERT INTO `op_questions` (`ID_QUESTION`, `ID_MEMBER`, `question`, `creationDate`, `difficulty`, `score`) VALUES (4, 1, 'q1', '0000-00-00', '3', ''),
(5, 3, 'qqqqq', '0000-00-00', '1', ''),
(6, 0, 'q1', '0000-00-00', '4', ''),
(7, 0, 'q1', '0000-00-00', '1', ''),
(8, 0, 'q1', '0000-00-00', '1', ''),
(9, 2393337, 'q1', '0000-00-00', '2', ''),
(10, 0, 'q1', '0000-00-00', '2', ''),
(11, 2, 'q1', '0000-00-00', '3', ''),
(12, 2, 'q1', '0000-00-00', '1', ''),
(13, 2, 'q1', '0000-00-00', '', ''),
(14, 2, 'q', '0000-00-00', '', ''),
(15, 2, 'q', '0000-00-00', '', ''),
(16, 2, 'q', '0000-00-00', '', ''),
(17, 2, 'q1', '0000-00-00', '3', ''),
(18, 2, 'q1', '0000-00-00', '', ''),
(19, 2, 'q1', '0000-00-00', '3', ''),
(20, 2, 'q1', '0000-00-00', '3', ''),
(21, 2, 'q1', '0000-00-00', '3', ''),
(22, 2, 'q1', '2007-12-12', '3', ''),
(23, 2, 'q1', '2007-12-12', '3', ''),
(24, 2, 'question1', '2007-12-12', '3', ''),
(25, 2, 'question1', '2007-12-12', '3', ''),
(26, 2, 'question1', '2007-12-12', '3', ''),
(27, 2, 'question1', '2007-12-12', '3', ''),
(28, 2, 'question1', '2007-12-12', '3', ''),
(29, 2, 'question1', '2007-12-12', '3', ''),
(30, 2, 'question1', '2007-12-12', '3', ''),
(31, 2, 'question1', '2007-12-12', '3', ''),
(32, 2, 'question1', '2007-12-12', '3', ''),
(33, 2, 'question1', '2007-12-12', '3', ''),
(34, 2, 'question1', '2007-12-12', '3', ''),
(35, 2, 'question1', '2007-12-12', '3', ''),
(36, 2, 'question1', '2007-12-12', '3', ''),
(37, 2, 'question1', '2007-12-12', '3', ''),
(38, 2, 'question1', '2007-12-12', '3', ''),
(39, 2, 'question1', '2007-12-12', '3', ''),
(40, 2, 'q1', '2007-12-12', '3', ''),
(41, 2, 'q1', '2007-12-12', '3', ''),
(42, 2, 'q1', '2007-12-12', '3', ''),
(43, 2, 'q1', '2007-12-12', '3', ''),
(44, 2, 'quest1', '2007-12-12', '3', ''),
(45, 2, 'quest1', '2007-12-12', '3', ''),
(46, 2, 'quest1', '2007-12-12', '3', ''),
(47, 2, 'quest1', '2007-12-12', '3', ''),
(48, 2, 'quest1', '2007-12-12', '3', ''),
(49, 2, 'quest1', '2007-12-12', '3', ''),
(50, 2, 'quest1', '2007-12-12', '3', ''),
(51, 2, 'quest1', '2007-12-12', '3', ''),
(52, 9, 'di quanti bit e'' l''hash  sha1?', '2007-12-12', '2', ''),
(53, 2, 'q1', '2007-12-13', '1', '');

-- --------------------------------------------------------

-- 
-- Struttura della tabella `op_sessions`
-- 

CREATE TABLE `op_sessions` (
  `uid` char(32) NOT NULL,
  `ID_MEMBER` int(10) unsigned NOT NULL,
  `creation_date` int(10) unsigned NOT NULL,
  KEY `uid` (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- 
-- Dump dei dati per la tabella `op_sessions`
-- 

INSERT INTO `op_sessions` (`uid`, `ID_MEMBER`, `creation_date`) VALUES ('88738483475908b8a894d84427ff5906', 2, 1197558976);

-- --------------------------------------------------------

-- 
-- Struttura della tabella `op_tags`
-- 

CREATE TABLE `op_tags` (
  `ID_TAG` mediumint(8) unsigned NOT NULL auto_increment,
  `tag` tinytext character set utf8 NOT NULL,
  `count` tinyint(4) NOT NULL,
  KEY `ID_TAG` (`ID_TAG`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- 
-- Dump dei dati per la tabella `op_tags`
-- 

INSERT INTO `op_tags` (`ID_TAG`, `tag`, `count`) VALUES (1, 'prova5', 1),
(2, 'prova6', 4),
(3, 'security networking', 10),
(4, 'prova10', 5);

-- --------------------------------------------------------

-- 
-- Struttura della tabella `op_tags_links`
-- 

CREATE TABLE `op_tags_links` (
  `ID` int(11) NOT NULL auto_increment,
  `ID_TAG` mediumint(8) unsigned NOT NULL,
  `ID_QUESTION` mediumint(8) unsigned NOT NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

-- 
-- Dump dei dati per la tabella `op_tags_links`
-- 

INSERT INTO `op_tags_links` (`ID`, `ID_TAG`, `ID_QUESTION`) VALUES (1, 1, 50),
(2, 2, 1),
(3, 1, 51),
(4, 2, 51),
(5, 3, 52),
(6, 2, 53);
