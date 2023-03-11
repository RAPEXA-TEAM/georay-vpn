package response

type LoginRp struct {
	Code int `json:"code"`
	Data struct {
		Device   string `json:"Device"`
		Os       string `json:"OS"`
		Days     string `json:"days"`
		Password string `json:"password"`
		Token    string `json:"token"`
		Username string `json:"username"`
	} `json:"data"`
	Openconnect []any `json:"openconnect"`
	Prices      struct {
		OneMonth   int `json:"1month"`
		TwoMonth   int `json:"2month"`
		ThreeMonth int `json:"3month"`
	} `json:"prices"`
	UpdateInfo struct {
		Force   string `json:"force"`
		Links   string `json:"links"`
		Version string `json:"version"`
	} `json:"update_info"`
	V2Ray []string `json:"v2ray"`
}
