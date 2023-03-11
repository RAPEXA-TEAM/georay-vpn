package request

type LoginRq struct {
	Email  string `form:"email" json:"email" binding:"required"`
	Pass   string `form:"pass" json:"pass" binding:"required"`
	Device string `form:"device" json:"device" binding:"required"`
	OS     string `form:"OS" json:"OS" binding:"required"`
}
