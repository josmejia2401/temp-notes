package main

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type TempNoteStruct struct {
	ID            primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
	Title         string             `bson:"title,omitempty" json:"title,omitempty"`
	Description   string             `bson:"description,omitempty" json:"description,omitempty"`
	OwnerUsername string             `bson:"ownerUsername,omitempty" json:"ownerUsername,omitempty"`
	CreatedAt     time.Time          `bson:"createdAt,omitempty" json:"createdAt,omitempty"`
	UpdatedAt     time.Time          `bson:"updatedAt,omitempty" json:"updatedAt,omitempty"`
}
