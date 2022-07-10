// routes/index.js
const mailRoutes = require('./mail');
module.exports = function(app, db) {
  mailRoutes(app, db);
  // Тут, позже, будут и другие обработчики маршрутов 
};