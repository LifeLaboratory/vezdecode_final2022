import React, { useState } from "react";
import ReactDOM from "react-dom/client";

import "@vkontakte/vkui/dist/vkui.css";
import { MailList } from "./components/mail/MailList"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
      <MailList  />
);
