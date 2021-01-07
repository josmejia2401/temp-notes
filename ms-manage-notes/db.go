package main

import (
	"context"
	"errors"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	DB_COL = "temp_notes"
)

var dbClient *mongo.Client = DbClient()
var dbDb *mongo.Database = Dbdb()

func DbClient() *mongo.Client {
	error1, CONFIG_JSON := loadJson()
	if error1 != nil {
		panic(error1)
	}
	db := CONFIG_JSON["db"].(map[string]interface{})
	uri := db["uri"].(string)
	maxPoolSize := db["maxPoolSize"].(uint64)
	appName := db["appName"].(string)
	timeOut := db["timeOut"].(int)

	clientOptions := options.Client().ApplyURI(uri)
	clientOptions.SetMaxPoolSize(maxPoolSize)
	clientOptions.SetAppName(appName)
	clientOptions.SetConnectTimeout(time.Duration(timeOut) * time.Second)
	client, err := mongo.Connect(context.TODO(), clientOptions)
	if err != nil {
		Log.Fatal(err)
		return nil
	}
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		Log.Fatal(err)
		return nil
	}
	Log.Println("Connected to MongoDB!")
	return client
}

func Dbdb() *mongo.Database {
	error1, CONFIG_JSON := loadJson()
	if error1 != nil {
		panic(error1)
	}
	db := CONFIG_JSON["db"].(map[string]interface{})
	name := db["name"].(string)
	dbx := dbClient.Database(name)
	Log.Println("Connected to " + name)
	return dbx
}

func DbCollection(name string) *mongo.Collection {
	return dbDb.Collection(name)
}

func DbClose() {
	err := dbClient.Disconnect(context.TODO())
	if err != nil {
		Log.Fatal(err)
	}
	Log.Println("Connection to MongoDB closed.")
}

func DbInsert(body *ManageNoteStruct) (error, *ManageNoteStruct) {
	insertResult, err := DbCollection(DB_COL).InsertOne(context.TODO(), body)
	if err != nil {
		return err, nil
	}
	if oid, ok := insertResult.InsertedID.(primitive.ObjectID); ok {
		body.ID = oid
	} else {
		return errors.New("ID no definido"), nil
	}
	return nil, body
}

func DbGetByID(id string) (error, *ManageNoteStruct) {
	_id, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return err, nil
	}
	filter := bson.D{{"_id", _id}}
	var result = ManageNoteStruct{}
	err = DbCollection(DB_COL).FindOne(context.TODO(), filter).Decode(&result)
	if err != nil {
		return err, nil
	}
	return nil, &result
}

func DbUpdate(id string, body ManageNoteStruct) error {
	_id, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return err
	}
	filter := bson.D{{"_id", _id}}
	update := bson.D{{"$set", body}}
	_, err = DbCollection(DB_COL).UpdateOne(context.TODO(), filter, update)
	if err != nil {
		return err
	}
	return nil
}

func DbDeleteById(id string) error {
	_id, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return err
	}
	opts := options.Delete().SetCollation(&options.Collation{})
	filter := bson.D{{"_id", _id}}
	_, err = DbCollection(DB_COL).DeleteOne(context.TODO(), filter, opts)
	if err != nil {
		return err
	}
	return nil
}
