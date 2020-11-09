package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"time"
)

func main() {
	formData := url.Values{
		"auth_user": {"dhcn"},
		"auth_pass": {"dhcn"},
		"accept":    {"Đăng nhập"},
	}
	URL := "http://172.16.0.1:8002/index.php?zone=iuh"
	isSend := false
	sleepTime := flag.Int("sleep", 5, "Time to sleep between call")
	flag.Parse()
	log.Println("Time sleep set to: " + fmt.Sprint(*sleepTime))
	for {
		resp, err := http.PostForm(URL, formData)
		if err != nil {
			log.Fatalln(err)
			isSend = true
			continue
		}

		defer resp.Body.Close()

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
			isSend = false
			continue
		}
		if !isSend {
			// log.Println("[+]You are connected!")
			log.Println("[!]Response: " + string(body))
			isSend = true
		}
		time.Sleep(time.Duration(*sleepTime) * time.Second)
	}
}
