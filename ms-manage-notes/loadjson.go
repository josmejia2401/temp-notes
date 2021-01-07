package main

import (
	"encoding/json"
	"io/ioutil"
	"os"
)

func loadJson() (error, map[string]interface{}) {
	jsonFile, err := os.Open("config.json")
	if err != nil {
		return err, nil
	}
	defer jsonFile.Close()
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var result map[string]interface{}
	json.Unmarshal([]byte(byteValue), &result)
	return nil, result
}
