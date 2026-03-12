const express = require("express")
const mongoose = require("mongoose")
const bodyParser = require("body-parser")
const path = require("path")

const app = express()

app.use(bodyParser.urlencoded({ extended: true }))

// MongoDB connection
mongoose.connect("mongodb://mongodb:27017/userdb")

const UserSchema = new mongoose.Schema({
    username: String,
    email: String
})

const User = mongoose.model("User", UserSchema)

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "views", "form.html"))
})

app.post("/user", async (req, res) => {

    const newUser = new User({
        username: req.body.username,
        email: req.body.email
    })

    await newUser.save()

    res.send("User saved successfully!")
})

app.listen(3000, () => {
    console.log("Server running on port 3000")
})