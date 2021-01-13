package main

import (
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gorilla/mux"
)

func SetupCloseHandler() {
	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		Log.Println("\r- Ctrl+C pressed in Terminal")
		//DbClose()
		os.Exit(0)
	}()
}

func main() {
	error1, CONFIG_JSON := loadJson()
	if error1 != nil {
		Log.Fatal(error1)
		return
	}

	SetupCloseHandler()

	route := mux.NewRouter()
	s := route.PathPrefix("/api/ms/manage-notes").Subrouter()
	s.HandleFunc("/create", HandlerCreate).Methods("POST", "OPTIONS")

	Log.Println(CONFIG_JSON)
	server := CONFIG_JSON["server"].(map[string]interface{})
	readTimeout := int(server["readTimeout"].(float64))
	writeTimeout := int(server["writeTimeout"].(float64))
	idleTimeout := int(server["idleTimeout"].(float64))
	port := server["port"].(string)

	srv := &http.Server{
		ReadTimeout:  time.Duration(readTimeout) * time.Second,
		WriteTimeout: time.Duration(writeTimeout) * time.Second,
		IdleTimeout:  time.Duration(idleTimeout) * time.Second,
		Handler:      s,
		Addr:         ":" + port,
	}

	Log.Println("INICIANDO")
	Log.Fatal(srv.ListenAndServe())
}
