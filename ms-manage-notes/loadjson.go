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
	/*var result map[string]interface{}
	json.Unmarshal([]byte(byteValue), &result)
	return nil, result*/
	var f interface{}
	err = json.Unmarshal([]byte(byteValue), &f)
	if err != nil {
		return err, nil
	}
	m := f.(map[string]interface{})
	//fmt.Println("Type = %v", m)
	return nil, m
}
