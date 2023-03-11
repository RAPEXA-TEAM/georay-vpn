package entity

type Users []User

type User struct {
	User     string `json:"user"`
	Password string `json:"password"`
	Phone    int    `json:"status"`
	Email    int    `json:"email"`
	Days     int    `json:"days"`
	Token    int    `json:"token"`
	Verified int    `json:"verified"`
}
