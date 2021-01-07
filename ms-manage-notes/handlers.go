package main

import (
	"encoding/json"
	"net/http"
)

func HandlerCreate(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Expose-Headers", "Authorization")
	w.Header().Set("Access-Control-Allow-Methods", "*")
	w.Header().Set("Access-Control-Allow-Headers", "*")
	if r.Method == "OPTIONS" {
		return
	}
	var body interface{}
	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		Log.Println(err)
		w.WriteHeader(400)
		return
	}
	w.WriteHeader(200)
	json.NewEncoder(w).Encode(body)
}
