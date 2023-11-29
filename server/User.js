const mongoose = require("mongoose");
const noteSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true },
  password: String,
});
const User = mongoose.model("user", noteSchema);
module.exports = User;
