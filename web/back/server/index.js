const React = require('react')
const ReactDOM = require("react-dom")
const { MailList } = require("./../src/components/mail/MailList")
const { SSRWrapper } = require("@vkontakte/vkui")
const express = require("express")
const useragent = require("express-useragent")
const ReactDOMServer = require('react-dom/server');
const server = express();
server.use(useragent.express());

import {
  AdaptivityProvider,
  ConfigProvider,
  useAdaptivity,
  AppRoot,
  SplitLayout,
  SplitCol,
  ViewWidth,
  View,
  Panel,
  PanelHeader,
  Header,
  Group,
  SimpleCell,
} from "@vkontakte/vkui";



server.get("/", function (req, res) {
  res.send(
    ReactDOMServer.renderToString(
      <SSRWrapper userAgent={req.useragent.source}>
        <ConfigProvider>
          <AdaptivityProvider>
            <MailList />
          </AdaptivityProvider>
        </ConfigProvider>,
      </SSRWrapper>
    )
  );
});

server.listen(3005);