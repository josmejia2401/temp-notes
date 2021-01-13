package main

import (
	"encoding/json"
	"net/http"
	"time"
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
	body := TempNoteStruct{}
	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		Log.Println(err)
		w.WriteHeader(400)
		return
	}
	err, result := DbGetByOwner(body.OwnerUsername)
	if err != nil {
		Log.Println(err)
		w.WriteHeader(500)
		return
	}
	if result != nil {
		Log.Println("El usuario ya existe", body.OwnerUsername)
		w.WriteHeader(500)
		json.NewEncoder(w).Encode("No se pudo crear la nota.")
		return
	}
	body.CreatedAt = time.Now().UTC()
	body.UpdatedAt = time.Now().UTC()
	err, result = DbInsert(&body)
	if err != nil {
		Log.Println(err)
		w.WriteHeader(500)
		return
	}
	w.WriteHeader(200)
	json.NewEncoder(w).Encode(result)
}
