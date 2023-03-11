package login

import (
	"georay/database"
	"georay/helper"
	"georay/models/entity"
	"georay/models/request"
	"github.com/gin-gonic/gin"
)

func AddLoginRoutes(group *gin.RouterGroup) {

	//localhost:5000/v1/auth/login
	authGroup := group.Group("/auth")

	authGroup.POST("/login", func(c *gin.Context) {
		var err error

		var rq request.LoginRq
		if err = c.ShouldBindJSON(&rq); err != nil {
			helper.SendErrorResponse(c, helper.REQURED_PARAMETERS_IS_NOT_SET)
			return
		}

		var rp = entity.User{}
		query := database.GetTableUsers().
			Where("email = ?", rq.Email).
			Where("password = ?", rq.Pass).
			First(&rp)
		err = query.Error

		if err != nil {
			helper.SendErrorResponse(c, helper.UNKNOWN_ERROR)
			return
		} else {
			helper.SendSuccessResponse(c, rp, nil)
		}

	})

	authGroup.POST("/signup", func(c *gin.Context) {

	})

}
