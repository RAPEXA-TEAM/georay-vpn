package database

import "gorm.io/gorm"

func GetTableUsers() *gorm.DB { return GetDB().Table("users") }
func GetTableTxIds() *gorm.DB { return GetDB().Table("txids") }

// FIXME
func GetTableSellers() *gorm.DB { return GetDB().Table("sellers") }
