package main

import (
	"georay/rest_api/login"
	"github.com/gin-gonic/gin"
)

var (
	router = gin.Default()
)

func main() {

	_ = router.SetTrustedProxies([]string{"localhost,192.168.0.1"})
	v1 := router.Group("/v1")

	login.AddLoginRoutes(v1)

	_ = router.Run(":5000")

}
