// const fs = require("fs");
// const { Button, SSRWrapper } = require("@vkontakte/vkui")
// const {reactDomServer} = require('react-dom/server')
// module.exports = function (app, db) {
//     app.get('/', (req, res) => {
//         // match({ routes: routes, location: req.url }, (err, redirect, props) => {
//         //     let html = reactDomServer.renderToString(
//         //         <SSRWrapper userAgent={req.useragent.source}>
//         //             <Button>Hello</Button>
//         //         </SSRWrapper>
//         //     )
//         //     res.send(renderPage(html))
//         const context = ReactDOMServer.renderToString(
//              <SSRWrapper userAgent={req.useragent.source}>
//                      <Button>Hello</Button>
//              </SSRWrapper>
//         )
//         })
//   });
// };