SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `mydb` ;
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Series`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Series` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Series` (
  `ID` INT NOT NULL,
  `NAME` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Lecture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Lecture` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Lecture` (
  `ID` INT NOT NULL,
  `NAME` VARCHAR(45) NULL,
  `SERIES` INT NOT NULL,
  PRIMARY KEY (`ID`),
  INDEX `SERIES_FK_idx` (`SERIES` ASC),
  CONSTRAINT `SERIES_FK`
    FOREIGN KEY (`SERIES`)
    REFERENCES `mydb`.`Series` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`VideoType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`VideoType` ;

CREATE TABLE IF NOT EXISTS `mydb`.`VideoType` (
  `ID` INT NOT NULL,
  `DESCRIPTION` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Video`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Video` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Video` (
  `ID` INT NOT NULL,
  `LECTURE` INT NOT NULL,
  `VIDEOTYPE` INT NOT NULL,
  `URL` VARCHAR(200) NULL,
  `LENGTH` DATETIME NULL,
  PRIMARY KEY (`ID`),
  INDEX `LECTURE_FK_idx` (`LECTURE` ASC),
  INDEX `VIDEOTYPE_FK_idx` (`VIDEOTYPE` ASC),
  CONSTRAINT `LECTURE_FK`
    FOREIGN KEY (`LECTURE`)
    REFERENCES `mydb`.`Lecture` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `VIDEOTYPE_FK`
    FOREIGN KEY (`VIDEOTYPE`)
    REFERENCES `mydb`.`VideoType` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Segment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Segment` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Segment` (
  `ID` INT NOT NULL,
  `VIDEO_ID` INT NULL,
  `START` TIME NULL,
  `BEST_INDEX` TIME NULL,
  PRIMARY KEY (`ID`),
  INDEX `VIDEO_FK_idx` (`VIDEO_ID` ASC),
  CONSTRAINT `VIDEO_FK`
    FOREIGN KEY (`VIDEO_ID`)
    REFERENCES `mydb`.`Video` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`OcrType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`OcrType` ;

CREATE TABLE IF NOT EXISTS `mydb`.`OcrType` (
  `ID` INT NOT NULL,
  `Description` VARCHAR(45) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`OcrResult`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`OcrResult` ;

CREATE TABLE IF NOT EXISTS `mydb`.`OcrResult` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `SEGMENT_ID` INT NULL,
  `TYPE` INT NULL,
  `CONTENT` VARCHAR(200) NULL,
  `KORD_LT_X` FLOAT NULL,
  `KORD_LT_Y` FLOAT NULL,
  `KORD_RB_X` FLOAT NULL,
  `KORD_RB_Y` FLOAT NULL,
  PRIMARY KEY (`ID`),
  INDEX `SEGMENT_FK_idx` (`SEGMENT_ID` ASC),
  INDEX `OCRTYPE_FK_idx` (`TYPE` ASC),
  CONSTRAINT `SEGMENT_FK`
    FOREIGN KEY (`SEGMENT_ID`)
    REFERENCES `mydb`.`Segment` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `OCRTYPE_FK`
    FOREIGN KEY (`TYPE`)
    REFERENCES `mydb`.`OcrType` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
