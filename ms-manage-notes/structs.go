package main

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)


type ManageNoteStruct struct {
	ID          	primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
	Title       	string             `bson:"url,omitempty" json:"url,omitempty"`
	Description 	string             `bson:"description,omitempty" json:"description,omitempty"`
	OwnerUsername 	string 			   `bson:"customerId,omitempty" json:"customerId,omitempty"`
	CreatedAt   	time.Time          `bson:"createdAt,omitempty" json:"createdAt,omitempty"`
	UpdatedAt   	time.Time          `bson:"updatedAt,omitempty" json:"updatedAt,omitempty"`
}
