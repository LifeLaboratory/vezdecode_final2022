// routes/index.js
const imagesRoutes = require('./images.js');
module.exports = function(app, db) {
 imagesRoutes(app, db);
  // Тут, позже, будут и другие обработчики маршрутов 
};