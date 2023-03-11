package database

import (
	"fmt"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"sync"
)

var dbLock = &sync.Mutex{}
var DB *gorm.DB

func GetDB() *gorm.DB {
	var err error
	if DB == nil {

		dbLock.Lock()
		defer dbLock.Unlock()

		if DB == nil {

			DB, err = gorm.Open(mysql.Open("root:@Gold1380@tcp(localhost:3306)/web3game?charset=utf8&parseTime=True"))
			if err != nil {
				panic(any(fmt.Errorf("connect db fail: %w", err)))
			} else {
				//database migration
				//if !DB.Migrator().HasTable(&entity.Game{}) {
				//	_ = DB.Migrator().CreateTable(&entity.Game{})
				//}
				//if !DB.Migrator().HasTable(&entity.Nonce{}) {
				//	_ = DB.Migrator().CreateTable(&entity.Nonce{})
				//}
			}

		}

	}
	return DB
}
